import { io } from "socket.io-client";

const socket = io("http://localhost:8000/telemetry", {
  transports: ["websocket"]
});

export default socket;
