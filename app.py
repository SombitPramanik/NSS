from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
)
import mysql.connector
from mysql.connector import Error
import random
import requests

with open("DBSecret.key", "r") as Key:
    DataBaseSecret = Key.read()
    Key.close()

DB_User_Name = DataBaseSecret.split(",")[0]
DB_Password = DataBaseSecret.split(",")[1]


app = Flask(__name__)
app.secret_key = '*$(#sds08279s**0923}wew@@)' 

def DBConnector(user=DB_User_Name, password=DB_Password):
    try:
        print(password,user)
        Connection = mysql.connector.connect(
            host="localhost",
            user=user.strip(),
            password=password.strip(),
            database="NSS_CEMK",
        )
        if Connection.is_connected():
            # print("Connection to the database was successful")
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


@app.route("/Dashboard")
def Dashboard():
    if 'AuthID' in session:
        return render_template("dashboard.html")
    else:
        return redirect("/")


@app.route("/SendOTP", methods=["POST"])
def SendOTP():
    data = request.get_json()
    Email = data.get("Email")
    Password = data.get("Password")

    Connection = DBConnector()
    if Connection:
        cursor = Connection.cursor(dictionary=True)
        query = "SELECT * FROM LoginDB WHERE Email = %s AND Password = %s"
        cursor.execute(query, (Email, Password))
        result = cursor.fetchone()
        if not result:
            return jsonify({"Message":"Unregistered Email, Incident Reported"})
        cursor.close()
        Connection.close()

        OTP = random.randint(000000, 999999)
        with open("EmailTemplate.html","r") as Ett:
            EmailMessage = Ett.read()
            Ett.close()

        with open("EmailAPI.key","r") as key:
            APIKey = key.read()
            key.close()

        APIDate = {
            "AuthID": f"{APIKey}",
            "ReceiverEmail": Email,
            "Subject": "OTP Verification CEMK NSS Dashboard Access",
            "Message": EmailMessage,
        }
        url = "https://smtp.spptechnologies.in/"
        response = requests.post(url, json=APIDate)
        if response:
            session["OTP"] = OTP
            session["Email"] = Email

            if result:
                return jsonify({"Message": True})
            else:
                return jsonify({"Message": False})
        else:
            return jsonify({"Message":"Some Problems with the Email API"})
    else:
        return jsonify({"Message":"Some Problems with our Backend"})


@app.route("/VerifyOTP", methods=["POST"])
def VerifyOTP():
    data = request.get_json()
    user_otp = data.get("OTP")
    
    if 'OTP' in session and session['OTP'] == int(user_otp):
        session['AuthID'] = f"{session["Email"]}{session["OTP"]}"
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/Logout")
def Logout():
    session.clear()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
