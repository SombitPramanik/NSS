from flask import Flask, Response, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def Index():
    return render_template("index.html")


@app.route("/Members")
def Members():
    return render_template("members.html")

if __name__ == "__main__":
    app.run(debug=True)