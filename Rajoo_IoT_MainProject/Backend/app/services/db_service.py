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
# # DB INIT
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


# # =========================================================
# # INSERTS
# # =========================================================
# def insert_machine_overview(data):
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO machine_overview
#         (total_set_output, total_actual_output, density, gsm, lay_flat)
#         VALUES (?, ?, ?, ?, ?)
#     """, (
#         data["total_set_output"],
#         data["total_actual_output"],
#         data["density"],
#         data["gsm"],
#         data["lay_flat"]
#     ))
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


# # =========================================================
# # FETCH – MACHINE OVERVIEW (KPIs)
# # =========================================================
# def fetch_machine_overview(limit=1):
#     """
#     Always return the latest KPI snapshot(s)
#     """
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


# # =========================================================
# # FETCH – TIME SERIES (GRAPHS)
# # =========================================================
# def fetch_series(tag, limit=30):
#     """
#     Fetch latest N values for a tag in correct time order
#     """
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT value
#         FROM machine_timeseries
#         WHERE tag = ?
#         ORDER BY id DESC
#         LIMIT ?
#     """, (tag, limit))

#     rows = cur.fetchall()
#     conn.close()

#     # reverse so graph goes left → right (old → new)
#     return [r["value"] for r in rows[::-1]]


# # =========================================================
# # FETCH – PROFILES (LIP / MAP)
# # =========================================================
# def fetch_profile(tag):
#     """
#     Profiles are overwrite-based, order by index_no
#     """
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT index_no, value
#         FROM machine_timeseries
#         WHERE tag = ?
#         ORDER BY index_no ASC
#     """, (tag,))

#     rows = cur.fetchall()
#     conn.close()

#     return [{"x": r["index_no"], "y": r["value"]} for r in rows]


# # =========================================================
# # FETCH – ZONE-WISE (DIE TEMP)
# # =========================================================
# def fetch_zonewise(tag):
#     """
#     Zone data is overwrite-based, order by index_no
#     """
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT index_no, value
#         FROM machine_timeseries
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
# FETCH – GENERIC TIME SERIES (GRAPHS)
# =========================================================
def fetch_series(tag, limit=30):
    """
    Fetch latest N values for any time-series tag
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

    # Old → New (for charts)
    return [r["value"] for r in rows[::-1]]


# =========================================================
# FETCH – LATEST VALUE (KPIs)
# =========================================================
def fetch_latest_value(tag):
    """
    Used for KPIs like layer speed, yield, ampere
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT 1
    """, (tag,))

    row = cur.fetchone()
    conn.close()

    return row["value"] if row else 0


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


# =========================================================
#  FETCH – LAYER KPIs
# =========================================================
def fetch_layer_kpis(layer_id):
    """
    Returns KPIs for a single layer
    """
    return {
        "speed": fetch_latest_value(f"layer_{layer_id}_speed"),
        "yield": fetch_latest_value(f"layer_{layer_id}_yield"),
        "ampere": fetch_latest_value(f"layer_{layer_id}_ampere")
    }


# =========================================================
# FETCH – LAYER GRAPHS
# =========================================================
def fetch_layer_trends(layer_id, limit=30):
    """
    Returns graph data for a single layer
    """
    return {
        "melt_pressure": fetch_series(f"layer_{layer_id}_melt_pressure", limit),
        "melt_temperature": fetch_series(f"layer_{layer_id}_melt_temperature", limit),
        "thickness_set": fetch_series(f"layer_{layer_id}_thickness_set", limit),
        "thickness_actual": fetch_series(f"layer_{layer_id}_thickness_actual", limit),
    }
