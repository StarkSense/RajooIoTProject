# print("LOADED telemetry_socket.py FROM:", __file__)

# from app.extensions import socketio
# from app.services.db_service import (
#     fetch_machine_overview,
#     fetch_series,
#     fetch_profile,
#     fetch_zonewise,
#     fetch_layer_kpis,
#     fetch_layer_trends,
#     fetch_winder_kpis,
#     fetch_winder_trends
# )

# # =========================================================
# # CONFIG
# # =========================================================
# WINDOW_SIZE = 30
# PROFILE_POINTS = 12
# MAP_POINTS = 9
# UPDATE_INTERVAL = 10
# LAYERS = [1, 2, 3]
# WINDERS = [1, 2]


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
# # BUILD LAYER PAYLOADS
# # =========================================================
# def build_layer_payload():
#     layer_data = {}
#     layer_trends = {}

#     for layer_id in LAYERS:
#         layer_data[f"layer{layer_id}"] = fetch_layer_kpis(layer_id)
#         layer_trends[f"layer{layer_id}"] = fetch_layer_trends(layer_id)

#     return layer_data, layer_trends

# # =========================================================
# # BUILD WINDER PAYLOADS
# # =========================================================
# def build_winder_payload():
#     winder_data = {}
#     winder_trends = {}

#     for winder_id in WINDERS:
#         winder_data[f"winder{winder_id}"] = fetch_winder_kpis(winder_id)
#         winder_trends[f"winder{winder_id}"] = fetch_winder_trends(winder_id)

#     return winder_data, winder_trends


# # =========================================================
# # TELEMETRY BACKGROUND LOOP
# # =========================================================
# def telemetry_task():
#     print("[SOCKET] Telemetry loop started")

#     while True:
#         try:
#             rows = fetch_machine_overview()
#             latest = rows[-1] if rows else {}

#             layer_data, layer_trends = build_layer_payload()
#             winder_data, winder_trends = build_winder_payload()


#             payload = {
#                 # -------------------------
#                 # EXISTING PAYLOAD 
#                 # -------------------------
#                 "machine_overview": {
#                     "total_set_output": round(latest.get("total_set_output", 0), 2),
#                     "total_actual_output": round(latest.get("total_actual_output", 0), 2),
#                     "density": round(latest.get("density", 0), 2),
#                     "gsm": round(latest.get("gsm", 0), 2),
#                     "lay_flat": round(latest.get("lay_flat", 0), 2),
#                 },

#                 "speed_trend": {
#                     "set": window(fetch_series("speed_set")),
#                     "actual": window(fetch_series("speed_actual"))
#                 },

#                 "ibc_temp": {
#                     "in": window(fetch_series("ibc_temp_in")),
#                     "out": window(fetch_series("ibc_temp_out"))
#                 },

#                 "lip_profile": latest_snapshot_per_index(
#                     fetch_profile("lip_profile")
#                 )[:PROFILE_POINTS],

#                 "map_profile": latest_snapshot_per_index(
#                     fetch_profile("map_profile")
#                 )[:MAP_POINTS],

#                 "die_temp_zones": [
#                     {
#                         "zone": f"Z{i + 1}",
#                         "set": 0,
#                         "actual": round(r["value"], 1)
#                     }
#                     for i, r in enumerate(fetch_zonewise("die_temp"))
#                 ],

#                 "thickness": {
#                     "trend": window(fetch_series("thickness_actual")),
#                     "stats": compute_thickness_stats(
#                         window(fetch_series("thickness_actual")),
#                         fetch_series("thickness_set"),
#                         fetch_series("gbr_position")
#                     )
#                 },

#                 # -------------------------
#                 #  LAYER DATA
#                 # -------------------------
#                 "layer_data": layer_data,
#                 "layer_trends": layer_trends,


#                 #-------------------------
#                 #  WINDER DATA (NEW)
#                 # -------------------------
#                 "winder_data": winder_data,
#                 "winder_trends": winder_trends
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
#     print("[SOCKET] Client connected – sending initial snapshot")

#     try:
        
#         layer_data, layer_trends = build_layer_payload()
#         winder_data, winder_trends = build_winder_payload()

#         rows = fetch_machine_overview()
#         latest = rows[-1] if rows else {}


#         payload = {
#             "machine_overview": latest,
#             "speed_trend": {
#                 "set": fetch_series("speed_set"),
#                 "actual": fetch_series("speed_actual")
#             },
#             "ibc_temp": {
#                 "in": fetch_series("ibc_temp_in"),
#                 "out": fetch_series("ibc_temp_out")
#             },
#             "lip_profile": fetch_profile("lip_profile"),
#             "map_profile": fetch_profile("map_profile"),
#             "die_temp_zones": [
#                 {
#                     "zone": f"Z{i + 1}",
#                     "set": 0,
#                     "actual": r["value"]
#                 }
#                 for i, r in enumerate(fetch_zonewise("die_temp"))
#             ],
#             "thickness": {
#                 "trend": fetch_series("thickness_actual"),
#                 "stats": compute_thickness_stats(
#                     fetch_series("thickness_actual"),
#                     fetch_series("thickness_set"),
#                     fetch_series("gbr_position")
#                 )
#             },
#             "layer_data": layer_data,
#             "layer_trends": layer_trends,

#             "winder_data": winder_data,
#             "winder_trends": winder_trends
#         }

#         socketio.emit("telemetry_update", payload)

#     except Exception as e:
#         print("[SOCKET] Initial snapshot error:", e)


# # =========================================================
# # STARTER
# # =========================================================
# def start_telemetry():
#     socketio.start_background_task(telemetry_task)



print("LOADED telemetry_socket.py FROM:", __file__)

import traceback
from flask import request

from app.extensions import socketio
from app.services.db_service import (
    fetch_machine_overview,
    fetch_series,
    fetch_profile,
    fetch_zonewise,
    fetch_layer_kpis,
    fetch_layer_trends,
    fetch_winder_kpis,
    fetch_winder_trends
)

# =========================================================
# CONFIG
# =========================================================
WINDOW_SIZE = 30
PROFILE_POINTS = 12
MAP_POINTS = 9
UPDATE_INTERVAL = 10  # seconds
LAYERS = [1, 2, 3]
WINDERS = [1, 2]

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
# BUILD LAYER PAYLOADS
# =========================================================
def build_layer_payload():
    layer_data = {}
    layer_trends = {}

    for layer_id in LAYERS:
        layer_data[f"layer{layer_id}"] = fetch_layer_kpis(layer_id)
        layer_trends[f"layer{layer_id}"] = fetch_layer_trends(layer_id)

    return layer_data, layer_trends

# =========================================================
# BUILD WINDER PAYLOADS
# =========================================================
def build_winder_payload():
    winder_data = {}
    winder_trends = {}

    for winder_id in WINDERS:
        winder_data[f"winder{winder_id}"] = fetch_winder_kpis(winder_id)
        winder_trends[f"winder{winder_id}"] = fetch_winder_trends(winder_id)

    return winder_data, winder_trends

# =========================================================
# TELEMETRY BACKGROUND LOOP
# (STARTED ONLY FROM run.py)
# =========================================================
def telemetry_task():
    print("[SOCKET] Telemetry loop started")

    while True:
        try:
            rows = fetch_machine_overview()
            latest = rows[-1] if rows else {}

            layer_data, layer_trends = build_layer_payload()
            winder_data, winder_trends = build_winder_payload()

            payload = {
                "machine_overview": {
                    "total_set_output": round(latest.get("total_set_output", 0), 2),
                    "total_actual_output": round(latest.get("total_actual_output", 0), 2),
                    "density": round(latest.get("density", 0), 2),
                    "gsm": round(latest.get("gsm", 0), 2),
                    "lay_flat": round(latest.get("lay_flat", 0), 2),
                },

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
                },

                "layer_data": layer_data,
                "layer_trends": layer_trends,

                "winder_data": winder_data,
                "winder_trends": winder_trends
            }

            # Emits to ALL connected clients (default behavior)
            socketio.emit("telemetry_update", payload)
            socketio.sleep(UPDATE_INTERVAL)

        except Exception:
            print("[SOCKET] Telemetry error:")
            print(traceback.format_exc())
            socketio.sleep(2)

# =========================================================
# SOCKET EVENTS
# =========================================================
@socketio.on("connect")
def on_connect():
    print("[SOCKET] Client connected:", request.sid)

    try:
        rows = fetch_machine_overview()
        latest = rows[-1] if rows else {}

        layer_data, layer_trends = build_layer_payload()
        winder_data, winder_trends = build_winder_payload()

        payload = {
            "machine_overview": latest,
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
            },
            "layer_data": layer_data,
            "layer_trends": layer_trends,
            "winder_data": winder_data,
            "winder_trends": winder_trends
        }

        # Initial snapshot ONLY for this client
        socketio.emit("telemetry_update", payload, room=request.sid)

    except Exception:
        print("[SOCKET] Initial snapshot error:")
        print(traceback.format_exc())
