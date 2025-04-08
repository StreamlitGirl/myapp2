from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'mysql.railway.internal',
    'user': 'root',
    'password': 'WxMcKJBKaOyynAhtzjCwccIpQcJXuvGE',
    'database': 'railway',
    'port' : 3306
}

@app.route('/add_patient', methods=['POST'])
def add_patient():
    conn = None
    cursor = None
    try:
        # Get JSON data from Flutter request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user already exists
        query_check = "SELECT * FROM patient WHERE mail = %s"
        cursor.execute(query_check, (email,))
        existing_user = cursor.fetchone()  # Fetch one row

        if existing_user:
            return jsonify({'message' : 'User already exists'}), 400

        # Insert data into the patient table
        query_insert = "INSERT INTO patient (mail, pwd) VALUES (%s, %s)"
        cursor.execute(query_insert, (email, password))
        conn.commit()

        return jsonify({'message': 'User added successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
