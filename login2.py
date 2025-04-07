from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'istic.glsi3',
    'database': 'monpfe'
}

@app.route('/login', methods=['POST'])
def login_patient():
    try:
        data = request.get_json()
        mail = data.get('mail')
        pwd = data.get('pwd')
        
        # Corrected the variable names to match with 'mail' and 'pwd'
        if not mail or not pwd:
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Establish MySQL connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Query to check if user exists and password matches
        query_all = "SELECT * FROM patient WHERE mail = %s AND pwd = %s"
        cursor.execute(query_all, (mail, pwd))
        user = cursor.fetchone()
        
        if user:
            return jsonify({'message': 'Let him in'}), 200
        else:
            # Check if the email exists for wrong password case
            query_mail = "SELECT * FROM patient WHERE mail = %s"
            cursor.execute(query_mail, (mail,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({'message': 'Wrong password'}), 402
            else:
                return jsonify({'message': 'User not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
