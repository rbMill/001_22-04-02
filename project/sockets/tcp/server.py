import threading
import socket
import time




class console_server:

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.lc = 0
        try:
            host = socket.gethostname()
            self.server.bind((host, 9999))
            self.server.listen()
            self.stop = False
            print(f'({host}) server online...')
            while self.running:
                self.client, self.address = self.server.accept()
                print(f'{self.address} joined')
                self._dis_loop = threading.Thread(target=self.dis_loop)
                self._dis_loop.start()

                self._ent_loop = threading.Thread(target=self.ent_loop)
                self._ent_loop.start()
                time.sleep(0.01)
        except OSError:
            print('Port Already Exist Cannot Overide')

    def dis_loop(self):
        while self.running:
            try:
                msg = self.client.recv(1024).decode('utf-8')

                if len(msg) > 0:
                    print(f'<<< {msg}')
                self.lc+=1
                time.sleep(0.01)
            except ConnectionResetError:
                print(f'{self.address} disconnected')
                return

    def ent_loop(self):
        while self.running:
            try:
                inp = input()
                if len(inp) > 0:
                    self.client.send(inp.encode('utf-8'))
                time.sleep(0.01)
            except ConnectionResetError:
                print(f'{self.address} disconnected')
                return

console_server()