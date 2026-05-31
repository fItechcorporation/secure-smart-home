from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import jsonify

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_home.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

device_state = {
    "manual_led": False
}

# ----------------------------
# Malaysia Timezone Function
# ----------------------------

def malaysia_time():
    return datetime.utcnow() + timedelta(hours=8)

# ----------------------------
# User Table
# ----------------------------

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    
# ----------------------------
# Device Table
# ----------------------------

class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50))
    api_key = db.Column(db.String(100))
    last_seen = db.Column(db.DateTime, default=malaysia_time)

# ----------------------------
# Alert Table
# ----------------------------

class Alert(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=malaysia_time)

# ----------------------------
# Log Table
# ----------------------------

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=malaysia_time)

# ----------------------------
# Login Credentials
# ----------------------------

USERNAME = "admin"
PASSWORD = "password123"

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def home():
    return redirect(url_for("login"))

# ----------------------------
# Login
# ----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(
            username=username,
            password=password
            ).first()
        
        if user:

            log = Log(
                action="Admin Login Success"
            )

            db.session.add(log)
            db.session.commit()

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")

# ----------------------------
# Simulate Motion Detection
# ----------------------------

@app.route("/simulate_motion", methods=["POST"])
def simulate_motion():

    alert = Alert(
        message="Motion Detected!"
    )

    db.session.add(alert)

    log = Log(
        action="Motion Alert Triggered"
    )

    db.session.add(log)

    db.session.commit()

    return redirect(url_for("dashboard"))

# ----------------------------
# Heartbeat API for Device
# ----------------------------

@app.route("/api/device-heartbeat", methods=["POST"])
def device_heartbeat():

    device = Device.query.filter_by(
        device_id="ESP32_001"
    ).first()

    if device is None:

        device = Device(
            device_id="ESP32_001",
            api_key="SECURE123",
            last_seen=malaysia_time()
        )

        db.session.add(device)

    else:

        device.last_seen = malaysia_time()

    db.session.commit()

    return {
        "status": "alive"
    }

# ----------------------------
# Dashboard
# ----------------------------

@app.route("/dashboard")
def dashboard():

    logs = Log.query.order_by(
        Log.timestamp.desc()
    ).all()

    alerts = Alert.query.order_by(
        Alert.timestamp.desc()
    ).all()

    print("TOTAL LOGS:", len(logs))
    print("TOTAL ALERTS:", len(alerts))

    device = Device.query.filter_by(
        device_id="ESP32_001"
    ).first()

    device_online = False
    
    if device and device.last_seen:
        diff = malaysia_time() - device.last_seen
        
        print("LAST SEEN:", device.last_seen)
        print("NOW:", malaysia_time())
        print("DIFF:", diff.total_seconds())

    print("SECONDS SINCE LAST HEARTBEAT:",
          diff.total_seconds())

    if diff.total_seconds() < 10:
        device_online = True

    return render_template(
        "dashboard.html",
        logs=logs,
        alerts=alerts,
        device_online=device_online
    )

# ----------------------------
# Turn ON
# ----------------------------

@app.route("/turn_on", methods=["POST"])
def turn_on():

    device_state["manual_led"] = True

    log = Log(
        action="LED ON"
    )

    db.session.add(log)
    db.session.commit()

    return redirect(url_for("dashboard"))

# ----------------------------
# Turn OFF
# ----------------------------

@app.route("/turn_off", methods=["POST"])
def turn_off():

    device_state["manual_led"] = False

    log = Log(
        action="LED OFF"
    )

    db.session.add(log)
    db.session.commit()

    return redirect(url_for("dashboard"))

# ----------------------------
# Simulate Motion Detection API
# ----------------------------

@app.route("/api/motion", methods=["POST"])
def motion_alert():

    alert = Alert(
        message="Motion Detected!"
    )

    db.session.add(alert)

    log = Log(
        action="Motion Detected By PIR Sensor"
    )

    db.session.add(log)

    db.session.commit()

    return {
        "status": "success"
    }

# ----------------------------
# Device Command API
# ----------------------------

@app.route("/api/device-command")
def device_command():

    return jsonify({
        "manual_led": device_state["manual_led"]
    })

# ----------------------------
# Run Application
# ----------------------------

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        # Create Admin User
        admin = User.query.filter_by(
            username="admin"
        ).first()

        if admin is None:

            admin = User(
                username="admin",
                password="password123"
            )

            db.session.add(admin)
            db.session.commit()

        # Create ESP32 Device
        device = Device.query.filter_by(
            device_id="ESP32_001"
        ).first()

        if device is None:

            device = Device(
                device_id="ESP32_001",
                api_key="SECURE123"
            )

            db.session.add(device)
            db.session.commit()

    app.run(debug=True)