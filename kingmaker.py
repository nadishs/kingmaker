'''
Project: Kingmaker by Nadish Shajahan
nadishshahjahan@gmail.com
https://github.com/nadishs
A Fisat CHPC Assignment Project.
Copyright (C) 2016 Nadish Shajahan

More details in README
'''
#####-----------------------------------1.CLASSES--------------------------------------------
class Unit:
	UnitCount = 0
	def __init__(self, uname, unclass, start_x,start_y, utype):
		self.name = uname
		self.uclass = unclass
		self.position_x = start_x
		self.position_y = start_y
		self.type = utype
		self.status = 1 # 1 for alive, 0 for dead
		Unit.UnitCount+=1

class Environment:
	LevelMap = [[]]  # A 2d map:  0 if empty tile,  1-5 if player(diff classes), 11-15 if enemy (diff classes)
	UnitMap = [[]]
	mp_size_x = 0
	mp_size_y = 0

	def __init__(self, xsize, ysize):
		Environment.mp_size_x = xsize
		Environment.mp_size_y = ysize
		Environment.LevelMap = [[0 for i in range(Environment.mp_size_x)] for j in range(Environment.mp_size_y)]
		Environment.UnitMap = [[None] * Environment.mp_size_x for j in range(Environment.mp_size_y)]

	def displayMap(self):
		for i in range(Environment.mp_size_x):
			for j in range(Environment.mp_size_y):
				col = colorD['gray']
				flag =0
				if Environment.LevelMap[i][j]!=0:
					colclass = Environment.UnitMap[i][j].uclass
					col = colorD['bishop']
					if Environment.UnitMap[i][j].type == 'P':
						flag=1
					elif Environment.UnitMap[i][j].type == 'E':
						flag=2

				if flag == 1:
					pygame.draw.rect(screen,
		                             col,
		                             [(MARGIN + WIDTH) * j,
		                              (MARGIN + HEIGHT) * i,
		                              WIDTH,
		                              HEIGHT])
					screen.blit(pchessimageD[colclass],((MARGIN + WIDTH) * j,(MARGIN + HEIGHT) * i))

				elif flag == 2:
					pygame.draw.rect(screen,
		                             col,
		                             [(MARGIN + WIDTH) * j + MARGIN,
		                              (MARGIN + HEIGHT) * i + MARGIN,
		                              WIDTH,
		                              HEIGHT])

					screen.blit(echessimageD[colclass],((MARGIN + WIDTH) * j + MARGIN,(MARGIN + HEIGHT) * i + MARGIN))
				else:

					pygame.draw.rect(screen,
		                             col,
		                             [(MARGIN + WIDTH) * j + MARGIN,
		                              (MARGIN + HEIGHT) * i + MARGIN,
		                              WIDTH,
		                              HEIGHT])
		gridsize = Environment.mp_size_x*(WIDTH+MARGIN)
		label1 = gamefont.render("Player:", 1, (255,255,0))
		label2 = gamefont2.render(P1.name, 1, (255,255,0))
		label3 = gamefont.render("Class:", 1, (255,255,0))
		label4 = gamefont2.render(P1.uclass, 1, (255,255,0))
		label5 = gamefont.render("Exp:", 1, (255,255,0))
		label6 = gamefont2.render(str(P1.experience), 1, (255,255,0))

		screen.blit(label1, (gridsize+10, 20))
		screen.blit(label2, (gridsize+10, 50))
		screen.blit(label3, (gridsize+10, 80))
		screen.blit(label4, (gridsize+10, 110))
		screen.blit(label5, (gridsize+10, 140))
		screen.blit(label6, (gridsize+10, 170))

	def updateMap(self, xpos, ypos, newxpos, newypos, uunit, unclass):
		#map updations here
		if uunit.type == 'P':
			Environment.LevelMap[newxpos][newypos] = Classes.UClassD[unclass]
			Environment.UnitMap[newxpos][newypos] = uunit
		elif uunit.type == 'E':
			temp = Classes.UClassD[unclass]
			Environment.LevelMap[newxpos][newypos] = temp*10
			Environment.UnitMap[newxpos][newypos] = uunit
			#no other entities as of now....
		Environment.LevelMap[xpos][ypos] = 0
		Environment.UnitMap[xpos][ypos]= None

#Players
class Player(Unit):
	PlayerCount = 0

	def __init__(self, pname, pclass, start_x,start_y,LevelEnv):
		Unit.__init__(self, pname, pclass, start_x, start_y,'P')
		self.experience = 0
		LevelEnv.updateMap(-1,-1, start_x,start_y,self, self.uclass)
		Player.PlayerCount += 1
	#movement
	def movePlayer(self, action, LevelEnv):
 		oldpos_x = self.position_x
		oldpos_y = self.position_y
		outcome = 0
		if action == K_UP:

			if oldpos_x == 0:
				return 1
			else:
				if LevelEnv.LevelMap[oldpos_x-1][oldpos_y]==0:
					LevelEnv.updateMap(oldpos_x, oldpos_y, oldpos_x-1, oldpos_y, self, self.uclass)
					self.position_x = oldpos_x-1
					self.position_y = oldpos_y
				else:
					# no player collision for now (only needed for multiplayer)
					outcome = self.engage(oldpos_x-1, oldpos_y,LevelEnv)
		elif action == K_DOWN:

			if oldpos_x == Environment.mp_size_x-1:
				return 1
			else:
				if LevelEnv.LevelMap[oldpos_x+1][oldpos_y]==0:
					LevelEnv.updateMap(oldpos_x, oldpos_y, oldpos_x+1, oldpos_y, self, self.uclass)
					self.position_x = oldpos_x+1
					self.position_y = oldpos_y
				else:
					# no player collision for now (only needed for multiplayer)
					outcome = self.engage(oldpos_x+1, oldpos_y,LevelEnv)

		elif action == K_LEFT:

			if oldpos_y == 0:
				return 1
			else:
				if LevelEnv.LevelMap[oldpos_x][oldpos_y-1]==0:
					LevelEnv.updateMap(oldpos_x, oldpos_y, oldpos_x, oldpos_y-1, self, self.uclass)
					self.position_x = oldpos_x
					self.position_y = oldpos_y-1
				
				else:
					# no player collision for now (only needed for multiplayer)
					outcome = self.engage(oldpos_x, oldpos_y-1,LevelEnv)


		elif action == K_RIGHT:

			if oldpos_y == Environment.mp_size_y-1:
				return 1
			else:
				if LevelEnv.LevelMap[oldpos_x][oldpos_y+1]==0:
					LevelEnv.updateMap(oldpos_x, oldpos_y, oldpos_x, oldpos_y+1, self, self.uclass)
					self.position_x = oldpos_x
					self.position_y = oldpos_y+1
				else:
					outcome = self.engage(oldpos_x, oldpos_y+1,LevelEnv)
		return outcome 

	# player vs enemy fights!
	def engage(self, x_pos, y_pos,LevelEnv):
		pclass = Classes.UClassD[self.uclass]-1
		temp = Environment.UnitMap[x_pos][y_pos].uclass
		eclass = Classes.UClassD[temp]-1
		oldpos_x = self.position_x
		oldpos_y = self.position_y

		if pclass >= eclass:
			Environment.UnitMap[x_pos][y_pos].status = 0
			self.experience += 10
			pclass += 1
			self.uclass = Classes.UClassL[pclass]
			
			LevelEnv.updateMap(oldpos_x, oldpos_y, x_pos, y_pos, self, self.uclass)
			self.position_x = x_pos
			self.position_y = y_pos
			if pclass == Classes.ClassesCount-1:
				outcome = 2
			else:
				outcome = 1
		else:
			LevelEnv.updateMap(oldpos_x, oldpos_y, -1, -1, self, self.uclass)
			self.position_x = 0
			self.position_y = 0
			self.status = 0
			outcome = -1
		
		return outcome


#Enemies
class Enemy(Unit):
	EnemyCount = 0

	def __init__(self, eclass, start_x,start_y,LevelEnv):
		Unit.__init__(self, str(Enemy.EnemyCount), eclass, start_x, start_y,'E')
		flag = 0

		if Environment.LevelMap[start_x][start_y] != 0:
			while Environment.LevelMap[start_x][start_y] != 0:
				start_x = random.randrange(0, 8, 1)
				start_y = random.randrange(0, 8, 1)
		LevelEnv.updateMap(-1,-1, start_x,start_y,self, self.uclass)
		Enemy.EnemyCount += 1

#UnitClasses
class Classes:
	ClassesCount = 0
	UClassD = {}
	UClassL = []
	def __init__(self, cname, ccolor, chitpoints, cdamage):
		self.name = cname
		self.color = ccolor
		self.hitpoints = chitpoints
		self.damage = cdamage
		Classes.UClassL.append(cname)
		Classes.UClassD[cname] = Classes.ClassesCount +1
		Classes.ClassesCount += 1

#####-----------------------------------2.FUNCTIONS--------------------------------------------
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
	fontobject = pygame.font.Font(None,18)
	titlefont = pygame.font.SysFont("arial", 20,True)
	
	pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  	pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  	if len(message) != 0:
		screen.blit(fontobject.render(message, 1, (255,255,255)),
                	((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
		screen.blit(pchessimageD['king'],((screen.get_width() / 2)-10,10))
		screen.blit(titlefont.render("KINGMAKER", 1, (255, 0, 0)),
                ((screen.get_width() / 2) - 60, 40))
		
 	pygame.display.flip()

def ask(screen, question):
  
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")



#####-----------------------------------3.MAIN--------------------------------------------
#imports
import random
import os
import sys
import pygame,pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

#loading class data
classesfile = open("classes.txt","r+")
lines = [line.rstrip('\n') for line in classesfile]
GameClasses = []
i=0
for line in lines:	

	words = line.split(',')
	temp = Classes(words[0],words[1],words[2],words[3])
	GameClasses.append(temp)
	i+=1

classesfile.close()

#declarations

##pygame declarations

###colors
colorD = {}
colorD['pawn'] = (0, 0, 0)
colorD['knight'] = (255, 255, 255)
colorD['bishop'] = (0, 255, 0)
colorD['king'] = (255, 0, 0)
colorD['rook'] = (255, 255, 0)
colorD['queen'] =  (0, 0, 255)
colorD['gray'] =  (200, 200, 200)

###grid & cell
WIDTH = 20
HEIGHT = 20
CWIDTH = WIDTH
MARGIN = 5
pygame.init()
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Kingmaker")
done = False
###text
gamefont = pygame.font.SysFont("monospace", 17)
gamefont2 = pygame.font.SysFont("arial", 17)

###window icon
icon = pygame.image.load(os.path.join("graphics","Chess_tile_kl.png"))
pygame.display.set_icon(icon)

###begin
clock = pygame.time.Clock()

###loading chesstile graphics

pchessimageD = {}

pchessimageD['pawn'] = pygame.image.load(os.path.join("graphics","Chess_tile_pd.png")).convert()
pchessimageD['pawn'] = pygame.transform.scale(pchessimageD['pawn'], (CWIDTH,CWIDTH))
pchessimageD['rook'] = pygame.image.load(os.path.join("graphics","Chess_tile_rd.png")).convert()
pchessimageD['rook']= pygame.transform.scale(pchessimageD['rook'], (CWIDTH,CWIDTH))
pchessimageD['knight'] = pygame.image.load(os.path.join("graphics","Chess_tile_nd.png")).convert()
pchessimageD['knight'] = pygame.transform.scale(pchessimageD['knight'], (CWIDTH,CWIDTH))
pchessimageD['bishop'] = pygame.image.load(os.path.join("graphics","Chess_tile_bd.png")).convert()
pchessimageD['bishop'] = pygame.transform.scale(pchessimageD['bishop'], (CWIDTH,CWIDTH))
pchessimageD['king'] = pygame.image.load(os.path.join("graphics","Chess_tile_kd.png")).convert()
pchessimageD['king'] = pygame.transform.scale(pchessimageD['king'], (CWIDTH,CWIDTH))
pchessimageD['queen'] = pygame.image.load(os.path.join("graphics","Chess_tile_qd.png")).convert()
pchessimageD['queen'] = pygame.transform.scale(pchessimageD['queen'], (CWIDTH,CWIDTH))

echessimageD = {}

echessimageD['pawn'] = pygame.image.load(os.path.join("graphics","Chess_tile_pl.png")).convert()
echessimageD['pawn'] = pygame.transform.scale(echessimageD['pawn'], (CWIDTH,CWIDTH))
echessimageD['rook'] = pygame.image.load(os.path.join("graphics","Chess_tile_rl.png")).convert()
echessimageD['rook'] = pygame.transform.scale(echessimageD['rook'], (CWIDTH,CWIDTH))
echessimageD['knight'] = pygame.image.load(os.path.join("graphics","Chess_tile_nl.png")).convert()
echessimageD['knight'] = pygame.transform.scale(echessimageD['knight'], (CWIDTH,CWIDTH))
echessimageD['bishop'] = pygame.image.load(os.path.join("graphics","Chess_tile_bl.png")).convert()
echessimageD['bishop'] = pygame.transform.scale(echessimageD['bishop'], (CWIDTH,CWIDTH))
echessimageD['king'] = pygame.image.load(os.path.join("graphics","Chess_tile_kl.png")).convert()
echessimageD['king'] = pygame.transform.scale(echessimageD['king'], (CWIDTH,CWIDTH))
echessimageD['queen'] = pygame.image.load(os.path.join("graphics","Chess_tile_ql.png")).convert()
echessimageD['queen'] = pygame.transform.scale(echessimageD['queen'], (CWIDTH,CWIDTH))

##object declarations
Level = Environment(8,8)

screen = pygame.display.set_mode((320,240))
pname = ask(screen, "Player Name")
eno = 5
screen.fill(colorD['pawn'])
px = 0
py = 0

pclass = Classes.UClassL[0]
P1 = Player(str(pname),pclass,px,py,Level)

win = 0
ex = 0
ey = 0

ec = 0


Enemies = [[None] for i in range(eno)]
for i in range(eno):
	ex = random.randrange(0, 8, 1)
	ey = random.randrange(0, 8, 1)
	enclass = Classes.UClassL[ec]
	Enemies[i] = Enemy(enclass,px,py,Level)
	ec += 1
Level.displayMap()
result = 0
waiting = False
#main loop
while win==0 and not done:

	for event in pygame.event.get():  
		if event.type == pygame.QUIT: 
			done = True
		if event.type == KEYDOWN:
			result = P1.movePlayer(event.key,Level)
		else:
			result = 0

	if result == -1:
		
		screen.fill(colorD['pawn'])
		label1 = gamefont.render("You are not worthy! :( ;)", 1, (255,255,0))
		label2 = gamefont.render("Press Enter key to exit...", 1, (255,255,0))
		screen.blit(label1, (30, 80))
		screen.blit(label2, (30, 110))
		pygame.display.flip()

		while 1:
			inkey = get_key()
			if inkey == K_RETURN:
				break
		win = -1
		break
	if result == 2:
		screen.fill(colorD['pawn'])


		pygame.draw.rect(screen,
						 colorD['pawn'],
						 [(MARGIN + WIDTH)+120,
						  (MARGIN + HEIGHT)+5,
						  WIDTH + MARGIN,
						  HEIGHT + MARGIN])
		pygame.draw.rect(screen,
						 colorD['king'],
						 [(MARGIN + WIDTH)+120, 
						  (MARGIN + HEIGHT)+5,
						  WIDTH,
						  HEIGHT])

		screen.blit(pchessimageD['king'],((MARGIN + WIDTH)+120,(MARGIN + HEIGHT)+5))


		label1 = gamefont.render("You are the King! :) ", 1, (255,255,0))
		label2 = gamefont.render("Press Enter key to exit...", 1, (255,255,0))
		screen.blit(label1, (80, 80))
		screen.blit(label2, (30, 110))
		pygame.display.flip()

		while 1:
			inkey = get_key()
			if inkey == K_RETURN:
				break

		win = 1
		break
	os.system('clear')
	screen.fill(colorD['pawn'])
	Level.displayMap()
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
###-------------------------------------------END------------------------------------------
