from groq import Groq
from app.config import settings
from app.memory.chroma_store import memory_manager
from app.agent.constraints import ConstraintManager
from app.memory.session_store import session_manager
from app.agent.query_decomposer import query_decomposer
from app.agent.retriever import retriever
from typing import List, Dict, Any, Optional
from loguru import logger
import json

class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.MODEL_NAME

    async def perform_research(self, query: str) -> Dict[str, Any]:
        """Perform deep research on a given complex query using Groq."""
        constraints = ConstraintManager()
        
        # Step 1: Decompose original query into sub-questions
        sub_queries = query_decomposer.decompose(query)
        logger.info(f"Decomposed query into: {sub_queries}")
        
        # Step 2: Retrieve context for each sub-query
        all_context = []
        for sq in sub_queries:
            constraints.add_retrieval()
            results = retriever.retrieve(sq)
            all_context.extend([r['content'] for r in results])

        context_str = "\n\n".join(list(set(all_context))) # deduplicate

        # Step 3: Synthesis and Answer Generation
        system_prompt = (
            "You are a specialized deep research assistant. Use the provided context to answer the user research query. "
            "If the context is insufficient, explain what is missing and then answer to the best of your knowledge."
        )
        user_prompt = f"Context:\n{context_str}\n\nSearch Query: {query}"

        # Note: Token counting might need adjustment for Groq/Llama models, but we'll use tiktoken as an approximation.
        constraints.add_token_count(system_prompt + user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                max_tokens=4000
            )

            answer = response.choices[0].message.content
            constraints.add_token_count(answer)

            # Step 4: Self-Evaluation
            evaluation = self._evaluate_response(query, answer, context_str)
            
            # Step 5: Save the result back to memory
            memory_manager.add_document(
                content=f"Research on: {query}\nResult: {answer}",
                metadata={"type": "research_result", "query": query}
            )

            # Step 6: Log everything to SQLite
            status = "completed"
            if constraints.is_budget_exceeded(): status = "budget_exceeded"
            elif constraints.is_retrieval_exceeded(): status = "retrieval_exceeded"

            session_manager.log_research(
                query=query,
                token_usage=constraints.used_tokens,
                retrieval_count=constraints.retrieval_count,
                status=status,
                evaluation=evaluation
            )

            return {
                "query": query,
                "sub_queries": sub_queries,
                "answer": answer,
                "evaluation": evaluation,
                "usage_status": constraints.get_status()
            }
        except Exception as e:
            logger.error(f"Error in research: {str(e)}")
            session_manager.log_research(
                query=query,
                token_usage=constraints.used_tokens,
                retrieval_count=constraints.retrieval_count,
                status="failed"
            )
            raise e

    def _evaluate_response(self, query: str, answer: str, context: str) -> Dict[str, Any]:
        """Perform a simple self-evaluation using Groq."""
        eval_prompt = (
            "Evaluate the quality of the research answer below based on the original query and context provided. "
            "Score from 1 to 5 on: Relevance, Accuracy, and Conciseness. Return a JSON object."
        )
        eval_user = f"Query: {query}\nAnswer: {answer}\nContext (Sample): {context[:1000]}..."

        try:
            eval_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": eval_prompt},
                    {"role": "user", "content": eval_user}
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            return json.loads(eval_response.choices[0].message.content)
        except Exception:
            return {"relevance": 0, "accuracy": 0, "conciseness": 0, "notes": "Evaluation failed."}

research_agent = ResearchAgent()

research_agent = ResearchAgent()
