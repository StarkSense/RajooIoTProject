
# import random
# from datetime import datetime

# from app.extensions import socketio
# from app.services.db_service import get_updates

# NAMESPACE = "/telemetry"

# # ===============================
# # CONFIG
# # ===============================
# LIP_POINTS = 12
# DIE_ZONES = 6
# HISTORY_LIMIT = 20
# LAYERS = ["layer1", "layer2", "layer3"]

# # ===============================
# # DASHBOARD HISTORY BUFFERS
# # ===============================
# lip_profile = [{"x": i + 1, "y": 0.0} for i in range(LIP_POINTS)]

# ibc_temp_in = []
# ibc_temp_out = []

# speed_set = []
# speed_actual = []

# die_temp_zones = [
#     {"zone": f"Z{i+1}", "set": 0.0, "actual": 0.0}
#     for i in range(DIE_ZONES)
# ]

# map_profile = [{"x": i * 10, "y": 0.0} for i in range(10)]

# thickness_trend = []
# thickness_stats = {
#     "set": 18.0,
#     "avg": 0.0,
#     "nominal": 18.0,
#     "max": 0.0,
#     "min": 0.0,
#     "gbr": 100
# }

# # ===============================
# # 🔥 LAYER-SPECIFIC BUFFERS
# # ===============================
# layer_buffers = {
#     layer: {
#         "speed": 0.0,
#         "yield": 0.0,
#         "ampere": 0.0,

#         "melt_pressure": [],
#         "melt_temperature": [],
#         "thickness": {
#             "set": [],
#             "actual": []
#         }
#     }
#     for layer in LAYERS
# }


# # ===============================
# # TELEMETRY LOOP
# # ===============================
# def telemetry_task():
#     print("[SOCKET] Background telemetry thread started")

#     while True:
#         try:
#             payload = get_updates()
#             now = datetime.utcnow().strftime("%H:%M:%S")

#             # ===============================
#             # DASHBOARD DATA (UNCHANGED)
#             # ===============================
#             for p in lip_profile:
#                 p["y"] = round(random.uniform(10.0, 18.0), 2)

#             ibc_temp_in.append({"x": now, "y": round(random.uniform(75, 85), 2)})
#             ibc_temp_out.append({"x": now, "y": round(random.uniform(70, 80), 2)})

#             ibc_temp_in[:] = ibc_temp_in[-HISTORY_LIMIT:]
#             ibc_temp_out[:] = ibc_temp_out[-HISTORY_LIMIT:]

#             speed_set.append({"x": now, "y": round(random.uniform(120, 150), 1)})
#             speed_actual.append({"x": now, "y": round(random.uniform(115, 145), 1)})

#             speed_set[:] = speed_set[-HISTORY_LIMIT:]
#             speed_actual[:] = speed_actual[-HISTORY_LIMIT:]

#             for z in die_temp_zones:
#                 z["set"] = round(random.uniform(170, 185), 1)
#                 z["actual"] = round(z["set"] - random.uniform(1, 5), 1)

#             for p in map_profile:
#                 p["y"] = round(random.uniform(15, 25), 1)

#             t = round(random.uniform(17.5, 18.8), 2)
#             thickness_trend.append({"x": now, "y": t})
#             thickness_trend[:] = thickness_trend[-HISTORY_LIMIT:]

#             thickness_stats["avg"] = round(
#                 sum(v["y"] for v in thickness_trend) / len(thickness_trend), 2
#             )
#             thickness_stats["max"] = max(v["y"] for v in thickness_trend)
#             thickness_stats["min"] = min(v["y"] for v in thickness_trend)
#             thickness_stats["gbr"] = random.randint(90, 110)

#             # ===============================
#             # 🔥 LAYER DATA (NEW)
#             # ===============================
#             layers_payload = {}

#             for layer in LAYERS:
#                 buf = layer_buffers[layer]

#                 buf["speed"] = round(random.uniform(180, 260), 1)
#                 buf["yield"] = round(random.uniform(85, 98), 1)
#                 buf["ampere"] = round(random.uniform(30, 65), 1)

#                 buf["melt_pressure"].append({
#                     "x": now,
#                     "y": round(random.uniform(140, 210), 1)
#                 })

#                 buf["melt_temperature"].append({
#                     "x": now,
#                     "y": round(random.uniform(180, 230), 1)
#                 })

#                 buf["thickness"]["set"].append({
#                     "x": now,
#                     "y": round(random.uniform(18.0, 18.5), 2)
#                 })

#                 buf["thickness"]["actual"].append({
#                     "x": now,
#                     "y": round(random.uniform(17.5, 18.8), 2)
#                 })

#                 # Trim history
#                 buf["melt_pressure"][:] = buf["melt_pressure"][-HISTORY_LIMIT:]
#                 buf["melt_temperature"][:] = buf["melt_temperature"][-HISTORY_LIMIT:]
#                 buf["thickness"]["set"][:] = buf["thickness"]["set"][-HISTORY_LIMIT:]
#                 buf["thickness"]["actual"][:] = buf["thickness"]["actual"][-HISTORY_LIMIT:]

#                 layers_payload[layer] = buf

#             # ===============================
#             # FINAL PAYLOAD
#             # ===============================
#             payload.update({
#                 "lip_profile": lip_profile,
#                 "ibc_temp": {"in": ibc_temp_in, "out": ibc_temp_out},
#                 "speed_trend": {"set": speed_set, "actual": speed_actual},
#                 "die_temp_zones": die_temp_zones,
#                 "map_profile": map_profile,
#                 "thickness": {
#                     "trend": thickness_trend,
#                     "stats": thickness_stats
#                 },
#                 "layers": layers_payload
#             })

#             socketio.emit("telemetry_update", payload, namespace=NAMESPACE)
#             socketio.emit("telemetry_update", payload)

#             socketio.sleep(5)

#         except Exception as e:
#             print("[SOCKET] Error:", e)
#             socketio.sleep(2)



print("LOADED telemetry_socket.py FROM:", __file__)

from app.extensions import socketio
from app.services.db_service import (
    fetch_machine_overview,
    fetch_series,
    fetch_profile,
    fetch_zonewise
)

# =========================================================
# CONFIG (TUNE THESE FOR YOUR DASHBOARD)
# =========================================================
WINDOW_SIZE = 30        # points for time-series graphs
PROFILE_POINTS = 12    # lip profile points (die width sections)
MAP_POINTS = 9          # map profile points


# =========================================================
# HELPER FUNCTIONS (THIS IS THE MAGIC)
# =========================================================

def window(series, size=WINDOW_SIZE):
    """Return last N points (for smooth graphs)"""
    return series[-size:] if len(series) > size else series


def latest_snapshot_per_index(rows):
    """
    Convert historical profile rows into a SINGLE snapshot:
    latest value per index_no
    """
    latest = {}
    for r in rows:
        idx = r["x"] if "x" in r else r["index_no"]
        latest[idx] = r["y"] if "y" in r else r["value"]

    return [{"x": k, "y": v} for k, v in sorted(latest.items())]


def compute_thickness_stats(actual, thickness_set, gbr_series):
    if not actual:
        return {
            "set": 0,
            "avg": 0,
            "min": 0,
            "max": 0,
            "nominal": 18,
            "gbr": 0
        }

    return {
        "set": thickness_set[-1] if thickness_set else 18,
        "avg": round(sum(actual) / len(actual), 2),
        "min": round(min(actual), 2),
        "max": round(max(actual), 2),
        "nominal": 18,
        "gbr": gbr_series[-1] if gbr_series else 0
    }


# =========================================================
# SOCKET.IO TELEMETRY
# =========================================================

telemetry_started = False


@socketio.on("connect")
def on_connect():
    global telemetry_started
    print("[SOCKET] Client connected")

    if not telemetry_started:
        print("[SOCKET] Starting telemetry task")
        socketio.start_background_task(telemetry_task)
        telemetry_started = True


def telemetry_task():
    print("[SOCKET] Telemetry started")

    while True:
        try:
            # =====================================================
            # MACHINE OVERVIEW (TOP KPI CARDS)
            # =====================================================
            machine_rows = fetch_machine_overview()
            latest_machine = machine_rows[-1] if machine_rows else {
                "total_set_output": 0,
                "total_actual_output": 0,
                "density": 0,
                "gsm": 0,
                "lay_flat": 0
            }

            machine_overview = {
                "total_set_output": round(latest_machine.get("total_set_output", 0), 2),
                "total_actual_output": round(latest_machine.get("total_actual_output", 0), 2),
                "density": round(latest_machine.get("density", 0), 2),
                "gsm": round(latest_machine.get("gsm", 0), 2),
                "lay_flat": round(latest_machine.get("lay_flat", 0), 2)
            }

            # =====================================================
            # SPEED (SET vs ACTUAL)
            # =====================================================
            speed_set = window(fetch_series("speed_set"))
            speed_actual = window(fetch_series("speed_actual"))

            # =====================================================
            # IBC TEMPERATURE (IN / OUT)
            # =====================================================
            ibc_temp_in = window(fetch_series("ibc_temp_in"))
            ibc_temp_out = window(fetch_series("ibc_temp_out"))

            # =====================================================
            # LIP PROFILE (SNAPSHOT – NOT HISTORY)
            # =====================================================
            lip_raw = fetch_profile("lip_profile")
            lip_profile = latest_snapshot_per_index(lip_raw)[:PROFILE_POINTS]

            # =====================================================
            # MAP PROFILE (SNAPSHOT – NOT HISTORY)
            # =====================================================
            map_raw = fetch_profile("map_profile")
            map_profile = latest_snapshot_per_index(map_raw)[:MAP_POINTS]

            # =====================================================
            # DIE TEMPERATURE ZONE WISE
            # =====================================================
            die_rows = fetch_zonewise("die_temp")
            die_temp_zones = []

            for i, r in enumerate(die_rows):
                die_temp_zones.append({
                    "zone": f"Z{i + 1}",
                    "set": 0,                  # OPC-UA setpoint can come later
                    "actual": round(r["value"], 1)
                })

            # =====================================================
            # THICKNESS (TREND + STATS)
            # =====================================================
            thickness_actual = window(fetch_series("thickness_actual"))
            thickness_set = fetch_series("thickness_set")
            gbr_series = fetch_series("gbr_position")

            thickness_stats = compute_thickness_stats(
                thickness_actual,
                thickness_set,
                gbr_series
            )

            # =====================================================
            # FINAL DASHBOARD PAYLOAD 
            # =====================================================
            payload = {
                "machine_overview": machine_overview,

                "lip_profile": lip_profile,
                "map_profile": map_profile,

                "speed_trend": {
                    "set": speed_set,
                    "actual": speed_actual
                },

                "ibc_temp": {
                    "in": ibc_temp_in,
                    "out": ibc_temp_out
                },

                "die_temp_zones": die_temp_zones,

                "thickness": {
                    "trend": thickness_actual,
                    "stats": thickness_stats
                }
            }

            socketio.emit("telemetry_update", payload)
            socketio.sleep(10)

        except Exception as e:
            print("[SOCKET] Telemetry error:", e)
            socketio.sleep(2)
