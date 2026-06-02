const API = "http://127.0.0.1:5000/todos";

async function loadTodos() {

    const response = await fetch(API);
    const todos = await response.json();

    const list = document.getElementById("todoList");
    list.innerHTML = "";

    todos.forEach(todo => {

        const li = document.createElement("li");

        li.innerHTML = `
            <span class="${todo.completed ? "completed" : ""}">
                ${todo.title}
            </span>

            <div>
                <button onclick="toggleTodo(${todo.id}, '${todo.title}', ${todo.completed})">
                    ✓
                </button>

                <button onclick="deleteTodo(${todo.id})">
                    Delete
                </button>
            </div>
        `;

        list.appendChild(li);
    });
}

async function addTodo(){

    const input = document.getElementById("todoInput");

    if(!input.value) return;

    await fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            title:input.value
        })
    });

    input.value="";
    loadTodos();
}

async function deleteTodo(id){

    await fetch(`${API}/${id}`,{
        method:"DELETE"
    });

    loadTodos();
}

async function toggleTodo(id,title,completed){

    await fetch(`${API}/${id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            title:title,
            completed:!completed
        })
    });

    loadTodos();
}

loadTodos();
