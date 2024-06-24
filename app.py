from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_bro():
    return "Team SPY"

if __name__ == "__ main__":
    app.run()
