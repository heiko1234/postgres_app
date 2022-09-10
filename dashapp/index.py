
"""Main application file"""

from app.postgres_app import app


# assign the server to run in docker and support debugging in vs code
server = app.server


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)


