import json
import random

def load_random_quote():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes = json.load(file)
    return random.choice(quotes)

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
        <p class="footer">Sent with love by Baba</p>
    </body>
    </html>
    """
    return body


