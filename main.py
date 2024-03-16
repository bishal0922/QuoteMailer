from flask import Flask, render_template, request, redirect, url_for
import threading
import atexit
from util import load_random_quote
from mail import send_email
import schedule
import time
from datetime import datetime, date
from util import generate_email_body

app = Flask(__name__, static_url_path='/static', static_folder='static')

def send_daily_quote():
    quote = load_random_quote()
    print(f"Today's random quote is \n\n{quote}\n\n")
    message = f"{quote['quote']}\n\n- {quote['source']}, {quote['philosophy']}"
    message = generate_email_body(quote['quote'], quote['source'])

    today = date.today().strftime("%B %d, %Y")
    subject = f"Daily Baba Quote {today}"

    with open('subscribers.txt', 'r', encoding='utf-8') as file:
        subscribers = [email.strip() for email in file.readlines() if email.strip()]
    if subscribers:
        send_email(subject, message, subscribers)

def run_scheduler():
    schedule.every().day.at("21:39").do(send_daily_quote)
    
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
            print(f"SUBSCRIPTION: Adding {email}")
            with open('subscribers.txt', 'a', encoding='utf-8') as file:
                file.write(email + '\n')
            return redirect(url_for('subscribe'))
    # Render a subscription form
    return render_template('subscribe.html')

@app.route('/suggest_quote', methods=['POST'])
def suggest_quote():
    print("SUGGESTION:")
    quote_link = request.form.get('quoteLink', '')
    quote_text = request.form.get('quoteText', '')
    author = request.form.get('author', 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"quote_link: {quote_link}")
    print(f"quote_text: {quote_text}")
    print(f"author: {author}")

    suggestion =  f"Time: {timestamp}, Link: {quote_link}, Quote: {quote_text}, Author: {author}\n"
    with open('suggested.txt', 'a', encoding='utf-8') as file:
        file.write(suggestion)
    return redirect(url_for('subscribe'))

if __name__ == '__main__':
    atexit.register(lambda: schedule.clear())  # Clear the scheduler when the app exits
    app.run(debug=True)