from flask import Flask, render_template, request, redirect, url_for
import threading
import atexit
from util import load_random_quote, get_postgres_connection
from mail import send_email
import schedule
import time
from datetime import datetime, date
from util import generate_email_body
import psycopg2

app = Flask(__name__, static_url_path='/static', static_folder='static')

def send_daily_quote():
    print("Preparing Quote")
    quote = load_random_quote()
    if quote:
        print(f"Today's random quote is \n\n{quote}\n\n")
        message = generate_email_body(quote['quote'], quote['source'])

        today = date.today().strftime("%B %d, %Y")
        subject = f"Daily Baba Quote {today}"

        # Connect to the PostgreSQL database to fetch subscribers
        conn = get_postgres_connection()
        cur = conn.cursor()
        cur.execute('SELECT email FROM subscribers')
        subscribers = [email[0] for email in cur.fetchall()]
        cur.close()
        conn.close()

        print("connection was closed")
        print(subscribers)

        if subscribers:
            send_email(subject, message, subscribers)
    else:
        print("No quote found for today.")



def run_scheduler():
    schedule.every().day.at("12:00").do(send_daily_quote)
    
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
            conn = get_postgres_connection()
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO subscribers (email) VALUES (%s)', (email,))
                conn.commit()
                print(f"SUBSCRIPTION: Adding {email}")
            except psycopg2.IntegrityError:
                conn.rollback()  # Roll back the transaction on error
                print("Email already exists.")
            finally:
                cur.close()
                conn.close()
            return redirect(url_for('subscribe'))
    return render_template('subscribe.html')


@app.route('/suggest_quote', methods=['POST'])
def suggest_quote():
    quote_link = request.form.get('quoteLink', '')
    quote_text = request.form.get('quoteText', '')
    author = request.form.get('author', 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    suggestion = f"SUGGESTION: Time: {timestamp}, Link: {quote_link}, Quote: {quote_text}, Author: {author}\n"
    print(suggestion)

    # Connect to the PostgreSQL database
    conn = get_postgres_connection()
    cur = conn.cursor()

    try:
        # Insert the suggestion into the suggested_quotes table
        cur.execute('INSERT INTO suggested_quotes (quote_link, quote_text, author, timestamp) VALUES (%s, %s, %s, %s)',
                    (quote_link, quote_text, author, timestamp))
        conn.commit()
    except Exception as e:
        # Handle any exceptions, such as integrity errors for duplicates, etc.
        conn.rollback()
        print(f"Error submitting suggestion: {e}")
    finally:
        # Ensure the database connection is closed
        cur.close()
        conn.close()

    return redirect(url_for('subscribe'))

@app.route('/test')
def test_route():
    return "Test route it is testing!"

if __name__ == '__main__':
    atexit.register(lambda: schedule.clear())  # Clear the scheduler when the app exits
    app.run()