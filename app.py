from flask import (
    Flask,
    Response,
    render_template,
    request,
    redirect,
    session,
    url_for,
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
app.secret_key = '*$(#sds08279s**[sdso])' 

def DBConnector(user=DB_User_Name, password=DB_Password):
    """Create a database Connection and return the Connection object."""
    try:
        print(password,user)
        Connection = mysql.connector.connect(
            host="localhost",
            user=user.strip(),
            password=password.strip(),
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
        cursor.close()
        Connection.close()

        OTP = random.randint(000000, 999999)
        EmailMessage = f"""\
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        padding-bottom: 20px;
                        border-bottom: 1px solid #dddddd;
                    }}
                    .header h1 {{
                        font-size: 24px;
                        margin: 0;
                    }}
                    .content {{
                        padding: 20px 0;
                        text-align: center;
                    }}
                    .content p {{
                        font-size: 16px;
                        margin: 10px 0;
                    }}
                    .otp {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #333333;
                        margin-top: 20px;
                    }}
                    .footer {{
                        text-align: center;
                        padding-top: 20px;
                        border-top: 1px solid #dddddd;
                    }}
                    .footer p {{
                        font-size: 14px;
                        color: #777777;
                        margin: 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>NSS CEMK</h1>
                    </div>
                    <div class="content">
                        <p>Welcome to CEMK NSS Admin Page Mr/Ms <strong>{Email}</strong>,</p>
                        <p>Here is your verification OTP:</p>
                        <div class="otp">{OTP}</div>
                    </div>
                    <div class="footer">
                        <p>This Platform is Truly Developed by Sombit Pramanik</p>
                    </div>
                </div>
            </body>
            </html>
            """
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
                
        print(OTP)
        session["OTP"] = OTP
        session["Email"] = Email

        if result:
            return jsonify(True)
        else:
            return jsonify(False)
    
    return jsonify("Invalid connection")


@app.route("/VerifyOTP", methods=["POST"])
def VerifyOTP():
    data = request.get_json()
    user_otp = data.get("OTP")
    
    if 'OTP' in session and session['OTP'] == int(user_otp):
        session['AuthID'] = f"{session["Email"]}{session["OTP"]}"
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/Dashboard")
def Dashboard():
    if 'AuthID' in session:
        return render_template("dashboard.html")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
