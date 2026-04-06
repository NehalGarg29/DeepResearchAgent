document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    const queryInput = document.getElementById('research-query');
    const statusContainer = document.getElementById('status-container');
    const resultContainer = document.getElementById('result-container');
    const statusText = document.getElementById('status-text');
    const subQueriesList = document.getElementById('sub-queries-list');
    const researchAnswer = document.getElementById('research-answer');
    const scoreBadge = document.getElementById('score-badge');
    const tokensUsage = document.getElementById('tokens-usage');
    const retrievalUsage = document.getElementById('retrieval-usage');

    // Auto-resize textarea
    queryInput.addEventListener('input', () => {
        queryInput.style.height = 'auto';
        queryInput.style.height = (queryInput.scrollHeight) + 'px';
    });

    submitBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        // Reset UI
        resultContainer.classList.add('hidden');
        statusContainer.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Researching...';
        
        statusText.textContent = "Decomposing query using Llama 3.3...";

        try {
            const response = await fetch('/api/v1/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) throw new Error("Failed to connect to the agent.");

            const data = await response.json();
            
            // Populate Results
            renderResults(data);

        } catch (error) {
            console.error(error);
            statusText.textContent = "Error: " + error.message;
            statusText.style.color = "#ef4444";
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Start Research';
            statusContainer.classList.add('hidden');
        }
    });

    function renderResults(data) {
        // Clear previous sub-queries
        subQueriesList.innerHTML = '';
        data.sub_queries.forEach(sq => {
            const li = document.createElement('li');
            li.textContent = sq;
            subQueriesList.appendChild(li);
        });

        // Set Answer
        researchAnswer.innerHTML = formatAnswer(data.answer);

        // Set Evaluation & Usage
        const eval = data.evaluation;
        const avgScore = ((eval.Relevance + eval.Accuracy + eval.Conciseness) / 3).toFixed(1);
        scoreBadge.textContent = "Avg Score: " + avgScore + "/5";
        
        tokensUsage.textContent = "Tokens: " + data.usage_status.used_tokens;
        retrievalUsage.textContent = "Retrievals: " + data.usage_status.retrieval_count;

        // Show Container
        resultContainer.classList.remove('hidden');
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }

    function formatAnswer(text) {
        // Simple formatting for bold and newlines
        return text
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }
});
