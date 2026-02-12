import time
from math import sin
from app.services.db_service import (
    init_db,
    get_db,
    insert_machine_overview,
    insert_timeseries
)

# =========================================================
# CONFIG
# =========================================================
UPDATE_INTERVAL = 10
DIE_ZONES = 7         
LIP_POINTS = 12
MAP_POINTS = 9
LAYERS = 3

# =========================================================
# MACHINE STATE
# =========================================================
machine = {
    "total_set_output": 96.0,
    "total_actual_output": 94.0,
    "density": 0.92,
    "gsm": 76.0,
    "lay_flat": 226.0
}

speed_set = 140.0
speed_actual = 138.0
thickness_set = 18.0
gbr_position = 107
tick = 0

# =========================================================
# LAYER STATE
# =========================================================
layers = {
    1: {"speed": 50.0, "yield": 30.0, "ampere": 12.0, "melt_pressure": 180.0, "melt_temperature": 220.0, "thickness_set": 6.0, "thickness_actual": 5.8},
    2: {"speed": 55.0, "yield": 32.0, "ampere": 13.0, "melt_pressure": 185.0, "melt_temperature": 225.0, "thickness_set": 6.0, "thickness_actual": 5.9},
    3: {"speed": 60.0, "yield": 34.0, "ampere": 14.0, "melt_pressure": 190.0, "melt_temperature": 230.0, "thickness_set": 6.0, "thickness_actual": 6.0}
}

# =========================================================
# WINDER STATE
# =========================================================
winders = {
    1: {"totalizer": 1200.0, "roll_length": 250.0, "roll_dia": 600.0},
    2: {"totalizer": 1180.0, "roll_length": 240.0, "roll_dia": 590.0}
}

# =========================================================
# EXTRUDER STATE
# =========================================================
EXTRUDER_MATERIALS = {
    "F18010": {"set_pct": 85, "set_kg": 2.55, "density": 0.920},
    "LD":     {"set_pct": 0,  "set_kg": 0.00, "density": 0.920},
    "F19010": {"set_pct": 0,  "set_kg": 0.00, "density": 0.920},
    "PPA705": {"set_pct": 15, "set_kg": 0.45, "density": 0.920},
    "MLLD":   {"set_pct": 0,  "set_kg": 0.00, "density": 0.915}
}

EXTRUDER_TEMP_ZONES = {
    "BZ-1": 100,
    "BZ-3": 90,
    "ADP": 85,
    "AD1": 100
}

extruders = {
    "A": {"tick": 0},
    "B": {"tick": 0},
    "C": {"tick": 0}
}

# =========================================================
# DUMMY DATA TASK
# =========================================================
def dummy_data_task():
    global tick
    init_db()
    print("[DUMMY] Dummy data provider started")

    while True:
        tick += 1

        # ================= MACHINE OVERVIEW =================
        machine["total_set_output"] += 1
        machine["total_actual_output"] += 1
        machine["density"] = round(0.92 + sin(tick / 10) * 0.005, 3)
        machine["gsm"] = round(76 + sin(tick / 8), 2)
        machine["lay_flat"] = round(226 + sin(tick / 6) * 2, 2)
        insert_machine_overview(machine)

        insert_timeseries("speed_set", round(speed_set + sin(tick / 5) * 3, 2))
        insert_timeseries("speed_actual", round(speed_actual + sin(tick / 6) * 3, 2))

        insert_timeseries("thickness_set", thickness_set)
        insert_timeseries("thickness_actual", round(thickness_set + sin(tick / 7) * 0.6, 2))
        insert_timeseries("gbr_position", gbr_position + tick % 5)

        # ================= IBC TEMP IN / OUT  =================
        insert_timeseries(
            "ibc_temp_in",
            round(32 + sin(tick / 6) * 2, 2)
        )

        insert_timeseries(
            "ibc_temp_out",
            round(34 + sin(tick / 7) * 2, 2)
        )

        # ================= LIP PROFILE =================
        for i in range(1, LIP_POINTS + 1):
            insert_timeseries(
                "lip_profile",
                round(18 + sin((tick + i) / 4) * 0.8, 2),
                index_no=i
            )

        # ================= MAP PROFILE =================
        for i in range(1, MAP_POINTS + 1):
            insert_timeseries(
                "map_profile",
                round(18 + sin((tick + i) / 5) * 0.6, 2),
                index_no=i
            )

        # ================= DIE TEMP ZONES (Z1–Z7 ONLY) =================
        conn = get_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM machine_timeseries WHERE tag = 'die_temp'")

        for z in range(1, DIE_ZONES + 1):
            cur.execute(
                """
                INSERT INTO machine_timeseries (tag, value, index_no)
                VALUES (?, ?, ?)
                """,
                (
                    "die_temp",
                    round(210 + sin((tick + z) / 3) * 4, 1),
                    z
                )
            )

        conn.commit()
        conn.close()

        # ================= LAYERS =================
        for lid, data in layers.items():
            insert_timeseries(f"layer_{lid}_speed", data["speed"] + tick)
            insert_timeseries(f"layer_{lid}_yield", data["yield"] + tick)
            insert_timeseries(f"layer_{lid}_ampere", data["ampere"] + tick)

            insert_timeseries(f"layer_{lid}_melt_pressure", data["melt_pressure"] + tick)
            insert_timeseries(f"layer_{lid}_melt_temperature", data["melt_temperature"] + tick)
            insert_timeseries(f"layer_{lid}_thickness_set", data["thickness_set"])
            insert_timeseries(
                f"layer_{lid}_thickness_set",
                data["thickness_set"]
            )

            insert_timeseries(
                f"layer_{lid}_thickness_actual",
                round(data["thickness_set"] + sin((tick + lid) / 6) * 0.25, 2)
            )

        # ================= WINDERS =================
        for wid, data in winders.items():
            insert_timeseries(f"winder_{wid}_totalizer", data["totalizer"] + tick)
            insert_timeseries(f"winder_{wid}_roll_length", data["roll_length"] + tick)
            insert_timeseries(f"winder_{wid}_roll_dia", data["roll_dia"] + tick)

        # ================= EXTRUDERS =================
        for ext_id in extruders:
            extruders[ext_id]["tick"] += 1
            t = extruders[ext_id]["tick"]

            total_set = 0
            total_act = 0

            for mat, cfg in EXTRUDER_MATERIALS.items():
                act_pct = round(cfg["set_pct"] + sin(t / 6) * 1.5, 2)
                act_kg = round(cfg["set_kg"] + sin(t / 5) * 0.05, 3)
                density = round(cfg["density"] + sin(t / 10) * 0.0005, 4)

                insert_timeseries(f"extruder_{ext_id}_material_{mat}_set_pct", cfg["set_pct"])
                insert_timeseries(f"extruder_{ext_id}_material_{mat}_act_pct", act_pct)
                insert_timeseries(f"extruder_{ext_id}_material_{mat}_set_kg", cfg["set_kg"])
                insert_timeseries(f"extruder_{ext_id}_material_{mat}_act_kg", act_kg)
                insert_timeseries(f"extruder_{ext_id}_material_{mat}_density", density)

                total_set += cfg["set_kg"]
                total_act += act_kg

            insert_timeseries(f"extruder_{ext_id}_total_set_kg", round(total_set, 2))
            insert_timeseries(f"extruder_{ext_id}_total_act_kg", round(total_act, 2))

            for zone, base in EXTRUDER_TEMP_ZONES.items():
                insert_timeseries(f"extruder_{ext_id}_temp_{zone}_set", base)
                insert_timeseries(
                    f"extruder_{ext_id}_temp_{zone}_act",
                    round(base + sin((t + len(zone)) / 4) * 3, 1)
                )

        time.sleep(UPDATE_INTERVAL)
