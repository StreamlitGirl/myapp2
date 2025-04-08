from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'mysql.railway.internal',
    'user': 'root',
    'password': 'WxMcKJBKaOyynAhtzjCwccIpQcJXuvGE',
    'database': 'railway',
    'port' : 3306
}


@app.route('/rdv', methods=['POST'])
def get_appointments():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username:
            return jsonify({'error': 'Missing username'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch appointments from the database
        query = """
        SELECT appointment_date, details, patient_mail
        FROM appointments
        WHERE patient_mail = %s
        """
        cursor.execute(query, (username,))
        appointments = cursor.fetchall()

        if appointments:
            # Prepare the response with appointment details
            response_data = []
            for appointment in appointments:
                appointment_data = {
                    'date': appointment[0].strftime('%B %d, %Y'),  # Format date
                    'time': appointment[0].strftime('%I:%M %p'),  # Format time
                    'details': appointment[1],
                    'status': 'Upcoming'  # You can adjust logic to set the status based on date
                }
                response_data.append(appointment_data)

            return jsonify({'appointments': response_data}), 200
        else:
            return jsonify({'message': 'No appointments found for this user'}), 405

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
