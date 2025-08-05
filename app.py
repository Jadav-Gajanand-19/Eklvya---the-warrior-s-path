from flask import Flask, render_template

# The database.py file is no longer needed with Firebase.

app = Flask(__name__)

# The Flask backend is now simplified. Its primary role is to serve the
# main HTML file. All application logic, including authentication and
# data persistence, will be handled by the client-side JavaScript using
# Firebase SDKs.
@app.route('/')
def index():
    """
    Renders the main index page.
    The page will handle user authentication and data display entirely in JavaScript.
    """
    # We no longer need to pass data from the backend to the template.
    # The frontend will fetch data directly from Firestore.
    return render_template('index.html')

if __name__ == '__main__':
    # A simple development server. In a production environment, you would use
    # a production WSGI server like Gunicorn.
    app.run(debug=True)

