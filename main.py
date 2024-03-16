from flask import Flask, render_template, request, redirect, url_for
import threading
import atexit
from util import load_random_quote
from mail import send_email
import schedule
import time
from datetime import datetime, date
from util import generate_email_body
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')

def send_daily_quote():
    quote = load_random_quote()
    if quote:
        print(f"Today's random quote is \n\n{quote}\n\n")
        message = generate_email_body(quote['quote'], quote['source'])

        today = date.today().strftime("%B %d, %Y")
        subject = f"Daily Baba Quote {today}"

        # Connect to the database to fetch subscribers
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        cur.execute('SELECT email FROM subscribers')
        subscribers = [email[0] for email in cur.fetchall()]
        conn.close()

        print("connection was closed")
        print(subscribers)

        if subscribers:
            send_email(subject, message, subscribers)
    else:
        print("No quote found for today.")



def run_scheduler():
    schedule.every().day.at("10:18").do(send_daily_quote)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()


@app.route('/', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            try:
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()
                cur.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
                conn.commit()
                print(f"SUBSCRIPTION: Adding {email}")
            except sqlite3.IntegrityError:
                print("Email already exists.")
            finally:
                conn.close()
            return redirect(url_for('subscribe'))
    return render_template('subscribe.html')


@app.route('/suggest_quote', methods=['POST'])
def suggest_quote():
    print("SUGGESTION:")
    quote_link = request.form.get('quoteLink', '')
    quote_text = request.form.get('quoteText', '')
    author = request.form.get('author', 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    suggestion =  f"SUGGESTION: Time: {timestamp}, Link: {quote_link}, Quote: {quote_text}, Author: {author}\n"
    print(suggestion)

    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO suggested_quotes (quote_link, quote_text, author) VALUES (?, ?, ?)',
                (quote_link, quote_text, author))
    conn.commit()
    conn.close()

    return redirect(url_for('subscribe'))

@app.route('/test')
def test_route():
    return "Test route it is testing!"

if __name__ == '__main__':
    atexit.register(lambda: schedule.clear())  # Clear the scheduler when the app exits
    app.run(debug=True)