import socket
import threading
import json

def send_json(conn, obj):
    conn.sendall((json.dumps(obj) + "\n").encode())

def recv_json(conn):
    try:
        buffer = b""
        while True:
            chunk = conn.recv(1)
            if not chunk:
                return None
            if chunk == b"\n":
                break
            buffer += chunk
        data = buffer.decode()
        return json.loads(data) if data else None
    except Exception as e:
        print(f"Error receiving JSON: {e}")
        return None

def send_messages(client_socket):
    while True:
        user_input = input()
        parts = user_input.strip().split(maxsplit=1) 
        command = parts[0]
        match command:
            case "move":
                uci = parts[1]
                send_json(client_socket, {"type": command, "uci": uci})
            case "chat":
                text = parts[1]  
                send_json(client_socket, {"type": command, "text": text})
            case "resign":
                client_socket.close()
                exit()

def receive_messages(client_socket, pcolor):
    while True:
        msg = recv_json(client_socket)
        msgtype = msg["type"]
        match msgtype:
            case "state":
                if (msg["turn"] == pcolor):
                    print(f"[server] turn: {pcolor}")
                    print(">", end="", flush=True)
                else:
                    print(f"[server] opponent's turn")
                    print(">", end="", flush=True)
            case "illegal":
                print(f"Illegal move, reason {msg['reason']}")
                print(">", end="", flush=True)
            case "chat":
                text = msg["text"]
                player =msg["from"]
                print(f'{player}: {text}')
                print(">", end="", flush=True)
            case "result":
                print(f'Result: {msg["outcome"]}, winner= {msg["winner"]}')
                print(">", end="", flush=True)
            case "opponent_left":
                print("opponent left, closing connection")
                print(">", end="", flush=True)
            case "move_ok":
                if (msg["by"] == pcolor):
                    print(f"move accepted: {msg['uci']}")
                    print(">", end="", flush=True)
                else:
                    print(f"opponent played: {msg['uci']}")
                    print(">", end="", flush=True)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))
    name = input("Enter name: ")
    send_json(client_socket, {"type":"hello","name":name })
    msg= recv_json(client_socket)
    welcomestatus = msg["ok"]
    if (welcomestatus == "false" ):
        print("Name already taken, please reconnect")
        client_socket.close()
        exit()
    msg = recv_json(client_socket)
    if (msg["type"] == "queued" and msg["pos"] == 1):
        print(f"[server] queued (position 1)...")
        msg = recv_json(client_socket)
    if (msg["type"] == "start"):
        color = msg["color"]
        print(f"[server] game started — you are {color.upper()} vs {msg['opponent']}")
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, color), daemon=True)
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()
    send_thread.join()

if __name__ == "__main__":
    main()