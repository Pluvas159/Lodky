import pygame as pg
import sys
import socket
import threading
import time

pg.init()

W = 1336
H = 768


WIN = pg.display.set_mode((W, H))
pg.display.set_caption('Loďky')
clock = pg.time.Clock()
all_fonts = pg.font.get_fonts()
font = pg.font.SysFont(all_fonts[0], 50, False)
lodka = pg.image.load('img\\boat.png')
bg = pg.image.load('img\\bg.jpg')
bg = pg.transform.scale(bg,(W,H))
bg1 = pg.transform.scale(pg.image.load('img\\bg1.jpg'),(W,H))
bg2 = pg.transform.scale(pg.image.load('img\\bg2.jpg'),(W,H))

colors = [(41,40,40),(0,0,0),(255,255,255)]


class Board():
	def __init__(self, WIN, player, mouse):
		self.win = WIN
		self.player = player
		self.x = 20
		self.mouse = mouse
		self.boats = False
		all_fonts = pg.font.get_fonts()
		self.font = pg.font.SysFont(all_fonts[0], 50, False)
		self.lode = []
		self.done = False
		self.b = b(self.win, self.mouse, self, 0)
		self.bs = []
		self.tiles = []
		self.rada = 0
		self.end = False
		self.name = ''
		self.namepicked = False

	def change_name(self, key):
		if key == pg.K_BACKSPACE:
			self.name = self.name[:-1]
		elif key in (13, 271):
			self.namepicked = True
		elif key != None:
			self.name += chr(key)




	def draw_numerals(self):
		x = 20
		if not self.player:
			x = 1336-570
		y = 20
		for i in range(10):
			draw_text(chr(65+i),x-10,y+55*i,(colors[0]),11)
			draw_text(str(i),x+5+55*i,5,(colors[0]),11)


	def draw_board(self):
		# if not self.player:
		# 	pg.draw.rect(self.win,(0,0,0),(W/2,0,W/2,500))
		# else:
		# 	pg.draw.rect(self.win,(0,0,0),(0,0,W/2,500))
		if not self.player:
			self.x = 1336-570
		y = 20

		if not self.end:
			if not self.done:
				self.tiles = []
				for i in range(10):
					for j in range(10):
						self.tiles.append(Tile(self.x, y, j, i, self.win))
				self.done = True
				for i in range(4):
					self.bs.append(b(self.win, self.mouse, self, 100*i ))


			if self.boats or not self.player:                         	##refreshes all of first board
				for tile in self.tiles:
					if tile.color == (255,0,0) or tile.color == (10,255,255):
						tile.color = colors[0]
					if self.mouse.clicked and self.player:
						if tile.rect.collidepoint(mouse.pos):
							tile.color = (10,255,255)
							self.mouse.clicked = False
					for boat in self.lode:
						if tile.a == boat.a and tile.b == boat.b:
							if tile.color !=(254,0,0):
								tile.color = (152,152,152)
					tile.draw()
			else:
				self.get_boats()				##Initializes new boats


	def get_boats(self):
		draw_text(f'Zadaj lode {len(self.lode)}/8',800,200,(255,255,255))
		rect = draw_get_rect(f'Zadaj lode {len(self.lode)}/8',800,200,(255,255,255))
		pg.draw.rect(self.win,colors[0],rect)
		draw_text(f'Zadaj lode {len(self.lode)}/8',800,200,(255,255,255))
	
		if len(self.lode)<8:
			for tile in self.tiles:
				# if self.mouse.clicked:
				# 	if tile.rect.collidepoint(mouse.pos):
				# 		je = False
				# 		for boat in self.lode:
				# 			if boat.a == tile.a and boat.b == tile.b:
				# 				je = True
				# 		if not je:
				# 			self.lode.append(Boat(tile.a,tile.b))
				# 			tile.color = (255,0,0)
				# 			tile.lod = True
				tile.draw()
			for b in self.bs:
				b.draw()
				pass
		else:
			self.boats = True

	    
	def draw_rada(self, cnt):
		if cnt.player2:
			if self.rada ==0:
						draw_text('Si na rade', W/2-75, 600,(0,0,0),40)

			else:
						draw_text('Opponent je na rade', W/2-125, 600,(0,0,0),40)
			draw_text(f'Uhadnute: {cnt.uhadnute}/8', W/2-600, 570, (0,0,0), 30)
			draw_text(f'Uhadnute: {cnt.porazene}/8', W/2+400, 570, (0,0,0), 30)
			draw_text('Tvoje meno:',10,650,(0,0,0),30)
			draw_text('Súperove meno:',1060,650,(0,0,0),30)
			draw_text(self.name,30,700,(0,0,0),30)
			draw_text(cnt.brd2.name,1100,700,(0,0,0),30)






class Mouse():
	def __init__(self, win):
		self.win = win
		self.clicked = False
		self.mousedown = False


	def check_click(self):
		self.mouse = pg.mouse.get_pressed(1)
		if self.mouse[0]:
			self.pos = pg.mouse.get_pos()
			self.clicked = True


	def get_p(self):
		return pg.mouse.get_pos()


class Menu():
	def __init__(self, win, font, mouse):
		self.font = font
		self.win = win
		self.play = False
		self.mouse = mouse
		self.inmenu = True
		self.namepick = False

	def add(self, a, text):
		self.menu_text = []
		text_surface = self.font.render(text, 1, colors[2])
		rect = pg.Rect(self.win.blit(text_surface, (1336/2-55,200*a)))
		pg.draw.rect(self.win,(colors[0]),rect)
		rect = pg.Rect(self.win.blit(text_surface, (1336/2-55,200*a)))
		self.menu_text.append(rect)

	def check_collision(self):
		if mouse.clicked and self.inmenu:
			for i in self.menu_text:
				v = i.collidepoint(mouse.pos)
				if v:
					self.inmenu=False
					if self.menu_text.index(i)==0:
						self.namepick = True

class Boat():
	def __init__(self, a, b, x, y, lod):
		self.a = a
		self.b = b
		self.win = WIN
		self.x = x
		self.y = y
		self.lod = pg.transform.scale(lodka,(100,40))
		self.win = WIN
		self.poradie = lod

	def draw(self):
		if self.poradie == 1:
			self.win.blit(self.lod,(self.x,self.y))

class b():
	def __init__(self, win, mouse, board, offset):
		self.win = win
		self.mouse = mouse
		self.lod = lodka
		self.lod = pg.transform.scale(self.lod,(100,40))
		self.clicked = False
		self.pos = (50+offset,600)
		self.board = board
		self.last_tiles = []
		self.done = False

	def draw(self):
			for tile in self.last_tiles:
				tile.color = colors[0]
			self.last_tiles = []
			b = self.win.blit(self.lod,self.pos)
			if not self.done:
				if self.mouse.mousedown:
					if self.clicked:
						self.clicked = not self.clicked
					elif b.collidepoint(self.mouse.pos):
							self.clicked = True
							self.mouse.mousedown = False
				if self.clicked:
						pos = self.mouse.get_p()
						self.pos = (pos[0]-50,pos[1]-20)
						for tile in self.board.tiles:
							if tile.rect.collidepoint(self.pos):
								self.pos = (tile.rect.x,tile.rect.y)
								if tile.color == colors[0]:
									tile.color = (0,255,0)
									self.last_tiles.append(tile)
								for i in self.board.tiles:
									if i.a == tile.a+1 and i.b ==tile.b:
										if i.color == colors[0]:
											i.color = (0,255,0)
											self.last_tiles.append(i)			
								break



				else:
					self.poradie = 1
					for tile in self.board.tiles:
						if tile.rect.colliderect(b):
							je = False
							for boat in self.board.lode:
								if boat.a == tile.a and boat.b == tile.b:
									je = True
							if not je:
								if self.poradie ==1:
									self.board.lode.append(Boat(tile.a,tile.b,tile.rect.x,tile.rect.y, self.poradie))
									self.poradie = 0
								else:
									self.board.lode.append(Boat(tile.a,tile.b,tile.rect.x,tile.rect.y, self.poradie))
								tile.color = (255,0,0)
								tile.lod = True
								self.done = True




class Connection():
	def __init__(self, board1, board2, mouse):
		self.brd1 = board1
		self.brd2 = board2
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.adress = ('178.143.5.230', 5050)
		self.connected = False
		self.header = 1024
		self.format = 'utf-8'
		self.disconnect = False
		self.mouse = mouse
		self.message = ''
		self.vykreslene = False
		self.uhadnute = 0
		self.porazene = 0
		self.thread = False
		self.player2 = False
		self.end = False
		self.opp_disconnect = False

	def connect(self):
		if not self.thread:
			self.thr = threading.Thread(target = self.handler)
			self.thr.daemon = True
			self.thr.start()
			self.thread = True

	def handler(self):
		while True:
			if not self.connected:
				try:
					self.client.connect(self.adress)
					self.lode_pos = [[self.brd1.name]]
					for lod in self.brd1.lode:
						self.lode_pos.append([lod.a,lod.b])
					self.send_msg(self.lode_pos)
					self.connected = True
				except:
					self.connected = False
					draw_text('SERVER',800,300,(0,0,0),40)
					draw_text('OFFLINE',800,350,(255,0,0),40)
					continue
					

			else:
				self.change_brd2()

	def draw_status(self):
		if not self.player2 and self.brd1.boats:
			if self.connected:
				draw_text('SERVER',800,300,(0,0,0),40)
				draw_text('ONLINE',800,350,(0,255,0),40)
			else:
				draw_text('SERVER',800,300,(0,0,0),40)
				draw_text('OFFLINE',800,350,(255,0,0),40)




				

	def receive_msg(self, bit):
			message = self.client.recv(self.header).decode(self.format).strip()
			return message

	def send_msg(self, msg):
			message = str(msg).encode(self.format)
			msg_len = len(message)
			message += b' '*(self.header - msg_len)
			self.client.send(message)

	def change_brd2(self):
		if not self.player2:
				draw_text('SERVER',800,300,(0,0,0),40)
				draw_text('ONLINE',800,350,(0,255,0),40)
				player2 = self.receive_msg(self.header)
				player2 = player2.split('],')
				self.player2 = True
				brd2.draw_board()
				for i in player2:
					if i != player2[0]:
						for tile in brd2.tiles:
							if tile.a == int(i[2]) and tile.b == int(i[5]):
								tile.lod = True
					else:
						self.brd2.name = i.replace('[','').replace("'",'')


		else:
			if not self.disconnect:
				self.send_msg(self.message)
				msg = self.receive_msg(self.header).split(' ')
				if msg[0]=='0':
					self.brd1.rada = 0
					self.vykreslene = False
					self.draw_opp(msg)
					self.mouse.clicked = False
					running = True
					while running:
						if self.mouse.clicked:
							self.mouse.clicked=False
							for tile in self.brd2.tiles:
								if tile.rect.collidepoint(self.mouse.pos):
									if tile.lod:
										tile.color = (10,255,255)
										self.uhadnute +=1
										if self.uhadnute >=8:
											self.end = True
									else:
										tile.color = (152,152,152)
									self.send_msg([tile.a,tile.b])
									msg = self.receive_msg(self.header)
									running = False

				else:
					self.brd1.rada = 1 
				if msg[3]=="1":
					self.opp_disconnect = True



				self.draw_opp(msg)

	def draw_opp(self, msg):
		try:
			for tile in self.brd1.tiles:
					if tile.a == int(msg[1].replace('[','').replace(',','')) and tile.b == int(msg[2].replace(']','')):
						if tile.lod:
							if tile.color != (254,0,0):
								tile.color = (254,0,0)
								self.porazene += 1
								if self.porazene >=8:
									self.end = True
						else:
							tile.color = (0,255,0)
						if not self.end:
							tile.draw()
			if not self.end:
				for lod in self.brd1.lode:
							lod.draw()
		except:
			pass

def draw_text(text, x, y, color, w = 50):
	all_fonts = pg.font.get_fonts()
	font = pg.font.SysFont(all_fonts[0], w, False)
	text_surface = font.render(text, 1, color)
	WIN.blit(text_surface, (x,y))

def draw_get_rect(text, x, y, color, w = 50):
	all_fonts = pg.font.get_fonts()
	font = pg.font.SysFont(all_fonts[0], w, False)
	text_surface = font.render(text, 1, color)
	return pg.Rect(WIN.blit(text_surface,(x,y)))




class Tile():
	def __init__(self, x, y, a, b,window):
		self.x = x
		self.y = y
		self.a = a

		self.b = b 
		self.w = 50
		self.space = 5
		self.win = window
		self.rect = pg.Rect(self.x+self.w*self.a+self.space*self.a, self.y+self.w*self.b+self.space*self.b, self.w, self.w)
		self.color = colors[0]
		self.lod = False


	def draw(self):
		pg.draw.rect(self.win, self.color, self.rect)


if __name__ == '__main__':
	mouse = Mouse(WIN)
	men = Menu(WIN, font, mouse)
	brd = Board(WIN, True, mouse)
	brd2 = Board(WIN, False, mouse)
	cnt = Connection(brd, brd2, mouse)
	while True:
	    pg.display.update()
	    if men.inmenu or men.namepick:
	    	WIN.blit(bg,(0,0))
	    elif men.play and not cnt.player2:
	    	WIN.blit(bg1,(0,0))
	    elif cnt.player2:
	    	WIN.blit(bg2,(0,0))

	    mouse.check_click()
	    if men.inmenu:
	    	men.add(1,'Play')
	    	men.check_collision()
	    if men.namepick:
	    	men.add(1,'Zadaj meno')
	    	men.add(2,brd.name)
	    	if brd.namepicked:
	    		men.namepick = False
	    		men.play = True
	    if men.play:
	    	cnt.draw_status()
	    	if cnt.porazene<8 and cnt.uhadnute<8:
		    	brd.draw_board()
		    	if brd.boats == True:
		    		cnt.connect()
		    		for tile in brd2.tiles:
		    			tile.draw()
		    		brd.draw_rada(cnt)
		    		if brd.boats:
		    			for lod in brd.lode:
		    				if not cnt.end:
		    					lod.draw()
		    		if cnt.end:
		    			brd.end = True

	    	elif cnt.uhadnute>=8:
	    			WIN.blit(bg,(0,0))
		    		men.add(1,'Vyhral si')
	    	else:
	    			WIN.blit(bg,(0,0))
		    		men.add(1,'Prehral si')
	    for event in pg.event.get():
	        if event.type == pg.QUIT:
	            pg.quit() 
	            sys.exit(0)
	            cnt.disconnect=True
	            break
	        elif event.type == pg.MOUSEBUTTONDOWN:
	        	mouse.mousedown = True
	        if event.type == pg.KEYDOWN:
	        	brd.change_name(event.key)
	    if cnt.opp_disconnect:
	    	WIN.blit(bg,(0,0))
	    	men.add(1,'Opponent disconnected')
	    	men.add(2,'closing the game')
	    	pg.display.update()
	    	time.sleep(3)
	    	break
	    clock.tick(60)