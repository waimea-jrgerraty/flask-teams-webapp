#===========================================================
# Database Related Functions
#===========================================================

from libsql_client import create_client_sync, LibsqlError
from contextlib import contextmanager
from dotenv import load_dotenv
from os import getenv, path
from colorama import Fore, init

# Colorama config
init(autoreset=True)

# Logging colours
DB_COL = Fore.MAGENTA

# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = getenv("TURSO_URL")
TURSO_KEY = getenv("TURSO_KEY")


#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
@contextmanager
def connect_db():
    from flask import current_app as app
    client = None

    try:
        # Create a connection to the Turso DB
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)

        # Clear any past queries
        app.dbSQL = None
        app.dbParams = None

        # Wrap the execute method to add logging
        original_execute = client.execute

        def logged_execute(sql, *params, **kwargs):
            # Store for later error handling
            app.dbSQL = sql
            app.dbParams = params

            # Log the query
            if app.debug:
                print(f"            DB SQL: {DB_COL}{sql}")
                print(f"            Params: {DB_COL}{params if params else 'None'}")

            # Run the query
            result = original_execute(sql, *params, **kwargs)

            # Log result
            if app.debug:
                sqlUp = sql.upper()
                if 'SELECT' in sqlUp:
                    print(f"          Row Data: {DB_COL}{getattr(result, 'rows', result)}")
                elif 'UPDATE' in sqlUp or 'DELETE' in sqlUp:
                    print(f"              Rows: {DB_COL}{getattr(result, 'rows_affected', result)}")
                elif 'INSERT' in sqlUp:
                    print(f"            New ID: {DB_COL}{getattr(result, 'last_insert_rowid', result)}")

            return result

        # Update the execute function
        client.execute = logged_execute
        # And return the client connection
        yield client

    finally:
        if client is not None:
            client.close()


