
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

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS machine_timeseries (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         tag TEXT,
#         value REAL,
#         index_no INTEGER,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
#     """)

#     conn.commit()
#     conn.close()


# def insert_machine_overview(data):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO machine_overview
#         (total_set_output, total_actual_output, density, gsm, lay_flat)
#         VALUES (?, ?, ?, ?, ?)
#     """, tuple(data.values()))
#     conn.commit()
#     conn.close()


# def insert_timeseries(tag, value, index_no=None):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO machine_timeseries (tag, value, index_no)
#         VALUES (?, ?, ?)
#     """, (tag, value, index_no))
#     conn.commit()
#     conn.close()


# def fetch_machine_overview(limit=1):
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT *
#         FROM machine_overview
#         ORDER BY id DESC
#         LIMIT ?
#     """, (limit,))

#     rows = cur.fetchall()
#     conn.close()
#     return [dict(r) for r in rows]




# def fetch_series(tag, limit=30):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT value FROM machine_timeseries
#         WHERE tag = ?
#         ORDER BY timestamp ASC
#         LIMIT ?
#     """, (tag, limit))
#     rows = cur.fetchall()
#     conn.close()
#     return [r["value"] for r in rows]


# def fetch_profile(tag):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT index_no, value FROM machine_timeseries
#         WHERE tag = ?
#         ORDER BY index_no ASC
#     """, (tag,))
#     rows = cur.fetchall()
#     conn.close()
#     return [{"x": r["index_no"], "y": r["value"]} for r in rows]


# def fetch_zonewise(tag):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT index_no, value FROM machine_timeseries
#         WHERE tag = ?
#         ORDER BY index_no ASC
#     """, (tag,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows


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
# DB INIT
# =========================================================
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


# =========================================================
# INSERTS
# =========================================================
def insert_machine_overview(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO machine_overview
        (total_set_output, total_actual_output, density, gsm, lay_flat)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["total_set_output"],
        data["total_actual_output"],
        data["density"],
        data["gsm"],
        data["lay_flat"]
    ))
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


# =========================================================
# FETCH – MACHINE OVERVIEW (KPIs)
# =========================================================
def fetch_machine_overview(limit=1):
    """
    Always return the latest KPI snapshot(s)
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM machine_overview
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =========================================================
# FETCH – TIME SERIES (GRAPHS)
# =========================================================
def fetch_series(tag, limit=30):
    """
    Fetch latest N values for a tag in correct time order
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT ?
    """, (tag, limit))

    rows = cur.fetchall()
    conn.close()

    # reverse so graph goes left → right (old → new)
    return [r["value"] for r in rows[::-1]]


# =========================================================
# FETCH – PROFILES (LIP / MAP)
# =========================================================
def fetch_profile(tag):
    """
    Profiles are overwrite-based, order by index_no
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT index_no, value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))

    rows = cur.fetchall()
    conn.close()

    return [{"x": r["index_no"], "y": r["value"]} for r in rows]


# =========================================================
# FETCH – ZONE-WISE (DIE TEMP)
# =========================================================
def fetch_zonewise(tag):
    """
    Zone data is overwrite-based, order by index_no
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT index_no, value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))

    rows = cur.fetchall()
    conn.close()
    return rows
