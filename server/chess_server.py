import socket
import threading
import json
from  chess_logic import Board, Move

players = {}
queue = []
gamelist = {}
names = {}

def send_json(conn, obj):
    conn.sendall((json.dumps(obj) + "\n").encode())

def is_in_check(board):
     color = board.turn
     kingrow,kingcolumn = board._king_pos(color)
     return board.is_square_attacked_by(kingrow,kingcolumn, board.enemy(color))

def recv_json(conn):
    data = conn.recv(1024).decode()
    return json.loads(data.strip()) if data else None

def msg_receiver(conn,rival,board):
     flag = True
     while flag:
          msg = recv_json(conn)
          msgtype = msg["type"]
          match msgtype:
               case "move":
                    if (board.turn == gamelist[conn]):
                         uci = msg["uci"]  
                         mv = Move(uci)
                         ok, reason = board.make_move(mv)
                         if not ok:
                            send_json(conn, {"type": "illegal", "reason": reason})
                            break
                         else:
                              print(f"[{names[conn]}] {uci} ✓")
                              send_json(conn, {"type": "move_ok", "uci": uci, "by": "white" if gamelist[conn]== 'w' else "black"})
                              send_json(rival, {"type": "move_ok", "uci": uci, "by": "white" if gamelist[conn]== 'w' else "black"})
                              if is_in_check(board):
                                send_json(conn, {"type": "result", "outcome": "checkmate", "winner": "white" if gamelist[conn]== 'w' else "black"} )
                                send_json(rival, {"type": "result", "outcome":"checkmate" , "winner": "white" if gamelist[conn]== 'w' else "black"}) 
                                break
                    else:
                         send_json(conn, {"type": "illegal", "reason": "not_your_turn"})
                         break
                    send_json(conn, {"type":"state", "fen": board.fen(),"turn": "white" if board.turn == 'w' else "black","check": is_in_check(board)})
                    send_json(rival, {"type":"state", "fen": board.fen(),"turn": "white" if board.turn == 'w' else "black","check": is_in_check(board)})
               case "chat":
                    text = msg["text"]
                    send_json(rival, {"type": "chat","from": names[conn], "text": text})
               case "resign":
                    send_json(rival, {"type": "opponent_left"})
                    
     

def gamethread(c1,c2):
     board = Board()
     send_json(c1, {"type":"state", "fen": board.fen(),"turn": "white","check": is_in_check(board)})
     send_json(c2, {"type":"state", "fen": board.fen(),"turn": "white","check": is_in_check(board)})
     thread1 = threading.Thread(target=msg_receiver, args=(c1,c2,board))
     thread1.start()
     thread2 = threading.Thread(target=msg_receiver, args=(c2,c1,board))
     thread2.start()

                        
     
     


def start_game():
     if len(queue) == 2:
          p1 = queue.pop(0)
          p2 = queue.pop(0)
          c1= players[p1]
          c2 = players [p2]
          names[c1]= p1
          names[c2]= p2
          
          gamelist[c1] = 'w'
          gamelist[c2] = 'b'

          print(f"Paired: {p1} (white) vs {p2} (black)")

          send_json(c1, {"type": "start", "color": "white", "opponent": p2})
          send_json(c2, {"type": "start", "color": "black", "opponent": p1})

          thread = threading.Thread(target=gamethread, args = (c1,c2))
          thread.start()

def handle_client(conn, addr):
     namejson = recv_json(conn)
     name = namejson["name"]
     if name.lower() in players:
        send_json(conn, {"type": "welcome", "ok": "false"})
        conn.close()
        return
     print(f"Client {name} connected from {addr}")
     players[name] = conn
     send_json(conn, {"type": "welcome", "ok": "true"})
     queue.append(name)
     pos = len(queue)
     if (pos ==1 ):
        send_json(conn, {"type": "queued", "pos": pos})

     start_game()

          


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port =12345
    server_socket.bind(("localhost",port))
    server_socket.listen(5)
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
        main()
