from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Function to create the table if it doesn't exist
def create_table():
    conn = sqlite3.connect('submissions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table when the application starts
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    save_submission(name, email)
    return 'Form submitted!'

def save_submission(name, email):
    conn = sqlite3.connect('submissions.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO submissions (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

@app.route('/submissions')
def submissions():
    submissions = get_submissions()
    return render_template('submissions.html', submissions=submissions)

def get_submissions():
    conn = sqlite3.connect('submissions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email FROM submissions')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    app.run(debug=True)
