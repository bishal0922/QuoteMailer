# QuoteMailer

`babaquotes.vercel.app`
![QuoteMailer](https://babaquotes.vercel.app)

QuoteMailer is a simple web application that sends a daily email to subscribers with a random quote from a database of quotes. The application is built using Python, Flask, and PostgreSQL.

## Features
- Users can subscribe to the daily email list
- Users can suggest quotes to be added to the database

Database schema:
``` SQL
CREATE TABLE IF NOT EXISTS subscribers (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS suggested_quotes (
    id SERIAL PRIMARY KEY,
    quote_link TEXT,
    quote_text TEXT NOT NULL,
    author TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    source TEXT,
    philosophy TEXT
);
```


