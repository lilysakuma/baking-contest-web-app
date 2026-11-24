# Baking Contest Web App

A simple baking contest website built with Python, Flask, SQLite, and HTML.

## About the Project

I originally created this project for a computer science class at Florida State University. The goal was to build a website that connects to a database and allows users to submit and view information through a web interface.

I decided to include this project in my portfolio because it demonstrates my experience working with Python, databases, and backend web development.

## Features

- Register new baking contest participants
- Submit baking contest entries
- Record excellent, OK, and bad votes
- View registered participants and contest results
- Validate user input and display error messages
- Store information in a SQLite database

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- Jinja2

## How to Run

Clone the repository:

```bash
git clone https://github.com/lilysakuma/baking-contest-web-app.git
cd baking-contest-web-app
```

Install Flask:

```bash
python3 -m pip install -r requirements.txt
```

Set up the database:

```bash
python3 init_db.py
```

Run the application:

```bash
python3 app.py
```

Open `http://127.0.0.1:50001` in your browser.

## Database

The database consists of two tables:

- `BakingContestPeople` — stores participant information.
- `BakingContestEntry` — stores baking entries and their vote counts.

The tables are connected through a user ID, which allows each participant to have multiple baking entries.

## What I Learned

This project helped me better understand how a website communicates with a database. I gained experience with Flask routes, GET and POST requests, SQL queries, input validation, and displaying database information through HTML templates.

I also learned how to use parameterized SQL queries to help prevent SQL injection.

## Security Note

Since this project was made for a class, passwords are stored as plain text and displayed in the original user listing. If this were a real-world application, I would hash passwords before storing them, remove them from the user listing, and implement proper authentication and access controls.

This project is intended for demonstration purposes only. Only fictional user information should be used.

## Testing

I added 8 automated tests using Python's unittest library to make sure everything works as expected. These tests check user registration, baking entries, invalid inputs, and whether information is being saved and displayed correctly.

I used a temporary database for testing so that the original database would not be changed.

To run the tests:

```bash
python3 -m unittest test_app -v
```

All 8 tests passed.

## Future Improvements

- Improve the website's appearance with CSS
- Add secure password storage and authentication
- Add the ability to edit and delete entries
- Display contest rankings based on votes

## Author

Lily Sakuma  
Computer Science Student at Florida State University

AI assistance was used during development and debugging.