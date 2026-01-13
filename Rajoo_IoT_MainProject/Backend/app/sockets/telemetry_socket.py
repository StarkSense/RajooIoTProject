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

# # ===============================
# # HISTORY BUFFERS
# # ===============================
# lip_profile = [{"x": i + 1, "y": 0.0} for i in range(LIP_POINTS)]

# ibc_temp_in = []
# ibc_temp_out = []

# # ✅ SET vs ACT SPEED
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


# def telemetry_task():
#     print("[SOCKET] Background telemetry thread started")

#     while True:
#         try:
#             payload = get_updates()
#             now = datetime.utcnow().strftime("%H:%M:%S")

#             # ===============================
#             # LIP PROFILE
#             # ===============================
#             for p in lip_profile:
#                 p["y"] = round(random.uniform(10.0, 18.0), 2)

#             # ===============================
#             # IBC TEMP IN / OUT
#             # ===============================
#             ibc_temp_in.append({
#                 "x": now,
#                 "y": round(random.uniform(75, 85), 2)
#             })
#             ibc_temp_out.append({
#                 "x": now,
#                 "y": round(random.uniform(70, 80), 2)
#             })

#             ibc_temp_in[:] = ibc_temp_in[-HISTORY_LIMIT:]
#             ibc_temp_out[:] = ibc_temp_out[-HISTORY_LIMIT:]

#             # ===============================
#             # SET vs ACT SPEED (LIVE)
#             # ===============================
#             speed_set.append({
#                 "x": now,
#                 "y": round(random.uniform(120, 150), 1)
#             })

#             speed_actual.append({
#                 "x": now,
#                 "y": round(random.uniform(115, 145), 1)
#             })

#             speed_set[:] = speed_set[-HISTORY_LIMIT:]
#             speed_actual[:] = speed_actual[-HISTORY_LIMIT:]

#             # ===============================
#             # DIE TEMP ZONE WISE
#             # ===============================
#             for z in die_temp_zones:
#                 z["set"] = round(random.uniform(170, 185), 1)
#                 z["actual"] = round(z["set"] - random.uniform(1, 5), 1)

#             # ===============================
#             # MAP PROFILE
#             # ===============================
#             for p in map_profile:
#                 p["y"] = round(random.uniform(15, 25), 1)

#             # ===============================
#             # THICKNESS
#             # ===============================
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
#             # FINAL PAYLOAD CONTRACT
#             # ===============================
#             payload.update({
#                 "lip_profile": lip_profile,

#                 "ibc_temp": {
#                     "in": ibc_temp_in,
#                     "out": ibc_temp_out
#                 },

#                 "speed_trend": {
#                     "set": speed_set,
#                     "actual": speed_actual
#                 },

#                 "die_temp_zones": die_temp_zones,

#                 "map_profile": map_profile,

#                 "thickness": {
#                     "trend": thickness_trend,
#                     "stats": thickness_stats
#                 }
#             })

#             # Emit for all listeners
#             socketio.emit("telemetry_update", payload, namespace=NAMESPACE)
#             socketio.emit("telemetry_update", payload)

#             socketio.sleep(5)

#         except Exception as e:
#             print("[SOCKET] Error:", e)
#             socketio.sleep(2)


import random
from datetime import datetime

from app.extensions import socketio
from app.services.db_service import get_updates

NAMESPACE = "/telemetry"

# ===============================
# CONFIG
# ===============================
LIP_POINTS = 12
DIE_ZONES = 6
HISTORY_LIMIT = 20
LAYERS = ["layer1", "layer2", "layer3"]

# ===============================
# DASHBOARD HISTORY BUFFERS
# ===============================
lip_profile = [{"x": i + 1, "y": 0.0} for i in range(LIP_POINTS)]

ibc_temp_in = []
ibc_temp_out = []

speed_set = []
speed_actual = []

die_temp_zones = [
    {"zone": f"Z{i+1}", "set": 0.0, "actual": 0.0}
    for i in range(DIE_ZONES)
]

map_profile = [{"x": i * 10, "y": 0.0} for i in range(10)]

thickness_trend = []
thickness_stats = {
    "set": 18.0,
    "avg": 0.0,
    "nominal": 18.0,
    "max": 0.0,
    "min": 0.0,
    "gbr": 100
}

# ===============================
# 🔥 LAYER-SPECIFIC BUFFERS
# ===============================
layer_buffers = {
    layer: {
        "speed": 0.0,
        "yield": 0.0,
        "ampere": 0.0,

        "melt_pressure": [],
        "melt_temperature": [],
        "thickness": {
            "set": [],
            "actual": []
        }
    }
    for layer in LAYERS
}


# ===============================
# TELEMETRY LOOP
# ===============================
def telemetry_task():
    print("[SOCKET] Background telemetry thread started")

    while True:
        try:
            payload = get_updates()
            now = datetime.utcnow().strftime("%H:%M:%S")

            # ===============================
            # DASHBOARD DATA (UNCHANGED)
            # ===============================
            for p in lip_profile:
                p["y"] = round(random.uniform(10.0, 18.0), 2)

            ibc_temp_in.append({"x": now, "y": round(random.uniform(75, 85), 2)})
            ibc_temp_out.append({"x": now, "y": round(random.uniform(70, 80), 2)})

            ibc_temp_in[:] = ibc_temp_in[-HISTORY_LIMIT:]
            ibc_temp_out[:] = ibc_temp_out[-HISTORY_LIMIT:]

            speed_set.append({"x": now, "y": round(random.uniform(120, 150), 1)})
            speed_actual.append({"x": now, "y": round(random.uniform(115, 145), 1)})

            speed_set[:] = speed_set[-HISTORY_LIMIT:]
            speed_actual[:] = speed_actual[-HISTORY_LIMIT:]

            for z in die_temp_zones:
                z["set"] = round(random.uniform(170, 185), 1)
                z["actual"] = round(z["set"] - random.uniform(1, 5), 1)

            for p in map_profile:
                p["y"] = round(random.uniform(15, 25), 1)

            t = round(random.uniform(17.5, 18.8), 2)
            thickness_trend.append({"x": now, "y": t})
            thickness_trend[:] = thickness_trend[-HISTORY_LIMIT:]

            thickness_stats["avg"] = round(
                sum(v["y"] for v in thickness_trend) / len(thickness_trend), 2
            )
            thickness_stats["max"] = max(v["y"] for v in thickness_trend)
            thickness_stats["min"] = min(v["y"] for v in thickness_trend)
            thickness_stats["gbr"] = random.randint(90, 110)

            # ===============================
            # 🔥 LAYER DATA (NEW)
            # ===============================
            layers_payload = {}

            for layer in LAYERS:
                buf = layer_buffers[layer]

                buf["speed"] = round(random.uniform(180, 260), 1)
                buf["yield"] = round(random.uniform(85, 98), 1)
                buf["ampere"] = round(random.uniform(30, 65), 1)

                buf["melt_pressure"].append({
                    "x": now,
                    "y": round(random.uniform(140, 210), 1)
                })

                buf["melt_temperature"].append({
                    "x": now,
                    "y": round(random.uniform(180, 230), 1)
                })

                buf["thickness"]["set"].append({
                    "x": now,
                    "y": round(random.uniform(18.0, 18.5), 2)
                })

                buf["thickness"]["actual"].append({
                    "x": now,
                    "y": round(random.uniform(17.5, 18.8), 2)
                })

                # Trim history
                buf["melt_pressure"][:] = buf["melt_pressure"][-HISTORY_LIMIT:]
                buf["melt_temperature"][:] = buf["melt_temperature"][-HISTORY_LIMIT:]
                buf["thickness"]["set"][:] = buf["thickness"]["set"][-HISTORY_LIMIT:]
                buf["thickness"]["actual"][:] = buf["thickness"]["actual"][-HISTORY_LIMIT:]

                layers_payload[layer] = buf

            # ===============================
            # FINAL PAYLOAD
            # ===============================
            payload.update({
                "lip_profile": lip_profile,
                "ibc_temp": {"in": ibc_temp_in, "out": ibc_temp_out},
                "speed_trend": {"set": speed_set, "actual": speed_actual},
                "die_temp_zones": die_temp_zones,
                "map_profile": map_profile,
                "thickness": {
                    "trend": thickness_trend,
                    "stats": thickness_stats
                },
                "layers": layers_payload
            })

            socketio.emit("telemetry_update", payload, namespace=NAMESPACE)
            socketio.emit("telemetry_update", payload)

            socketio.sleep(5)

        except Exception as e:
            print("[SOCKET] Error:", e)
            socketio.sleep(2)
