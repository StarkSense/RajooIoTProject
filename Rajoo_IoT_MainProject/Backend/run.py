

from app import create_app
from app.extensions import socketio
from app.services.db_service import init_db
from app.services.dummy_data_provider import dummy_data_task
from app.sockets.telemetry_socket import start_telemetry
import time

app = create_app()

if __name__ == "__main__":
    init_db()

    socketio.start_background_task(dummy_data_task)
    time.sleep(2)

    start_telemetry()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )
