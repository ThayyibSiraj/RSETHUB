from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            event_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()
    return render_template('events.html', event=event)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO registrations (name, email, event_id) VALUES (?, ?, ?)', (name, email, event_id))
        conn.commit()
        conn.close()
        flash('You have successfully registered for the event!')
        return redirect(url_for('index'))
    return render_template('register.html', event_id=event_id)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        
        # Insert the new event into the database
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (title, date, description) VALUES (?, ?, ?)', (title, date, description))
        conn.commit()
        conn.close()

        flash('Event created successfully!')
        return redirect(url_for('index'))

    # If it's a GET request, just render the form
    return render_template('create_event.html')

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    flash('Event has been deleted successfully!')
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>/registrations')
def event_registrations(event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registrations WHERE event_id = ?', (event_id,))
    registrations = cursor.fetchall()
    conn.close()
    return render_template('registrations.html', registrations=registrations, event_id=event_id)

@app.route('/delete_registration/<int:registration_id>/<int:event_id>', methods=['POST'])
def delete_registration(registration_id, event_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registrations WHERE id = ?', (registration_id,))
    conn.commit()
    conn.close()
    flash('Registration has been deleted successfully!')
    return redirect(url_for('event_registrations', event_id=event_id))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
