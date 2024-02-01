import os
from flask import Flask, jsonify, request, render_template
import mysql.connector

# Our app variable
app = Flask(__name__)

# Variable for database connection information from docker-compose file
db_config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'database': os.environ['DB_NAME']
}

@app.route('/')
def hello():
    # Index page
    return render_template("index.html")

@app.route('/get_data', methods=['GET'])
def get_data():
    # Connect to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Execute a CREATE TABLE command to make the data table if not already created
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS data (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))"
    )

    # Execute a SELECT query to retrieve data
    query = "SELECT * FROM data"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    # Convert the result to a JSON response
    data = [{'id': row[0], 'name': row[1]} for row in rows]
    return jsonify(data)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    # Get the data from the request body
    data = request.get_json()
    name = data['name']

    # Connect to the MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Execute a CREATE TABLE command to make the data table if not already created
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS data (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))"
    )

    # Execute an INSERT query to store the data
    query = "INSERT INTO data (name) VALUES (%s)"
    cursor.execute(query, (name,))

    # Commit the transaction and close the database connection
    connection.commit()
    cursor.close()
    connection.close()

    # Return a success message
    return jsonify({'message': 'Data created successfully'})

@app.route('/delete_data/<int:id>', methods=['DELETE'])
def delete_data(id):
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Execute a DELETE command to remove the data
    delete_query = "DELETE FROM data WHERE id = %s"
    cursor.execute(delete_query, (id,))

    # Commit the transaction and close the database connection
    conn.commit()
    cursor.close()
    conn.close()

    # Return a success message
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0')
