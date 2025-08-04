import sqlite3
import json

DATABASE_FILE = 'warriors_path.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """Initializes the database by creating tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_data (
            date TEXT PRIMARY KEY,
            completed_workouts TEXT,
            todo_list TEXT,
            shloka_shown INTEGER,
            run_list TEXT,
            physical_tasks TEXT,
            journal_entry TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            deadline TEXT,
            current_streak INTEGER,
            last_completion_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_daily_data(date_str):
    """Retrieves data for a specific day."""
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM daily_data WHERE date = ?', (date_str,)).fetchone()
    conn.close()
    if data:
        # Deserialize JSON data from text fields
        return {
            'completedWorkouts': json.loads(data['completed_workouts']) if data['completed_workouts'] else [],
            'todoList': json.loads(data['todo_list']) if data['todo_list'] else [],
            'shlokaShown': bool(data['shloka_shown']),
            'runList': json.loads(data['run_list']) if data['run_list'] else [],
            'physicalTasks': json.loads(data['physical_tasks']) if data['physical_tasks'] else [],
            'journalEntry': data['journal_entry'] if data['journal_entry'] else ''
        }
    return {}

def get_all_daily_data():
    """Retrieves data for all days for the calendar and charts."""
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM daily_data').fetchall()
    conn.close()
    all_data = {}
    for row in data:
        all_data[row['date']] = {
            'completedWorkouts': json.loads(row['completed_workouts']) if row['completed_workouts'] else [],
            'todoList': json.loads(row['todo_list']) if row['todo_list'] else [],
            'shlokaShown': bool(row['shloka_shown']),
            'runList': json.loads(row['run_list']) if row['run_list'] else [],
            'physicalTasks': json.loads(row['physical_tasks']) if row['physical_tasks'] else [],
            'journalEntry': row['journal_entry'] if row['journal_entry'] else ''
        }
    return all_data

def update_daily_data(date_str, updates):
    """Updates or inserts data for a specific day."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if a record for the date exists
    existing_data = cursor.execute('SELECT * FROM daily_data WHERE date = ?', (date_str,)).fetchone()
    
    if existing_data:
        # Get existing data and update with new values
        completed_workouts = updates.get('completedWorkouts', json.loads(existing_data['completed_workouts']) if existing_data['completed_workouts'] else [])
        todo_list = updates.get('todoList', json.loads(existing_data['todo_list']) if existing_data['todo_list'] else [])
        shloka_shown = updates.get('shlokaShown', existing_data['shloka_shown'])
        run_list = updates.get('runList', json.loads(existing_data['run_list']) if existing_data['run_list'] else [])
        physical_tasks = updates.get('physicalTasks', json.loads(existing_data['physical_tasks']) if existing_data['physical_tasks'] else [])
        journal_entry = updates.get('journalEntry', existing_data['journal_entry'])
        
        cursor.execute('''
            UPDATE daily_data SET completed_workouts = ?, todo_list = ?, shloka_shown = ?,
            run_list = ?, physical_tasks = ?, journal_entry = ? WHERE date = ?
        ''', (json.dumps(completed_workouts), json.dumps(todo_list), shloka_shown, json.dumps(run_list), json.dumps(physical_tasks), journal_entry, date_str))
    else:
        # Insert new data
        completed_workouts = updates.get('completedWorkouts', [])
        todo_list = updates.get('todoList', [])
        shloka_shown = updates.get('shlokaShown', False)
        run_list = updates.get('runList', [])
        physical_tasks = updates.get('physicalTasks', [])
        journal_entry = updates.get('journalEntry', '')

        cursor.execute('''
            INSERT INTO daily_data (date, completed_workouts, todo_list, shloka_shown, run_list, physical_tasks, journal_entry)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date_str, json.dumps(completed_workouts), json.dumps(todo_list), shloka_shown, json.dumps(run_list), json.dumps(physical_tasks), journal_entry))

    conn.commit()
    conn.close()

def get_user_profile():
    """Retrieves user profile data (goal, streak)."""
    conn = get_db_connection()
    profile = conn.execute('SELECT * FROM user_profile').fetchone()
    conn.close()
    if profile:
        return {
            'goal': profile['goal'],
            'deadline': profile['deadline'],
            'currentStreak': profile['current_streak'],
            'lastCompletionDate': profile['last_completion_date']
        }
    return {'goal': None, 'deadline': None, 'currentStreak': 0, 'lastCompletionDate': None}

def set_long_term_goal(goal, deadline):
    """Sets or updates the user's long-term goal."""
    conn = get_db_connection()
    conn.execute('DELETE FROM user_profile') # Simplifies logic for a single user
    conn.execute('INSERT INTO user_profile (id, goal, deadline, current_streak) VALUES (1, ?, ?, 0)', (goal, deadline))
    conn.commit()
    conn.close()

def delete_long_term_goal():
    """Deletes the user's long-term goal."""
    conn = get_db_connection()
    conn.execute('UPDATE user_profile SET goal = NULL, deadline = NULL')
    conn.commit()
    conn.close()

def update_streak(new_streak, last_completion_date):
    """Updates the user's streak data."""
    conn = get_db_connection()
    conn.execute('UPDATE user_profile SET current_streak = ?, last_completion_date = ? WHERE id = 1', (new_streak, last_completion_date))
    conn.commit()
    conn.close()

