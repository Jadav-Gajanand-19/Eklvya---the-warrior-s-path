from flask import Flask, render_template, request, jsonify
from datetime import datetime
import database
import json

app = Flask(__name__)

# Route to the home page, which will display the daily tracker
@app.route('/')
def index():
    # Get today's date in YYYY-MM-DD format
    today_date = datetime.now().strftime('%Y-%m-%d')
    # Get all daily data for the calendar view and charts
    all_data = database.get_all_daily_data()
    # Get streak and goal data
    user_profile = database.get_user_profile()
    
    # Render the index.html template and pass the necessary data
    return render_template(
        'index.html',
        today=today_date,
        all_data=all_data,
        user_profile=user_profile
    )

# API endpoint to get data for a specific day
@app.route('/api/day/<date_str>')
def get_day_data(date_str):
    data = database.get_daily_data(date_str)
    return jsonify(data)

# API endpoint to get all data
@app.route('/api/all_data')
def get_all_data():
    all_data = database.get_all_daily_data()
    return jsonify(all_data)

# API endpoint to save or update daily data
@app.route('/api/save_daily_data', methods=['POST'])
def save_daily_data():
    data = request.json
    date_str = data.get('date')
    updates = data.get('updates')
    if date_str and updates:
        database.update_daily_data(date_str, updates)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid data"}), 400

# API endpoint to set or update a long-term goal
@app.route('/api/set_goal', methods=['POST'])
def set_goal():
    data = request.json
    goal = data.get('goal')
    deadline = data.get('deadline')
    database.set_long_term_goal(goal, deadline)
    return jsonify({"success": True})

# API endpoint to delete a long-term goal
@app.route('/api/delete_goal', methods=['POST'])
def delete_goal_api():
    database.delete_long_term_goal()
    return jsonify({"success": True})

# API endpoint to save a journal entry
@app.route('/api/save_journal', methods=['POST'])
def save_journal_api():
    data = request.json
    date_str = data.get('date')
    journal_entry = data.get('journalEntry')
    if date_str is None or journal_entry is None:
        return jsonify({"success": False, "error": "Invalid data"}), 400
    database.update_daily_data(date_str, {'journalEntry': journal_entry})
    return jsonify({"success": True})


# Initialize database on application startup
with app.app_context():
    database.init_db()

if __name__ == '__main__':
    app.run(debug=True)

