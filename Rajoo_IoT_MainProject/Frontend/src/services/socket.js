// import { io } from "socket.io-client";

// const socket = io("http://localhost:8000/telemetry", {
//   transports: ["websocket"]
// });

// export default socket;


// src/socket.js


// src/socket.js


// src/services/socket.js
import { io } from "socket.io-client";

const socket = io("http://localhost:5000", {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: Infinity,
  reconnectionDelay: 1000
});

socket.on("connect", () => {
  console.log("Socket connected to backend:", socket.id);
});

socket.on("disconnect", () => {
  console.log(" Socket disconnected");
});

socket.on("connect_error", (err) => {
  console.error(" Socket connection error:", err.message);
});

export default socket;

