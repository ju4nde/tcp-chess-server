⭐ 🚀 TCP Chess Server — Multithreaded Online Chess System
A complete client–server chess platform built using Python sockets, multithreading, and JSON-based communication.
Two players connect over TCP, get matched through a queue system, and play a full chess game with legality checks, chat support, and live game state updates.
This project demonstrates network programming, thread orchestration, protocol design, and real-time gameplay synchronization.
⭐ ✨ Features
🎮 Matchmaking System
Players send "hello" with a username.
Prevents duplicate names.
FIFO queue for waiting players.
First two players are paired automatically.
♟️ Real Chess Gameplay
Full legal move validation.
Detects:
Check
Checkmate
Stalemate
Automatic turn switching.
FEN state updates sent to both clients.
⚠ Chess rules engine (chess_logic.py) is adapted from a minimal open-source implementation.
All networking, server logic, matchmaking, JSON protocol, concurrency handling, and client implementation were done by me.
💬 In-Game Chat
Send text messages directly to your opponent during the match.
