# import random
# from app.extensions import socketio
# from app.services.db_service import get_db, init_db


# def dummy_data_task():
#     print("[DUMMY] Generator started")

#     # Ensure DB + table exists
#     init_db()

#     conn = get_db()
#     cur = conn.cursor()

#     while True:
#         try:
#             cur.execute("""
#                 INSERT INTO machine_overview (
#                     total_set_output,
#                     total_actual_output,
#                     density,
#                     gsm,
#                     lay_flat
#                 ) VALUES (?, ?, ?, ?, ?)
#             """, (
#                 random.uniform(90, 110),
#                 random.uniform(90, 110),
#                 random.uniform(0.9, 1.0),
#                 random.uniform(40, 100),
#                 random.uniform(200, 250)
#             ))

#             conn.commit()
#             print("[DUMMY] Data inserted")

#             socketio.sleep(5)

#         except Exception as e:
#             print("[DUMMY] Error:", e)
#             socketio.sleep(2)


import random
import time
from collections import deque

from app.extensions import socketio
from app.services.db_service import get_db, init_db


# =========================================================
# INTERNAL BUFFERS FOR TIME-SERIES DATA
# =========================================================

MAX_POINTS = 30  # number of points per graph

_layer_buffers = {
    "layer1": {
        "melt_pressure": deque(maxlen=MAX_POINTS),
        "melt_temperature": deque(maxlen=MAX_POINTS),
        "thickness_actual": deque(maxlen=MAX_POINTS),
    },
    "layer2": {
        "melt_pressure": deque(maxlen=MAX_POINTS),
        "melt_temperature": deque(maxlen=MAX_POINTS),
        "thickness_actual": deque(maxlen=MAX_POINTS),
    },
    "layer3": {
        "melt_pressure": deque(maxlen=MAX_POINTS),
        "melt_temperature": deque(maxlen=MAX_POINTS),
        "thickness_actual": deque(maxlen=MAX_POINTS),
    }
}


# =========================================================
# LAYER-WISE DUMMY DATA GENERATOR
# =========================================================

def _generate_layer_data(layer_name):
    buffer = _layer_buffers[layer_name]

    # Scalar live values
    speed = round(random.uniform(180, 260), 2)           # RPM
    yield_val = round(random.uniform(70, 95), 2)         # %
    ampere = round(random.uniform(20, 45), 2)            # A
    set_thickness = round(random.uniform(40, 70), 2)     # micron

    # Time series
    buffer["melt_pressure"].append(round(random.uniform(80, 140), 2))     # Bar
    buffer["melt_temperature"].append(round(random.uniform(160, 230), 2)) # °C
    buffer["thickness_actual"].append(
        round(set_thickness + random.uniform(-3, 3), 2)
    )

    return {
        "speed": speed,
        "yield": yield_val,
        "ampere": ampere,

        "melt_pressure": list(buffer["melt_pressure"]),
        "melt_temperature": list(buffer["melt_temperature"]),

        "thickness": {
            "set": set_thickness,
            "actual": list(buffer["thickness_actual"])
        }
    }


def get_live_layer_data():
    """
    Public function used by telemetry_socket.py
    """
    return {
        "layer1": _generate_layer_data("layer1"),
        "layer2": _generate_layer_data("layer2"),
        "layer3": _generate_layer_data("layer3"),
    }


# =========================================================
# EXISTING DUMMY DATA TASK (MERGED, NOT REMOVED)
# =========================================================

def dummy_data_task():
    print("[DUMMY] Generator started")

    # Ensure DB + table exists
    init_db()

    conn = get_db()
    cur = conn.cursor()

    while True:
        try:
            # ---------------- EXISTING DB INSERT (UNCHANGED)
            total_set_output = random.uniform(90, 110)
            total_actual_output = random.uniform(90, 110)
            density = random.uniform(0.9, 1.0)
            gsm = random.uniform(40, 100)
            lay_flat = random.uniform(200, 250)

            cur.execute("""
                INSERT INTO machine_overview (
                    total_set_output,
                    total_actual_output,
                    density,
                    gsm,
                    lay_flat
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                total_set_output,
                total_actual_output,
                density,
                gsm,
                lay_flat
            ))

            conn.commit()
            print("[DUMMY] Machine overview inserted")

            # ---------------- NEW: LAYER LIVE DATA
            layer_data = get_live_layer_data()

            # ---------------- SOCKET EMIT (CENTRALIZED)
            socketio.emit("telemetry_update", {
                "total_set_output": total_set_output,
                "total_actual_output": total_actual_output,
                "density": density,
                "gsm": gsm,
                "lay_flat": lay_flat,

                "layers": layer_data
            })

            print("[DUMMY] Telemetry emitted")

            socketio.sleep(5)

        except Exception as e:
            print("[DUMMY] Error:", e)
            socketio.sleep(2)
