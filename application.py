import os
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date

load_dotenv()  # Load environment variables from .env file
application = Flask(__name__)
# TODO: update the CORS configuration
cors = CORS(application)
is_dev_mode = os.getenv('FLASK_ENV') == 'development'

def get_questions_for_date(date):
    with open(os.path.join('questions', 'backend_questions.json'), 'r') as f:
        questions_list = json.load(f)
        question_set_to_use = calculate_days_past_july_14_2025(date)
        return questions_list[question_set_to_use % len(questions_list)]

def calculate_days_past_july_14_2025(input_date):
    """
    Calculates the number of days that have passed since July 14, 2025.
    Args:
        input_date (date): date object
    Returns:
        int: The number of days past July 14, 2025, or None if the input date is invalid.
    """
    try:
        start_date = date(2025, 6, 14)

        if input_date < start_date:
            return None  # Return None if the input date is before July 14, 2025

        days_passed = (input_date - start_date).days
        return days_passed

    except ValueError:
        return None  # Return None if the input date format is invalid

@application.route('/api/questions/<date_string>')
def get_data_by_date(date_string, methods=['GET']):
    """
      Args:
        date_string (str): The input date in the format 'YYYY-MM-DD'.
    """
    api_key = request.headers.get('Authorization').replace('Bearer ', '', 1)  # Extract the key without 'Bearer '
    if api_key != os.getenv('API_KEY'):
        return jsonify({"error": "Invalid API key"}), 401  # Unauthorized

    date_obj = date.fromisoformat(date_string)
    return jsonify(get_questions_for_date(date_obj))

if __name__ == '__main__':
    application.run(debug=is_dev_mode)
