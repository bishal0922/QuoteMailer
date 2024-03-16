import sqlite3

def load_random_quote():
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute('SELECT quote, source, philosophy FROM quotes ORDER BY RANDOM() LIMIT 1')
    quote = cur.fetchone()
    conn.close()
    if quote:
        return {'quote': quote[0], 'source': quote[1], 'philosophy': quote[2]}
    else:
        return None


def generate_email_body(quote, source):
    body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Daily Philosophy Quote</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .quote {{
                font-size: 18px;
                color: #333333;
                margin-bottom: 20px;
            }}
            .source {{
                font-size: 14px;
                color: #666666;
            }}
            .footer {{
                font-size: 12px;
                color: #999999;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="quote">{quote}</p>
            <p class="source">- {source}</p>
        </div>
        <p class="footer">Sent with love by Baba Bishal ❤️</p>
    </body>
    </html>
    """
    return body


