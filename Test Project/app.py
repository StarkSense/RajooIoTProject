from flask import Flask, g, jsonify, request
from flask_socketio import SocketIO, emit
import sqlite3
import threading
import time
from datetime import datetime
import os


DB_FILE = "blownfilm.db" if os.path.exists("blownfilm.db") else "blownfilm"
if not os.path.exists(DB_FILE):
    raise FileNotFoundError(f"Database file not found: {DB_FILE}")

DATABASE = DB_FILE
print(f"Using database: {DATABASE}")

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app, cors_allowed_origins="*")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


#HEALTH CHECK
@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "database": DATABASE,
        "message": "Flask IoT Backend connected to blownfilm database"
    })


#FETCH TELEMETRY FROM ALL TABLES
@app.route("/api/telemetry", methods=["GET"])
def telemetry_all_tables():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cur.fetchall()]

        db_data = {}
        if not tables:
            return jsonify({
                "status": "ok",
                "database": DATABASE,
                "table_count": 0,
                "tables": {},
                "timestamp": datetime.utcnow().isoformat(),
                "message": "No tables found in database."
            })

        for table in tables:
            try:
                cur.execute(f"SELECT * FROM {table} ORDER BY ROWID DESC LIMIT 50")
                rows = cur.fetchall()
                db_data[table] = [row_to_dict(row) for row in rows]
            except Exception as e:
                db_data[table] = [{"error": str(e)}]

        cur.close()

        return jsonify({
            "status": "ok",
            "database": DATABASE,
            "table_count": len(tables),
            "timestamp": datetime.utcnow().isoformat(),
            "tables": db_data
        })

    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#REAL-TIME STREAMING (WebSocket)
@socketio.on("connect")
def handle_connect():
    print(f"Client connected: {request.sid}")
    emit("server_message", {"message": f"Connected to live telemetry stream ({DATABASE})"})

@socketio.on("disconnect")
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

def background_data_stream():
  
    while True:
        try:
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

    
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row["name"] for row in cur.fetchall()]

            db_snapshot = {}
            for table in tables:
                try:
                    cur.execute(f"SELECT * FROM {table} ORDER BY ROWID DESC LIMIT 1")
                    rows = cur.fetchall()
                    db_snapshot[table] = [dict(row) for row in rows]
                except Exception as e:
                    db_snapshot[table] = [{"error": str(e)}]

            conn.close()

            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "database": DATABASE,
                "table_count": len(tables),
                "tables": db_snapshot
            }

            socketio.emit("telemetry_update", payload)

            time.sleep(30)  
        except Exception as e:
            print("Background thread error:", e)
            time.sleep(5)


thread = threading.Thread(target=background_data_stream)
thread.daemon = True
thread.start()


# START SERVER
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
