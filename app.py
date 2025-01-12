import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
    # Render the welcome page with animated "Team SPY" text
    return render_template("welcome.html")

if __name__ == "__main__":
    # Default to port 5000 if PORT is not set in the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
