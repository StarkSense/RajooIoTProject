# from app import create_app
# from app.extensions import socketio
# from app.services.db_service import init_db
# from app.services.dummy_data_provider import dummy_data_task
# from app.sockets.telemetry_socket import telemetry_task

# app = create_app()

# if __name__ == "__main__":
#     init_db()

    
#     socketio.start_background_task(dummy_data_task)
#     socketio.start_background_task(telemetry_task)

#     socketio.run(
#     app,
#     host="0.0.0.0",
#     port=5000,
#     debug=True,
#     use_reloader=False
# )




# ----------------------------------------------------------------------------------------------------
# from app import create_app
# from app.extensions import socketio
# from app.services.db_service import init_db
# from app.services.dummy_data_provider import dummy_data_task
# from app.sockets.telemetry_socket import telemetry_task

# app = create_app()

# if __name__ == "__main__":
#     init_db()

#     # -----------------------------
#     # START BACKGROUND TASKS
#     # -----------------------------
#     socketio.start_background_task(dummy_data_task)
#     socketio.start_background_task(telemetry_task)

#     # -----------------------------
#     # START SERVER
#     # -----------------------------
#     socketio.run(
#         app,
#         host="0.0.0.0",
#         port=5000,
#         debug=True,
#         use_reloader=False
#     )


from app import create_app
from app.extensions import socketio
from app.services.db_service import init_db
from app.services.dummy_data_provider import dummy_data_task
from app.sockets.telemetry_socket import telemetry_task

app = create_app()

if __name__ == "__main__":
    init_db()

    socketio.start_background_task(dummy_data_task)
    socketio.start_background_task(telemetry_task)

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False   
    )
