import socket
import threading, multiprocessing
import time

SERVER_ADRESS = ('192.168.100.41', 5050)
FORMAT = 'utf-8'
HEADER = 1024

players = {}

class Server():							#server start
	def __init__(self, inet, stream):
		self.inet = inet
		self.stream = stream
		self.server = socket.socket(self.inet, self.stream)
		self.server.bind(SERVER_ADRESS)
		self.clients = []
		self.players = 0

	def start(self):
		print('Awaiting user')
		self.server.listen()
		while True:
			client_socket, client_adress = self.server.accept()
			print(f'Client connected at {client_adress[0]}')
			self.clients.append(Client(client_socket, client_adress, self))
			if len(self.clients)>1:
				for client in self.clients:
					for j in self.clients:
						if client.adress != j.adress:
							try:
								client.send_msg(j.lode)
							except:
								client.close_cnt()
			threading.Thread(target = self.clients[-1].handle, daemon = True).start()					




class Client():								#handles every client
	def __init__(self, socket, adress, server):
		self.socket = socket
		self.adress = adress
		self.lode = self.receive_msg(HEADER)
		self.server = server
		self.pos = [-1, -1]


			
	def close_cnt(self):
		self.socket.close()
		print('Client disconnected at',self.adress)
		self.server.clients.remove(self)
		self.server.players -= 1 

	def handle(self):
		self.turn = self.server.clients.index(self)
		self.server.players += 1
		while True:
			try:
				pos = [-1,-1]
				msg = self.receive_msg(HEADER)
				if bool(msg):
					self.pos = msg
					self.turn = 1
					for i in self.server.clients:
						if i !=self:
							i.turn = 0
							pos = i.pos
				for i in self.server.clients:
					if i != self:
						pos = i.pos


				if msg=='Disconnect':
					print(msg)
					self.close_cnt()
					break

				self.send_msg(f'{self.turn} {pos} {self.server.players}')
			except Exception as e:
				print(e)
				self.close_cnt()
				break
 

	def send_msg(self, msg):					#essential for send and receive
			message = str(msg).encode(FORMAT)
			msg_len = len(message)
			message += b' '*(HEADER - msg_len)
			self.socket.send(message)

	def receive_msg(self, bit):
		message = self.socket.recv(HEADER).decode(FORMAT).strip()
		return message
		




if __name__=='__main__':
	Server(socket.AF_INET, socket.SOCK_STREAM).start()