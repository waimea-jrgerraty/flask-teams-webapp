# A Basic Flask App Linked to a Turso Database

This is template for a simple [Flask](https://flask.palletsprojects.com) application with a [Turso](https://turso.tech/) SQLite database to store and provide data. The app uses [Jinja2](https://jinja.palletsprojects.com/templates/) templating for structuring pages and data, and [PicoCSS](https://picocss.com/) for styling.

This app provides **user sign-up, login and logout**. Certain features of the app are adjusted / restricted based on whether the user is logged in or not: Menu items, DB actions like add and delete, etc.


## Project Structure

- **app** folder

    - **static** folder - Files to be served as-is
        - **css** folder
            - **styles.css** - A user stylesheet
        - **images** folder
            - **icon.svg** - Site favicon
            - *other example images*
        - **js** folder
            - **utils.js** - Utility functions

    - **templates** folder
        - **components** folder
            - **messages.jinja** - Block to display flash messages
            - *other component templates*
        - **pages** folder
            - **base.jinja** - The base template for all pages
            - *other templates for specific pages*

    - **helpers** folder - Utility functions
        - **db.py** - Functions for database access
        - **errors.py** - Functions for error reporting
        - **session.py** - Functions to manage session data
        - **auth.py** - Functions to manage authentication
        - **time.py** - Functions to help format timestamps

    - **\_\_init__.py** - App launcher code

- **requirements.txt** - Defines the Python modules needed

- **.env** - Environment variable, e.g. Turso secrets
- **.env.example** - Demo .env file
- **.gitignore** - Prevents venv and .env from being pushed


## Demo Database Schema

The database used for this demo has the following schema:

```sql
CREATE TABLE `users` (
    `id`            INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`          TEXT NOT NULL,
    `username`      TEXT NOT NULL UNIQUE,
    `password_hash` TEXT NOT NULL
);

CREATE TABLE `things` (
    `id`      INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`    TEXT    NOT NULL,
    `price`   INTEGER NOT NULL DEFAULT 0,
    `user_id` INTEGER NOT NULL,

	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
    ON UPDATE CASCADE ON DELETE CASCADE
);
```


## Project Setup and Deployment

See [SETUP.md](SETUP.md) for details of how to install and run the app locally for development, how to setup and configure the [Turso](https://turso.tech/) database, and how to deploy the app to [Render](https://render.com/) for hosting.

## Demo Site

A demo of this site is hosted [here](https://flask-turso-basic-app-setup.onrender.com)

*Note: This is a read-only version to avoid the DB being spammed!*
