from copy import deepcopy as copy
from random import randint as random
from pg2q import getTable, jsOpen

def getrandXY(d, exc=[]):
	if isinstance(d, int): d = [d, d]
	while True:
		res = [random(0, d[0]-1), random(0, d[1]-1)]
		if res not in exc: break
	return res

def snakeMove(snake, pastpos):
	pastpos = copy(snake[0])
	if len(snake) > 1:
		snake.pop(-1)
		snake.insert(1, copy(pastpos))
	return snake, pastpos

def getDir(a, b):
	c = [b[0]-a[0], b[1]-a[1]]
	if abs(c[0]) >= abs(c[1]):
		t = 1 if c[0] >= 0 else -1
		return (t, 0)
	elif abs(c[0]) < abs(c[1]):
		t = 1 if c[1] >= 0 else -1
		return (0, t)

def reStart(session):
	xy = (session["size"][0], session["size"][1])

	walls = []
	for i in range(session["size"][0]):
		walls.append([i, 0])
		walls.append([i, session["size"][1]-1])
	for i in range(session["size"][1]):
		walls.append([0, i])
		walls.append([session["size"][0]-1, i])

	snake = [getrandXY(xy, walls)]
	pastpos = copy(snake[0])
	target = getrandXY(xy, snake+walls)

	virus = []
	for i in range(int(xy[0]*xy[1]*session["ppl"][0])):
		virus.append(getrandXY(xy, snake+[target]+walls))

	enemy = []
	enemy_pastpos = False
	if session["ppl"][1] >= 1:
		enemy = [getrandXY(xy, walls+snake+[target]+virus)]
		enemy_pastpos = copy(enemy[0])

	score = 0
	move = True
	console_text = []

	return snake, pastpos, target, walls, virus, enemy, enemy_pastpos, score, move, console_text

def getSession(game):
	game = jsOpen("src/default.json")[game]
	session = game["session"]
	constext = game["constext"]
	color = game["color"]
	PIX = session["pix"]
	SU = session["pix"]/8
	path = "src/"+session["src"]
	text_size = int(PIX/1.5)
	return session, constext, color, PIX, SU, path, text_size