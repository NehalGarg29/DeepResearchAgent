from groq import Groq
from app.config import settings
from typing import List
import json

class QueryDecomposer:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.MODEL_NAME

    def decompose(self, query: str) -> List[str]:
        """Decompose a complex research query into sub-questions using Groq."""
        system_prompt = (
            "You are a research expert. Decompose the following complex research query into 2-4 simpler, "
            "independent sub-questions that can be answered through search. "
            "Return the sub-questions as a JSON object with a key 'sub_questions' containing a list of strings."
        )
        user_prompt = f"Query: {query}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        try:
            content = json.loads(response.choices[0].message.content)
            return content.get("sub_questions", [query])
        except Exception:
            return [query]

query_decomposer = QueryDecomposer()
