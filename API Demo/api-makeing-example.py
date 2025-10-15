from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (in-memory storage)
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# POST: Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = {"id": len(users) + 1, "name": data['name']}
    users.append(new_user)
    return jsonify(new_user), 201

# PUT: Update user details
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user["id"] == user_id:
            user["name"] = data["name"]
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# DELETE: Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"})

# Run the server
if __name__ == '__main__':
    app.run(debug=True)  