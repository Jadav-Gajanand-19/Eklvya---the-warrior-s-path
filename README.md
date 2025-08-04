# 🛡 The Warrior's Path: Daily Tracker

## 📖 Overview
**The Warrior's Path** is a web-based daily tracker designed to help you build discipline and track your long-term goals. Inspired by the principles of the Bhagavad Gita, the application provides a centralized hub to log your daily activities, set and track goals, and visualize your progress over time.

## ✨ Features
- ✅ **Daily Planner**: Log and track daily physical tasks and to-do items.
- 🏃 **Endurance Running Tracker**: Track your running distance and time, with dynamic charts.
- 🎯 **Long-Term Goal Setting**: Set and monitor a long-term goal with a deadline.
- 📓 **Personal Journal**: Reflect through daily journal entries.
- 📅 **Interactive Calendar**: View and navigate past entries.
- 📊 **Progress Charts**: Visualize weekly trends in workouts and running.
- 📜 **Daily Inspiration**: Receive daily verses from the Bhagavad Gita.
- 💾 **Persistent Data**: All data is stored in a local SQLite database.

## 🛠 Tech Stack
- **Backend**: Python + Flask
- **Database**: SQLite3
- **Frontend**: HTML, JavaScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js

## 🚀 Setup & Installation

### 1. Clone the repository or download the files
Ensure `app.py`, `database.py`, and `index.html` are in the same folder.

### 2. Install dependencies
Install Flask if not already installed:
```bash
pip install Flask
```

### 3. Run the app
```bash
python app.py
```
Open your browser at: [http://localhost:5000](http://localhost:5000)
Live Link : https://eklvya-warrior-path-9b7b315e6f82.herokuapp.com/

## 🔌 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Loads the homepage |
| `/api/day/<date_str>` | GET | Retrieves data for a specific day |
| `/api/save_daily_data` | POST | Saves or updates a day’s data |
| `/api/set_goal` | POST | Sets a long-term goal |
| `/api/delete_goal` | POST | Deletes the current goal |
| `/api/save_journal` | POST | Saves a journal entry |

## 🗃 Database Schema

### `daily_data`
| Column | Type | Description |
|--------|------|-------------|
| `date` | TEXT | Primary key (YYYY-MM-DD) |
| `todo_list` | TEXT | JSON string of todos |
| `run_list` | TEXT | JSON string of run logs |
| `physical_tasks` | TEXT | JSON string of workouts |
| `journal_entry` | TEXT | Daily reflection text |
| `completed_workouts` | TEXT | Retained from original schema |
| `shloka_shown` | INTEGER | Quote displayed flag |

### `user_profile`
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `goal` | TEXT | Long-term goal |
| `deadline` | TEXT | Goal deadline |
| `current_streak` | INTEGER | Current discipline streak |
| `last_completion_date` | TEXT | Date of last completed streak |

## 🙏 Credits
- Inspired by the timeless wisdom of the **Bhagavad Gita**.
- Built using **Python**, **Flask**, and **SQLite**.
- UI designed with **Tailwind CSS** and **Chart.js**.