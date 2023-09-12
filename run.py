# import sys
# sys.path.append("src")
import pg2q as gui
from defout import *

# инициализация игры

MODE = "snakegame"

session, constext, color, PIX, SU, path, text_size = getSession("test")
snake, pastpos, target, walls, virus, enemy, enemy_pastpos, score, move, console_text = reStart(session)
gui_info = {
	"title": "vw_crush {}".format(session["title"]),
	"size": (PIX*(session["size"][0]*2+3), (PIX*(session["size"][1]+2))),
	"fps": session["fps"],
	"speed": session["speed"],
	"color_bg": color["bg"],
	"icon_path": "icon.png",
	"font": session["font"],
	"json_sprites": path+"/sprites.json",
	"sfx_paths": {
		"move": path+"/move.ogg",
		"target": path+"/target.ogg",
		"virus": path+"/virus.ogg",
		"wall": path+"/wall.ogg",
		"move_enemy": path+"/move_enemy.ogg",
		"target_enemy": path+"/target_enemy.ogg"}}
display = gui.Scene(gui_info)

# запуск цикла
run, t = True, 0
while run:
	display.clear()

	# === GRAPHIC -------------------------------------------------------

	if MODE == "snakegame":

		# упаковка координатов к спрайтам
		guipack = {
			"snake_head": [snake[0]],
			"snake_body": snake[1:],
			"target": [target],
			"wall": walls,
			"virus": virus}
		if len(enemy)>0:
			guipack["enemy_head"] = [enemy[0]]
			guipack["enemy_body"] = enemy[1:]
		# отрисовка спрайтов по координатам
		display.drawBox(color["bg_snakegame"], (PIX,PIX), (session["size"][0]*PIX, session["size"][1]*PIX))
		for sprite in guipack:
			for obj in guipack[sprite]:
				display.drawSprite(sprite, (PIX+obj[0]*PIX, PIX+obj[1]*PIX), SU)

		# отрисовка прогрессбара
		display.drawBox(color["bg_progressbar"], ((session["size"][0]+2)*PIX, PIX), (session["size"][0]*PIX, PIX))
		score_percent = int(score/len(constext)*session["size"][0])
		for i in range(score_percent):
			display.drawSprite("load_on", ((session["size"][0]+2+i)*PIX, PIX), SU)
		for i in range(score_percent, session["size"][0]):
			display.drawSprite("load_off", ((session["size"][0]+2+i)*PIX, PIX), SU)
		display.drawText(score, text_size, color["text_progressbar"], ((session["size"][0]+1)*PIX+int(PIX/3), PIX))
		display.drawText(len(constext)-score, text_size, color["text_progressbar"], ((session["size"][0]*2+2)*PIX+int(PIX/3), PIX))

		# отрисовка консоли
		display.drawBox(color["bg_console"], ((session["size"][0]+2)*PIX, 3*PIX), (session["size"][0]*PIX, (session["size"][1]-2)*PIX))
		ii = len(console_text) - (session["size"][1]-2) if len(console_text) > session["size"][1]-2 else 0
		for i in range(ii, len(console_text)):
			display.drawText("info {} => {}".format(i, console_text[i]), text_size, color["text_console"], ((session["size"][0]+2)*PIX, (3+i-ii)*PIX))

		# === KEYBOARD/MOUSE ------------------------------------------------

		# считывание ввода
		key = display.getKey()

		# клавиатура
		if isinstance(key, str):
			if key == "Esc": run = False
			if key == "Space":
				MODE = "snakegame"
				snake, pastpos, target, walls, virus, enemy, enemy_pastpos, score, move, console_text = reStart(session)
				move = True
				score = 0
			# передвижение змейки
			if move:
				if key in ["Left", "Right", "Up", "Down"]:
					if key == "Left" and snake[0][0] > 0:
						snake, pastpos = snakeMove(snake, pastpos)
						snake[0][0] -= 1
					elif key == "Right" and snake[0][0] < session["size"][0]-1:
						snake, pastpos = snakeMove(snake, pastpos)
						snake[0][0] += 1
					elif key == "Up" and snake[0][1] > 0:
						snake, pastpos = snakeMove(snake, pastpos)
						snake[0][1] -= 1
					elif key == "Down" and snake[0][1] < session["size"][1]-1:
						snake, pastpos = snakeMove(snake, pastpos)
						snake[0][1] += 1
					if snake[0] != target:
						display.playSFX("move", .5)

		# мышь
		if isinstance(key, list):
			pass

		# === CHECKING--------------------------------------------------------

		# передвижение врага
		if len(enemy)>0:
			if t%(session["fps"]/session["ppl"][1])==0:
				enemy, enemy_pastpos = snakeMove(enemy, enemy_pastpos)
				direct = getDir(enemy[0], target)
				enemy[0][0] += direct[0]
				enemy[0][1] += direct[1]
				# display.playSFX("move_enemy", .5)
			if enemy[0] == target:
				target = getrandXY((session["size"][0], session["size"][1]), walls+virus)
				enemy.append(copy(enemy_pastpos))
				display.playSFX("target_enemy")
				if len(snake) > 1:
					if score > 0: score -= 1
					snake.pop(-1)
					console_text.pop(-1)
				else:
					if move:
						display.playSFX("wall")
					move = False
					MODE = "gameover"

		for el in snake:
			# обработка столкновения змейки с целью
			if el == target:
				target = getrandXY((session["size"][0], session["size"][1]), walls+virus)
				snake.append(copy(pastpos))
				display.playSFX("target")
				if score < len(constext):
					console_text.append(constext[score])
					score += 1
			# обработка столкновения змейки с вирусом
			elif el in virus:
				if len(snake) > 1:
					if t%10==0:
						if score > 0: score -= 1
						snake.pop(-1)
						console_text.pop(-1)
				display.playSFX("virus")

		# обработка столкновения змейки с хвостом и стенами
		if snake[0] in snake[1:]+walls+enemy:
			if move:
				display.playSFX("wall")
			move = False
			MODE = "gameover"

		# если нужное количество очков набрано
		if score >= len(constext): MODE = "wingame"

	elif MODE == "gameover": 
		display.drawText("You lose: {}/{} ~".format(score, len(constext)), 30, color["text_lose"], (50,50))
		display.drawText("Press [SPACE] for new game", 20, color["text_lose_sub"], (50, 80))

	elif MODE == "wingame":
		display.drawText("You win: {} !".format(score), 30, color["text_win"], (50,50))
		display.drawText("Press [SPACE] for new game", 20, color["text_win_sub"], (50, 80))


	if MODE in ["gameover", "wingame"]:
		key = display.getKey()
		if isinstance(key, str):
			if key == "Esc": run = False
			if key == "Space":
				MODE = "snakegame"
				snake, pastpos, target, walls, virus, enemy, enemy_pastpos, score, move, console_text = reStart(session)
				move = True
				score = 0
		elif isinstance(key, list): pass

	# === ----------------------------------------------------------------

	t = display.update()
del display