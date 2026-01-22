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
# PERSISTENT MACHINE STATE 
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
    1: {
        "speed": 50.0,
        "yield": 30.0,
        "ampere": 12.0,
        "melt_pressure": 180.0,
        "melt_temperature": 220.0,
        "thickness_set": 6.0,
        "thickness_actual": 5.8
    },
    2: {
        "speed": 55.0,
        "yield": 32.0,
        "ampere": 13.0,
        "melt_pressure": 185.0,
        "melt_temperature": 225.0,
        "thickness_set": 6.0,
        "thickness_actual": 5.9
    },
    3: {
        "speed": 60.0,
        "yield": 34.0,
        "ampere": 14.0,
        "melt_pressure": 190.0,
        "melt_temperature": 230.0,
        "thickness_set": 6.0,
        "thickness_actual": 6.0
    }
}

# =========================================================
# WINDER STATE 
# =========================================================
winders = {
    1: {
        "totalizer": 1200.0,
        "roll_length": 250.0,
        "roll_dia": 600.0
    },
    2: {
        "totalizer": 1180.0,
        "roll_length": 240.0,
        "roll_dia": 590.0
    }
}


# =========================================================
# UTILITY 
# =========================================================
def clear_tag(tag):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM machine_timeseries WHERE tag = ?", (tag,))
    conn.commit()
    conn.close()

# =========================================================
# DUMMY DATA TASK
# =========================================================
def dummy_data_task():
    global tick
    init_db()

    print("[DUMMY] Deterministic dummy with layer data started")

    while True:
        tick += 1

        # =====================================================
        # MACHINE OVERVIEW 
        # =====================================================
        machine["total_set_output"] += 1
        machine["total_actual_output"] += 1
        machine["density"] = round(0.92 + 0.005 * sin(tick / 10), 3)
        machine["gsm"] = round(76 + sin(tick / 8), 2)
        machine["lay_flat"] = round(226 + sin(tick / 6) * 2, 2)

        insert_machine_overview(machine)

        # =====================================================
        # SPEED 
        # =====================================================
        insert_timeseries("speed_set", round(speed_set + sin(tick / 5) * 3, 2))
        insert_timeseries("speed_actual", round(speed_actual + sin(tick / 6) * 3, 2))

        # =====================================================
        # IBC TEMP 
        # =====================================================
        insert_timeseries("ibc_temp_in", round(82 + sin(tick / 4) * 2, 2))
        insert_timeseries("ibc_temp_out", round(78 + sin(tick / 5) * 2, 2))

        # =====================================================
        # THICKNESS 
        # =====================================================
        actual_thickness = round(thickness_set + sin(tick / 7) * 0.6, 2)
        insert_timeseries("thickness_set", thickness_set)
        insert_timeseries("thickness_actual", actual_thickness)
        insert_timeseries("gbr_position", gbr_position + tick % 5)

        # =====================================================
        # DIE TEMP ZONES 
        # =====================================================
        clear_tag("die_temp")
        for i in range(DIE_ZONES):
            insert_timeseries(
                "die_temp",
                round(172 + i + sin((tick + i) / 6) * 2, 1),
                index_no=i + 1
            )

        # =====================================================
        # LIP PROFILE 
        # =====================================================
        clear_tag("lip_profile")
        for i in range(LIP_POINTS):
            insert_timeseries(
                "lip_profile",
                round(18 + sin((tick + i) / 3) * 1.2, 2),
                index_no=i + 1
            )

        # =====================================================
        # MAP PROFILE
        # =====================================================
        clear_tag("map_profile")
        for i in range(MAP_POINTS):
            insert_timeseries(
                "map_profile",
                round(20 + sin((tick + i) / 4) * 2, 2),
                index_no=i * 10
            )

        # =====================================================
        #LAYER-WISE DATA 
        # =====================================================
        for layer_id, data in layers.items():
            # KPIs
            data["speed"] += 1
            data["yield"] += 1
            data["ampere"] += 1

            insert_timeseries(f"layer_{layer_id}_speed", data["speed"])
            insert_timeseries(f"layer_{layer_id}_yield", data["yield"])
            insert_timeseries(f"layer_{layer_id}_ampere", data["ampere"])

            # Graph data
            data["melt_pressure"] += 1
            data["melt_temperature"] += 1
            data["thickness_set"] += 0.1
            data["thickness_actual"] += 0.1

            insert_timeseries(f"layer_{layer_id}_melt_pressure", data["melt_pressure"])
            insert_timeseries(f"layer_{layer_id}_melt_temperature", data["melt_temperature"])
            insert_timeseries(f"layer_{layer_id}_thickness_set", data["thickness_set"])
            insert_timeseries(f"layer_{layer_id}_thickness_actual", data["thickness_actual"])


        # =====================================================
        # WINDER-WISE DATA
        # =====================================================
        for winder_id, data in winders.items():
            # KPI
            data["totalizer"] += 1
            insert_timeseries(
                f"winder_{winder_id}_totalizer",
                data["totalizer"]
            )

            # Time-series graphs
            data["roll_length"] += 1
            data["roll_dia"] += 0.5

            insert_timeseries(
                f"winder_{winder_id}_roll_length",
                data["roll_length"]
            )
            insert_timeseries(
                f"winder_{winder_id}_roll_dia",
                data["roll_dia"]
            )
    

        time.sleep(UPDATE_INTERVAL)
