from flask import (
    Flask,
    Response,
    render_template,
    request,
    redirect,
    session,
    url_for,
)
import mysql.connector
from mysql.connector import Error


with open("DBSecret.key", "r") as Key:
    DataBaseSecret = Key.read()
    Key.close()

DB_User_Name = DataBaseSecret.split(",")[0]
DB_Password = DataBaseSecret.split(",")[1]


app = Flask(__name__)


def DBConnector(user=DB_User_Name, password=DB_Password):
    """Create a database Connection and return the Connection object."""
    try:
        Connection = mysql.connector.connect(
            host="127.0.0.1",
            user=user,
            password=password,
            database="NSS_CEMK",
        )
        if Connection.is_connected():
            print("Connection to the database was successful")
            return Connection
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to the database")
        return None


@app.route("/")
def Index():
    return render_template("index.html")


@app.route("/Members")
def Members():
    return render_template("members.html")


@app.route("/About")
def About():
    return render_template("about.html")


@app.route("/SendOTP")
def SendOTP():
    otp = 121313
    return otp


@app.route("/Login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        Email = request.form["Email"]
        Password = request.form["Password"]
        OTP = request.form["OTP"]
        Connection = DBConnector()
        if Connection:
            cursor = Connection.cursor(dictionary=True)
            query = (
                "SELECT * FROM LoginDB WHERE Email = %s AND Password = %s AND OTP = %s"
            )
            cursor.execute(query, (Email, Password, OTP))
            result = cursor.fetchone()
            cursor.close()
            Connection.close()

            if result:
                session["Email"] = Email
                return redirect(url_for("Dashboard"))
            else:
                error = "Invalid user or OTP"
                return render_template("login.html", error=error)
        else:
            error = "Internal Error Please try after some time"
            return render_template("login.html", error=error)
    elif request.method == "GET":
        return render_template("login.html")
    else:
        return Response("Nothing to worry I am hear then Why Fear")


if __name__ == "__main__":
    app.run(debug=True)
