#===========================================================
# Logging Middleware
#===========================================================

from flask import request, session
from dotenv import load_dotenv
from os import getenv
from colorama import Fore, init
from datetime import datetime
import logging

# Colorama config
init(autoreset=True)

# Logging colours
REQ_COL = Fore.CYAN
ROUTE_COL = Fore.BLUE
SESS_COL = Fore.YELLOW

# Load Flask and Turso environment variables from the .env file
load_dotenv()
HOST = getenv("FLASK_RUN_HOST", "localhost")
PORT = getenv("FLASK_RUN_PORT", 5000)

# Disable built-in logging
logging.getLogger('werkzeug').setLevel(logging.CRITICAL)


#-----------------------------------------------------------
# Return a coloured status message
#-----------------------------------------------------------
def colStatus(response):
    if response.status_code < 300:
        return f"{Fore.GREEN}{response.status}"
    if response.status_code < 400:
        return f"{Fore.YELLOW}{response.status}"
    return f"{Fore.RED}{response.status}"


#-----------------------------------------------------------
# Provide logging handlers to the Flask app
#-----------------------------------------------------------
def init_logging(app):
    # Announce the app...
    print(f"\n🚀 Flask server is running at {Fore.GREEN}http://{HOST}:{PORT}\n")


    #--------------------------------------------------
    # Pre-request logging
    #--------------------------------------------------
    @app.before_request
    def log_request():
        # Don't log at start for static files
        if app.debug and not '/static/' in request.path:
            now = datetime.now().strftime("%H:%M:%S")

            # The URL
            print(f"[{now}] Request: {REQ_COL}{request.method} {request.path}")
            # Matched routing rule
            if request.url_rule:
                print(f"           Matches: {ROUTE_COL}{request.method.lower()}(\"{request.url_rule}\")")
            # Matched route function name
            if request.endpoint:
                print(f"           Handler: {ROUTE_COL}{request.endpoint}()")
            # URL params, if any
            if request.view_args:
                print(f"            Params: {ROUTE_COL}{request.view_args}")
            # Any GET args
            if request.args:
                print(f"              Args: {ROUTE_COL}{dict(request.args)}")
            # Any form data
            if request.form:
                print(f"              Form: {ROUTE_COL}{dict(request.form)}")
            # Any files uploaded
            if request.files:
                print(f"             Files: {ROUTE_COL}{dict(request.files)}")
            # Any session values
            if session:
                print(f"           Session: {SESS_COL}{dict(session)}")


    #--------------------------------------------------
    # Post-request logging
    #--------------------------------------------------
    @app.after_request
    def log_response(response):
        if app.debug:
            # Was this a matched route?
            if not '/static/' in request.path:
                # Yes, so complete it
                print(f"            Status: {colStatus(response)}{Fore.RESET}\n")
            else:
                # Nope, a static file, so show the full request/response
                now = datetime.now().strftime("%H:%M:%S")
                print(f"[{now}] Request: {REQ_COL}{request.method} {request.path} {colStatus(response)}{Fore.RESET}\n")

            return response

