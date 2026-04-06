# Dify Integration Notes: Deep Research Agent

This guide explains how to set up the **Deep Research Agent** as a tool or custom agent within **Dify**.

## Scenario 1: Using FastAPI as a Custom Tool
Dify allows you to register external APIs as tools.

1. **Register the Backend**: 
   - Go to **Tools** > **Custom Tools** > **Create Tool**.
   - Set the URL to `http://your-fastapi-host/api/v1/research`.
   - Method: `POST`.
   - Parameter: `query` (String).

2. **Add to Chatflow**:
   - In a Dify workflow, add a **Tool** node.
   - Select the "Deep Research Agent" tool you just created.
   - Pass the output of the "Question Classifier" or "Intent" node to the tool's `query` input.

## Scenario 2: Direct Orchestration in Dify
You can replicate the query decomposition logic within Dify's canvas.

1. **Input Node**: Receive user research query.
2. **LLM Node (Query Decomposer)**:
   - System Prompt: `Decompose the query into 2-4 sub-questions. Output as JSON list.`
3. **Iteration Node (Multi-Retrieve)**:
   - For each sub-question, call the **Vector Store** or **Searching Tool** (like Tavily).
4. **Knowledge Retrieval**: Connect to Dify's built-in Knowledge base (if indexed).
5. **LLM Node (Synthesis)**:
   - Final prompt using all retrieved context and sub-questions.

## Recommended Tool Configurations
- **Tavily Search**: For real-world internet research.
- **SerpAPI**: For Google Search results.
- **Python Code**: For complex data transformations or CSV analysis within Dify.
