# import sqlite3
# from pathlib import Path

# DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"


# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


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

#     conn.commit()
#     conn.close()
#     print("[INIT] Database ready")


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


import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"


# =========================================================
# DB CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# INITIALIZATION
# =========================================================

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # ---------------- EXISTING TABLE (UNCHANGED)
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

    # ---------------- NEW: LAYER SNAPSHOT TABLE (OPTIONAL)
    # Stores latest scalar values only (not graphs)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS layer_snapshot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        layer_name TEXT,
        speed REAL,
        yield REAL,
        ampere REAL,
        set_thickness REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("[INIT] Database ready")


# =========================================================
# DASHBOARD (MAIN) DATA
# =========================================================

def get_updates():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            total_set_output,
            total_actual_output,
            density,
            gsm,
            lay_flat,
            timestamp
        FROM machine_overview
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else {}


# =========================================================
# LAYER DATA (OPTIONAL – SNAPSHOT ONLY)
# =========================================================

def save_layer_snapshot(layer_name, speed, yield_val, ampere, set_thickness):
    """
    Stores only latest numeric values for history/debug.
    Graph data stays in memory (SocketIO).
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO layer_snapshot (
            layer_name,
            speed,
            yield,
            ampere,
            set_thickness
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        layer_name,
        speed,
        yield_val,
        ampere,
        set_thickness
    ))

    conn.commit()
    conn.close()


def get_latest_layer_snapshot(layer_name):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            speed,
            yield,
            ampere,
            set_thickness,
            timestamp
        FROM layer_snapshot
        WHERE layer_name = ?
        ORDER BY id DESC
        LIMIT 1
    """, (layer_name,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else {}
