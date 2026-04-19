const form = document.getElementById("query-form");
const queryInput = document.getElementById("query-input");
const historyNode = document.getElementById("history");
const statusNode = document.getElementById("status");
const exampleButtons = document.querySelectorAll(".example");

const sessionHistory = [];

function setStatus(text) {
    statusNode.textContent = text;
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function renderHistory() {
    if (sessionHistory.length === 0) {
        historyNode.innerHTML = '<p class="muted">Пока нет запросов.</p>';
        return;
    }

    const reversed = [...sessionHistory].reverse();
    historyNode.innerHTML = reversed
        .map((item) => {
            const meta = `scenario=${item.scenario} | mode=${item.mode} | fallback=${item.fallback}`;
            const trace = `sources=${item.sourcesCount}, retrieval_hits=${item.retrievalHits}`;
            return `
                <article class="item">
                    <div class="query">${escapeHtml(item.query)}</div>
                    <div class="meta">${escapeHtml(meta)} | ${escapeHtml(trace)}</div>
                    <div class="answer">${escapeHtml(item.answer)}</div>
                </article>
            `;
        })
        .join("");
}

async function sendQuery(query) {
    const topK = 3;
    const url = `/scenarios/handle?q=${encodeURIComponent(query)}&top_k=${topK}`;
    setStatus("Выполняется запрос...");
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        sessionHistory.push({
            query: query,
            scenario: data?.scenario?.name ?? "unknown",
            mode: data?.mode ?? "unknown",
            fallback: String(data?.fallback ?? "unknown"),
            answer: data?.answer ?? "",
            sourcesCount: Array.isArray(data?.sources) ? data.sources.length : 0,
            retrievalHits: Array.isArray(data?.retrieval_trace?.results)
                ? data.retrieval_trace.results.length
                : 0,
        });
        renderHistory();
        setStatus("Готово.");
    } catch (error) {
        setStatus(`Ошибка запроса: ${error}`);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = queryInput.value.trim();
    if (!query) {
        setStatus("Введите запрос.");
        return;
    }
    await sendQuery(query);
});

exampleButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const query = button.dataset.q || "";
        queryInput.value = query;
        await sendQuery(query);
    });
});

renderHistory();
