from flask import Flask, jsonify, request
import mysql.connector
app = Flask(__name__)
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ciel2027"
)
@app.route('/v3/etudiants/', methods=['GET'])
def login():
    username = "user1"
    password = "123456"
    cursor = mydb.cursor()
    rep = "SELECT * FROM user WHERE login ={username} AND password = {password}"
    cursor.execute(rep)
    data = cursor.fetchone()
    if data:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
if __name__ == '__main__':
    app.run(debug=True)