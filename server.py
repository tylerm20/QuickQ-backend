from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import date

app = Flask(__name__)
# TODO: update the CORS configuration
cors = CORS(app)

def get_questions_for_date(date):
    with open('backend_questions.json', 'r') as f:
        questions_list = json.load(f)
        question_set_to_use = calculate_days_past_april_14_2024(date)
        return questions_list[question_set_to_use % len(questions_list)]

def calculate_days_past_april_14_2024(input_date):
    """
    Calculates the number of days that have passed since April 14, 2024.
    Args:
        input_date (date): date object
    Returns:
        int: The number of days past April 14, 2024, or None if the input date is invalid.
    """
    try:
        start_date = date(2024, 4, 14)

        if input_date < start_date:
            return None  # Return None if the input date is before April 14, 2024

        days_passed = (input_date - start_date).days
        return days_passed

    except ValueError:
        return None  # Return None if the input date format is invalid

@app.route('/api/questions/<date_string>')
def get_data_by_date(date_string, methods=['GET']):
    """
      Args:
        date_string (str): The input date in the format 'YYYY-MM-DD'.
    """
    date_obj = date.fromisoformat(date_string)
    return jsonify(get_questions_for_date(date_obj))

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for easier development
