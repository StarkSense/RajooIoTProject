
# print("LOADED telemetry_socket.py FROM:", __file__)

# from app.extensions import socketio
# from app.services.db_service import (
#     fetch_machine_overview,
#     fetch_series,
#     fetch_profile,
#     fetch_zonewise
# )

# # =========================================================
# # CONFIG
# # =========================================================
# WINDOW_SIZE = 30
# PROFILE_POINTS = 12
# MAP_POINTS = 9
# UPDATE_INTERVAL = 10


# # =========================================================
# # HELPERS
# # =========================================================
# def window(series, size=WINDOW_SIZE):
#     return series[-size:] if len(series) > size else series


# def latest_snapshot_per_index(rows):
#     latest = {}
#     for r in rows:
#         idx = r.get("x", r.get("index_no"))
#         val = r.get("y", r.get("value"))
#         latest[idx] = val

#     return [{"x": k, "y": v} for k, v in sorted(latest.items())]


# def compute_thickness_stats(actual, thickness_set, gbr_series):
#     if not actual:
#         return {
#             "set": 0,
#             "avg": 0,
#             "min": 0,
#             "max": 0,
#             "nominal": 18,
#             "gbr": 0
#         }

#     return {
#         "set": thickness_set[-1] if thickness_set else 18,
#         "avg": round(sum(actual) / len(actual), 2),
#         "min": round(min(actual), 2),
#         "max": round(max(actual), 2),
#         "nominal": 18,
#         "gbr": gbr_series[-1] if gbr_series else 0
#     }


# # =========================================================
# # TELEMETRY LOOP (STARTED ONCE)
# # =========================================================
# def telemetry_task():
#     print("[SOCKET] Telemetry loop started")

#     while True:
#         try:
#             machine_rows = fetch_machine_overview()
#             latest_machine = machine_rows[-1] if machine_rows else {}

#             machine_overview = {
#                 "total_set_output": round(latest_machine.get("total_set_output", 0), 2),
#                 "total_actual_output": round(latest_machine.get("total_actual_output", 0), 2),
#                 "density": round(latest_machine.get("density", 0), 2),
#                 "gsm": round(latest_machine.get("gsm", 0), 2),
#                 "lay_flat": round(latest_machine.get("lay_flat", 0), 2),
#             }

#             speed_set = window(fetch_series("speed_set"))
#             speed_actual = window(fetch_series("speed_actual"))

#             ibc_temp_in = window(fetch_series("ibc_temp_in"))
#             ibc_temp_out = window(fetch_series("ibc_temp_out"))

#             lip_profile = latest_snapshot_per_index(
#                 fetch_profile("lip_profile")
#             )[:PROFILE_POINTS]

#             map_profile = latest_snapshot_per_index(
#                 fetch_profile("map_profile")
#             )[:MAP_POINTS]

#             die_temp_zones = [
#                 {
#                     "zone": f"Z{i + 1}",
#                     "set": 0,
#                     "actual": round(r["value"], 1)
#                 }
#                 for i, r in enumerate(fetch_zonewise("die_temp"))
#             ]

#             thickness_actual = window(fetch_series("thickness_actual"))
#             thickness_set = fetch_series("thickness_set")
#             gbr_series = fetch_series("gbr_position")

#             thickness_stats = compute_thickness_stats(
#                 thickness_actual,
#                 thickness_set,
#                 gbr_series
#             )

#             payload = {
#                 "machine_overview": machine_overview,
#                 "lip_profile": lip_profile,
#                 "map_profile": map_profile,
#                 "speed_trend": {
#                     "set": speed_set,
#                     "actual": speed_actual
#                 },
#                 "ibc_temp": {
#                     "in": ibc_temp_in,
#                     "out": ibc_temp_out
#                 },
#                 "die_temp_zones": die_temp_zones,
#                 "thickness": {
#                     "trend": thickness_actual,
#                     "stats": thickness_stats
#                 }
#             }

#             socketio.emit("telemetry_update", payload)
#             socketio.sleep(UPDATE_INTERVAL)

#         except Exception as e:
#             print("[SOCKET] Telemetry error:", e)
#             socketio.sleep(2)


# # =========================================================
# # SOCKET EVENTS
# # =========================================================
# @socketio.on("connect")
# def on_connect():
#     print("[SOCKET] Client connected")


# # =========================================================
# # START TASK FROM run.py
# # =========================================================
# def start_telemetry():
#     socketio.start_background_task(telemetry_task)



print("LOADED telemetry_socket.py FROM:", __file__)

from app.extensions import socketio
from app.services.db_service import (
    fetch_machine_overview,
    fetch_series,
    fetch_profile,
    fetch_zonewise
)

# =========================================================
# CONFIG
# =========================================================
WINDOW_SIZE = 30
PROFILE_POINTS = 12
MAP_POINTS = 9
UPDATE_INTERVAL = 10


# =========================================================
# HELPERS
# =========================================================
def window(series, size=WINDOW_SIZE):
    return series[-size:] if len(series) > size else series


def latest_snapshot_per_index(rows):
    latest = {}
    for r in rows:
        idx = r.get("x", r.get("index_no"))
        val = r.get("y", r.get("value"))
        latest[idx] = val
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
# TELEMETRY BACKGROUND LOOP (UNCHANGED)
# =========================================================
def telemetry_task():
    print("[SOCKET] Telemetry loop started")

    while True:
        try:
            rows = fetch_machine_overview()
            latest = rows[-1] if rows else {}

            machine_overview = {
                "total_set_output": round(latest.get("total_set_output", 0), 2),
                "total_actual_output": round(latest.get("total_actual_output", 0), 2),
                "density": round(latest.get("density", 0), 2),
                "gsm": round(latest.get("gsm", 0), 2),
                "lay_flat": round(latest.get("lay_flat", 0), 2),
            }

            payload = {
                "machine_overview": machine_overview,
                "speed_trend": {
                    "set": window(fetch_series("speed_set")),
                    "actual": window(fetch_series("speed_actual"))
                },
                "ibc_temp": {
                    "in": window(fetch_series("ibc_temp_in")),
                    "out": window(fetch_series("ibc_temp_out"))
                },
                "lip_profile": latest_snapshot_per_index(
                    fetch_profile("lip_profile")
                )[:PROFILE_POINTS],
                "map_profile": latest_snapshot_per_index(
                    fetch_profile("map_profile")
                )[:MAP_POINTS],
                "die_temp_zones": [
                    {
                        "zone": f"Z{i + 1}",
                        "set": 0,
                        "actual": round(r["value"], 1)
                    }
                    for i, r in enumerate(fetch_zonewise("die_temp"))
                ],
                "thickness": {
                    "trend": window(fetch_series("thickness_actual")),
                    "stats": compute_thickness_stats(
                        window(fetch_series("thickness_actual")),
                        fetch_series("thickness_set"),
                        fetch_series("gbr_position")
                    )
                }
            }

            socketio.emit("telemetry_update", payload)
            socketio.sleep(UPDATE_INTERVAL)

        except Exception as e:
            print("[SOCKET] Telemetry error:", e)
            socketio.sleep(2)


# =========================================================
# SOCKET EVENTS (FIXED – SNAPSHOT ON CONNECT)
# =========================================================
@socketio.on("connect")
def on_connect():
    print("[SOCKET] Client connected – sending initial snapshot")

    try:
        rows = fetch_machine_overview()
        latest = rows[-1] if rows else {}

        payload = {
            "machine_overview": {
                "total_set_output": latest.get("total_set_output", 0),
                "total_actual_output": latest.get("total_actual_output", 0),
                "density": latest.get("density", 0),
                "gsm": latest.get("gsm", 0),
                "lay_flat": latest.get("lay_flat", 0),
            },
            "speed_trend": {
                "set": fetch_series("speed_set"),
                "actual": fetch_series("speed_actual")
            },
            "ibc_temp": {
                "in": fetch_series("ibc_temp_in"),
                "out": fetch_series("ibc_temp_out")
            },
            "lip_profile": fetch_profile("lip_profile"),
            "map_profile": fetch_profile("map_profile"),
            "die_temp_zones": [
                {
                    "zone": f"Z{i + 1}",
                    "set": 0,
                    "actual": r["value"]
                }
                for i, r in enumerate(fetch_zonewise("die_temp"))
            ],
            "thickness": {
                "trend": fetch_series("thickness_actual"),
                "stats": compute_thickness_stats(
                    fetch_series("thickness_actual"),
                    fetch_series("thickness_set"),
                    fetch_series("gbr_position")
                )
            }
        }

        socketio.emit("telemetry_update", payload)

    except Exception as e:
        print("[SOCKET] Initial snapshot error:", e)
