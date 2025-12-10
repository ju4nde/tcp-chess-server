# Multithreaded TCP Chess Server  
A full client–server chess system built using Python sockets and multithreading.  
Players connect via TCP, enter a matchmaking queue, and are paired automatically.  
The server manages real-time moves, legality checking, chat messaging, and game termination.

**Technologies:** Python, sockets, threads, JSON messaging, custom protocol design.

---

## 🚀 Features

### 🧩 Matchmaking Queue
- Players send `"hello"` with their username  
- Server prevents duplicate names  
- Players are added to a FIFO queue  
- First two players are paired into a match  

### ♟ Real Chess Gameplay
- Supports legal move validation  
- Check, checkmate, stalemate detection  
- Automatic turn switching  
- FEN board state output after each move  

> ⚠ Chess rules implementation comes from an adapted minimal open-source engine (`chess_logic.py`).  
> All networking, server logic, concurrency, JSON protocol, client app, and matchmaking were implemented by me.

---

## 📡 Networking Protocol Overview

The client and server communicate using **newline-terminated JSON objects**.
