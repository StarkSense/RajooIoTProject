import time
from math import sin
from app.services.db_service import (
    init_db,
    get_db,
    insert_machine_overview,
    insert_timeseries
)

# =========================================================
# CONFIG (MATCH IMAGE-1)
# =========================================================
UPDATE_INTERVAL = 10
DIE_ZONES = 7
LIP_POINTS = 12
MAP_POINTS = 9

# =========================================================
# PERSISTENT MACHINE STATE (OPC-UA STYLE)
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
# UTILITY: CLEAR TAG DATA (CRITICAL FIX)
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

    print("[DUMMY] Image-1 deterministic dummy started (7 zones)")

    while True:
        tick += 1

        # =====================================================
        # MACHINE OVERVIEW (APPEND)
        # =====================================================
        machine["total_set_output"] += 1
        machine["total_actual_output"] += 1
        machine["density"] = round(0.92 + 0.005 * sin(tick / 10), 3)
        machine["gsm"] = round(76 + sin(tick / 8), 2)
        machine["lay_flat"] = round(226 + sin(tick / 6) * 2, 2)

        insert_machine_overview(machine)

        # =====================================================
        # SPEED (APPEND – TREND)
        # =====================================================
        insert_timeseries("speed_set", round(speed_set + sin(tick / 5) * 3, 2))
        insert_timeseries("speed_actual", round(speed_actual + sin(tick / 6) * 3, 2))

        # =====================================================
        # IBC TEMP (APPEND – TREND)
        # =====================================================
        insert_timeseries("ibc_temp_in", round(82 + sin(tick / 4) * 2, 2))
        insert_timeseries("ibc_temp_out", round(78 + sin(tick / 5) * 2, 2))

        # =====================================================
        # THICKNESS (APPEND – TREND)
        # =====================================================
        actual_thickness = round(thickness_set + sin(tick / 7) * 0.6, 2)
        insert_timeseries("thickness_set", thickness_set)
        insert_timeseries("thickness_actual", actual_thickness)
        insert_timeseries("gbr_position", gbr_position + tick % 5)

        # =====================================================
        # DIE TEMP ZONES (OVERWRITE – CRITICAL)
        # =====================================================
        clear_tag("die_temp")
        for i in range(DIE_ZONES):
            insert_timeseries(
                "die_temp",
                round(172 + i + sin((tick + i) / 6) * 2, 1),
                index_no=i + 1
            )

        # =====================================================
        # LIP PROFILE (OVERWRITE)
        # =====================================================
        clear_tag("lip_profile")
        for i in range(LIP_POINTS):
            insert_timeseries(
                "lip_profile",
                round(18 + sin((tick + i) / 3) * 1.2, 2),
                index_no=i + 1
            )

        # =====================================================
        # MAP PROFILE (OVERWRITE)
        # =====================================================
        clear_tag("map_profile")
        for i in range(MAP_POINTS):
            insert_timeseries(
                "map_profile",
                round(20 + sin((tick + i) / 4) * 2, 2),
                index_no=i * 10
            )

        time.sleep(UPDATE_INTERVAL)
