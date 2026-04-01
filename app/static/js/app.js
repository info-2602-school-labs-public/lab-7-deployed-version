async function getTodoData() {
    const response = await fetch('/api/todos');

    if (!response.ok) {
        console.error("API error:", await response.text());
        return [];
    }

    return response.json();
}

function loadTable(todos) {
    const table = document.querySelector('#result');
    table.innerHTML = "";

    if (!Array.isArray(todos)) {
        console.error("Expected array but got:", todos);
        return;
    }

    todos.forEach(todo => {
        table.innerHTML += `
        <tr>
            <td>${todo.id}</td>
            <td>${todo.text}</td>
            <td>${todo.done ? "Done" : "Pending"}</td>
        </tr>`;
    });
}

async function refreshTable() {
    const todos = await getTodoData();
    loadTable(todos);
}

/* ADD TODO WITHOUT RELOAD */
document.getElementById("todoForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const text = document.getElementById("todoInput").value;

    await fetch('/todos', {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `text=${encodeURIComponent(text)}`
    });

    document.getElementById("todoInput").value = "";

    await refreshTable();
});

/* SEARCH */
function filterTodos() {
    const search = document.getElementById("search").value.toLowerCase();
    const rows = document.querySelectorAll("#result tr");

    rows.forEach(row => {
        const text = row.children[1].innerText.toLowerCase();
        row.style.display = text.includes(search) ? "" : "none";
    });
}

/* INITIAL LOAD */
refreshTable();