# import os
# from flask_socketio import SocketIO
# from flask_jwt_extended import JWTManager


# ASYNC_MODE = os.getenv("SOCKETIO_ASYNC_MODE", "threading")

# socketio = SocketIO(
#     cors_allowed_origins="*",
#     async_mode=ASYNC_MODE
# )

# jwt = JWTManager()




# from flask_socketio import SocketIO
# from flask_jwt_extended import JWTManager

# socketio = SocketIO(
#     cors_allowed_origins="*",
#     async_mode="threading",
#     ping_interval=25,
#     ping_timeout=60
# )

# jwt = JWTManager()



from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="threading",  
    ping_interval=25,
    ping_timeout=60
)

jwt = JWTManager()
