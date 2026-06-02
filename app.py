from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/todos", methods=["GET"])
def get_todos():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM todos")
    rows = cur.fetchall()

    conn.close()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])
        })

    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO todos(title) VALUES(?)",
        (data["title"],)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Added"})

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    UPDATE todos
    SET title=?, completed=?
    WHERE id=?
    """,(
        data["title"],
        int(data["completed"]),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message":"Updated"})

@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM todos WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
