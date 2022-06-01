import threading
import socket
import time




class console_client:

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.lc = 0
        try:
            self.server.connect(('192.168.0.104', 9999))
            print('connected to server')
            while self.running:
                if self.running:
                    self._dis_loop = threading.Thread(target=self.dis_loop)
                    self._dis_loop.start()
                    self._ent_loop = threading.Thread(target=self.ent_loop)
                    self._ent_loop.start()
                time.sleep(0.01)
            print('you have disconnected')
        except OSError:
            print('Server not Found')

    def dis_loop(self):
        while self.running:
            try:
                msg = self.server.recv(1024).decode('utf-8')

                if len(msg) > 0:
                    print(f'<<< {msg}')
                self.lc+=1
            except ConnectionResetError:
                self.running = False
                break
            time.sleep(0.01)

    def ent_loop(self):
        while self.running:
            try:
                inp = input()
                if len(inp) > 0:
                    self.server.send(inp.encode('utf-8'))
            except ConnectionResetError:
                self.running = False
                break
            time.sleep(0.01)

console_client()