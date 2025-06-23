#===========================================================
# Error Handling Functions
#===========================================================

from flask import render_template
from colorama import Fore, init
import traceback
import sys

# Colorama config
init(autoreset=True)

# Logging colours
ERR_COL = Fore.RED
CODE_COL = Fore.BLUE
ERR_BAR = f"{ERR_COL}!{Fore.RESET}"


#-----------------------------------------------------------
# 500 Server error page
#-----------------------------------------------------------
def server_error(message):
    return render_template("pages/500.jinja", error=message), 500


#-----------------------------------------------------------
# 404 Page not found error page
#-----------------------------------------------------------
def not_found_error():
    return render_template("pages/404.jinja"), 404


#-----------------------------------------------------------
# Provide error handlers to the Flask app
#-----------------------------------------------------------
def init_error(app):

    #------------------------------
    # 404 Page not found error page
    #------------------------------
    @app.errorhandler(404)
    def show_not_found(e):
        return not_found_error()


    #------------------------------
    # 500 Server error page
    #------------------------------
    @app.errorhandler(500)
    def show_server_error(e):
        return server_error(str(e))


    #------------------------------
    # General exception error page
    #------------------------------
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Only show verbose error details if debugging
        if app.debug:
            # Get the last frame from the traceback code (not Flask internals)
            tb = traceback.extract_tb(sys.exc_info()[2])

            # Find the last frame that's in your the directory
            app_frame = None
            for frame in reversed(tb):
                if 'venv' not in frame.filename and 'site-packages' not in frame.filename:
                    app_frame = frame
                    break

            errorName = type(e).__name__
            errorDetails = str(e)

            # Deal with libSQL exceptions relating to SQL errors
            sqlError = errorName == 'KeyError' and errorDetails == "'result'"
            if sqlError:
                errorName = "SQL Error"
                errorDetails = "There is an error in your SQL"

            print()
            print(f"           {ERR_COL}  Error: {ERR_COL}{errorName}")
            print(f"           {ERR_COL} Detail: {ERR_COL}{errorDetails}")

            error_msg = f"""
                <table class="error">
                    <tr><th>Error</th><td>{errorName}</td></tr>
                    <tr><th>Details</th><td>{errorDetails}</td></tr>
            """

            # Do we have a matching error frame?
            if app_frame:
                if not sqlError:
                    filename = app_frame.filename.replace(app.root_path, "")

                    print(f"           {ERR_COL}   File: {CODE_COL}{filename}")
                    print(f"           {ERR_COL}   Line: {CODE_COL}{app_frame.lineno}")
                    print(f"           {ERR_COL}   Code: {CODE_COL}{app_frame.line}")
                    print()

                    error_msg += f"""
                        <tr><th>File</th><td>{filename}</td></tr>
                        <tr><th>Line</th><td>{app_frame.lineno}</td></tr>
                        <tr><th>Code</th><td><code>{app_frame.line}</code></td></tr>
                    """
                else:
                    if app.dbSQL:
                        print(f"           {ERR_COL}   Code: {CODE_COL}{app.dbSQL}")
                        print()

                        error_msg += f"""
                            <tr><th>Code</th><td><code>{app.dbSQL}</code></td></tr>
                        """

            error_msg += "</table>"

            return server_error(error_msg)

        # Else just a generic message
        return server_error("An unexpected server error occurred")
