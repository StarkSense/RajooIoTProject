

# import sqlite3
# from pathlib import Path

# DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"


# # =========================================================
# # DB CONNECTION
# # =========================================================

# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


# # =========================================================
# # INITIALIZATION
# # =========================================================

# def init_db():
#     conn = get_db()
#     cur = conn.cursor()

   
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS machine_overview (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         total_set_output REAL,
#         total_actual_output REAL,
#         density REAL,
#         gsm REAL,
#         lay_flat REAL,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

   
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS layer_snapshot (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         layer_name TEXT,
#         speed REAL,
#         yield REAL,
#         ampere REAL,
#         set_thickness REAL,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     conn.commit()
#     conn.close()
#     print("[INIT] Database ready")


# # =========================================================
# # DASHBOARD (MAIN) DATA
# # =========================================================

# def get_updates():
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT
#             total_set_output,
#             total_actual_output,
#             density,
#             gsm,
#             lay_flat,
#             timestamp
#         FROM machine_overview
#         ORDER BY id DESC
#         LIMIT 1
#     """)

#     row = cur.fetchone()
#     conn.close()

#     return dict(row) if row else {}


# # =========================================================
# # LAYER DATA 
# # =========================================================

# def save_layer_snapshot(layer_name, speed, yield_val, ampere, set_thickness):
#     """
#     Stores only latest numeric values for history/debug.
#     Graph data stays in memory (SocketIO).
#     """
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO layer_snapshot (
#             layer_name,
#             speed,
#             yield,
#             ampere,
#             set_thickness
#         ) VALUES (?, ?, ?, ?, ?)
#     """, (
#         layer_name,
#         speed,
#         yield_val,
#         ampere,
#         set_thickness
#     ))

#     conn.commit()
#     conn.close()


# def get_latest_layer_snapshot(layer_name):
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT
#             speed,
#             yield,
#             ampere,
#             set_thickness,
#             timestamp
#         FROM layer_snapshot
#         WHERE layer_name = ?
#         ORDER BY id DESC
#         LIMIT 1
#     """, (layer_name,))

#     row = cur.fetchone()
#     conn.close()

#     return dict(row) if row else {}


import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS machine_overview (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_set_output REAL,
        total_actual_output REAL,
        density REAL,
        gsm REAL,
        lay_flat REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS machine_timeseries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT,
        value REAL,
        index_no INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_machine_overview(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO machine_overview
        (total_set_output, total_actual_output, density, gsm, lay_flat)
        VALUES (?, ?, ?, ?, ?)
    """, tuple(data.values()))
    conn.commit()
    conn.close()


def insert_timeseries(tag, value, index_no=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO machine_timeseries (tag, value, index_no)
        VALUES (?, ?, ?)
    """, (tag, value, index_no))
    conn.commit()
    conn.close()


def fetch_machine_overview(limit=30):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM machine_overview
        ORDER BY timestamp ASC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_series(tag, limit=30):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT value FROM machine_timeseries
        WHERE tag = ?
        ORDER BY timestamp ASC
        LIMIT ?
    """, (tag, limit))
    rows = cur.fetchall()
    conn.close()
    return [r["value"] for r in rows]


def fetch_profile(tag):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT index_no, value FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))
    rows = cur.fetchall()
    conn.close()
    return [{"x": r["index_no"], "y": r["value"]} for r in rows]


def fetch_zonewise(tag):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT index_no, value FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))
    rows = cur.fetchall()
    conn.close()
    return rows
