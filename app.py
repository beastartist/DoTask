# Simple To-Do List App using Flask
from flask import Flask, jsonify, request
from datetime import datetime

# Create a Flask web application
app = Flask(__name__)

# ---------------------------------
# In-memory data storage
# ---------------------------------
# This list will act like our temporary "database"
todos = []
next_id = 1  # We'll manually increase this to give each task a unique ID


# Helper function to find a to-do item by its ID
def find_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


# ---------------------------------
# 1. Create a new To-Do
# ---------------------------------
# Example: POST /todos  with JSON body like {"task": "Buy groceries"}
@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id

    # Get the JSON data sent by the user
    data = request.get_json()

    # Check if 'task' is given, otherwise return an error
    if not data or "task" not in data:
        return jsonify({"error": "Please provide a 'task' field"}), 400

    # Create a new to-do item
    new_todo = {
        "id": next_id,
        "task": data["task"],
        "isCompleted": False,
        "createdAt": datetime.utcnow().isoformat()
    }

    # Add it to our list
    todos.append(new_todo)
    next_id += 1  # increase the id for the next task

    return jsonify(new_todo), 201


# ---------------------------------
# 2. Get all To-Dos
# ---------------------------------
# Example: GET /todos
@app.route("/todos", methods=["GET"])
def get_all_todos():
    # Just send back the entire list of todos
    return jsonify(todos), 200


# ---------------------------------
# 3. Get a To-Do by its ID
# ---------------------------------
# Example: GET /todos/1
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo_by_id(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


# ---------------------------------
# 4. Update a To-Do
# ---------------------------------
# Example: PUT /todos/1  with JSON {"task": "Buy milk", "isCompleted": true}
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Update the task fields if provided
    if "task" in data:
        todo["task"] = data["task"]
    if "isCompleted" in data:
        todo["isCompleted"] = data["isCompleted"]

    return jsonify(todo), 200


# ---------------------------------
# 5. Delete a To-Do
# ---------------------------------
# Example: DELETE /todos/1
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    todos.remove(todo)
    return jsonify({"message": f"Todo with id {todo_id} deleted successfully"}), 200


# ---------------------------------
# Optional: A simple home route to test if server is running
# ---------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the doTask API!",
        "info": "Use the /todos endpoint to manage your tasks."
    }), 200


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
