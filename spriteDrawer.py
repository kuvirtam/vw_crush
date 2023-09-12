from copy import deepcopy as copy
import pg2q as gui
from os.path import exists
from pathlib import Path

gui_info = {
	"title": "spriteDrawer",
	"size": (480, 360),
	"fps": 30,
	"speed": 1,
	"color_bg": (30,30,30),
	"icon_path": False,
	"font": "arial"
}

# рамки для цвета от 0 до 255
def normalizeColor(color):
	for i in range(3):
		if color[i]<0: color[i] = 0
		elif color[i]>255: color[i] = 255
		else: pass
	return color

# ------------------------------------------------------------

inpath = input(">>")
display = gui.Scene(gui_info)

button_color = {
	"red_m100": ["-100", (0,0)],
	"red_m10": ["-10", (1,0)],
	"red_m1": ["-1", (2,0)],
	"green_m100": ["-100", (0,1)],
	"green_m10": ["-10", (1,1)],
	"green_m1": ["-1", (2,1)],
	"blue_m100": ["-100", (0,2)],
	"blue_m10": ["-10", (1,2)],
	"blue_m1": ["-1", (2,2)],
	"red_p100": ["+100", (5,0)],
	"red_p10": ["+10", (6,0)],
	"red_p1": ["+1", (7,0)],
	"green_p100": ["+100", (5,1)],
	"green_p10": ["+10", (6,1)],
	"green_p1": ["+1", (7,1)],
	"blue_p100": ["+100", (5,2)],
	"blue_p10": ["+10", (6,2)],
	"blue_p1": ["+1", (7,2)],} # кнопки для работы с цветом
button_frames = {
	"frame_left": ["<", (0,0)],
	"frame_right": [">", (1,0)],
	"frame_add": ["+", (0,2)],
	"frame_del": ["-", (1,2)],
	"frame_copy": ["/c", (1,1)]
	} # кнопки для работы с кадрами

button_sprites = {
	"spr_save": ["SAVE->", (0,0)],
	"spr_pack": ["PACK", (0,1)]} # кнопки для работы со спрайтами

# переменные
if exists(inpath+"//sprites.json"):
	SPRITES = gui.jsOpen(inpath+"//sprites.json")
else:
	SPRITES = {}
color = [0,0,0] # цвет
mode = "standart" # режим
r_tag = 200 # тэг для выделения текстового поля
path = "" # название спрайта
canvas = [gui.getTable((8,8), [])] # холст спрайта
frame = 0 # кадр холста
canvas_grid = 1

run, t = True, 0
while run:
	display.clear()

	# === Graphic ---------------------------------------------------------

	# отрисовка панели подбора цвета
	display.drawBox(color, (240,0), (90,90))
	button_color_ranges = display.drawButtonPad(button_color, (0,0), (30,30), text_size=15)
	color_texts = {
		"txt_red": display.drawButton((90,0),(60,30),"R: {}".format(color[0]), 15, (100,0,0), gui_info["color_bg"]),
		"txt_green": display.drawButton((90,30),(60,30),"G: {}".format(color[1]), 15, (0,100,0), gui_info["color_bg"]),
		"txt_blue": display.drawButton((90,60),(60,30),"B: {}".format(color[2]), 15, (0,0,100), gui_info["color_bg"]),}

	# отрисовка текстового поля
	txtin_path = display.drawButton((0,90), (330, 30), path, 15, bg_color=(r_tag,200,150), border=3)

	# отрисовка холста
	canvas_ranges = display.drawCanvas(canvas[frame], (0,120),(30,30), border=canvas_grid)

	# отрисовка панели кадров
	button_frames_ranges = display.drawButtonPad(button_frames, (240,120),(30,30), text_size=20, border=3)
	display.drawText("{}/{}".format(frame, len(canvas)-1), 15, (255,255,255), (240,150))

	# отрисовка кадров под холстом
	display.drawBox((150,0,0), (300,120+frame*30), (30,30))
	for i in range(len(canvas)):
		display.drawCanvas(canvas[i], (303,123+i*30), (3,3), 0)

	# отрисовка панели для работы с холстом/спрайтами
	button_sprites_ranges = display.drawButtonPad(button_sprites, (240,300), (90,30), text_size=25, border=3)

	display.drawBox((50,50,50), (344,15), (3, 330))

	# отрисовка нарисованных спрайтов
	spr_ranges = {}
	i = 0
	for t in SPRITES:
		display.drawText(t, 15, (255,255,255), (360,i*30))
		display.drawCanvas(SPRITES[t][0], (450,i*30), (3,3), 0)
		spr_ranges[t] = [450,450+8*3,i*30,i*30+8*3]
		i += 1

	#  === Key Input -----------------------------------------------------

	key = display.getKey()
	# ввод текста
	if mode == "input":
		if key in ["Esc", "Enter"]:
			mode = "standart"
			r_tag = 200
		elif isinstance(key, str) and key in "qwertyuiopasdfghjklzxcvbnm": path += key
		elif key == "Backspace": path = path[:-1]
		elif key == "Space": path += "_"
	# ---
	elif mode == "standart":
		if key:
			if key == "Esc": run = False
			elif key == "0":
				canvas_grid = 0 if canvas_grid == 1 else 1

			# проверка нажатий кнопок панели подбора цвета и их обработка
			for button in button_color:
				if gui.checkClick(key, button_color_ranges[button]):
					if button == "red_m100": color[0] -= 100
					elif button == "red_m10": color[0] -= 10
					elif button == "red_m1": color[0] -= 1
					elif button == "green_m100": color[1] -= 100
					elif button == "green_m10": color[1] -= 10
					elif button == "green_m1": color[1] -= 1
					elif button == "blue_m100": color[2] -= 100
					elif button == "blue_m10": color[2] -= 10
					elif button == "blue_m1": color[2] -= 1
					elif button == "red_p100": color[0] += 100
					elif button == "red_p10": color[0] += 10
					elif button == "red_p1": color[0] += 1
					elif button == "green_p100": color[1] += 100
					elif button == "green_p10": color[1] += 10
					elif button == "green_p1": color[1] += 1
					elif button == "blue_p100": color[2] += 100
					elif button == "blue_p10": color[2] += 10
					elif button == "blue_p1": color[2] += 1
			color = normalizeColor(color)

			# проверка нажатий на текст показывающих цвет
			for button in color_texts:
				if gui.checkClick(key, color_texts[button]):
					if button == "txt_red":
						if key[0] == "L": color[0] = 0
						elif key[0] == "R": color[0] = 255
					if button == "txt_green":
						if key[0] == "L": color[1] = 0
						elif key[0] == "R": color[1] = 255
					if button == "txt_blue":
						if key[0] == "L": color[2] = 0
						elif key[0] == "R": color[2] = 255

			# проверка нажатия на текстовое поле
			if gui.checkClick(key, txtin_path):
				mode = "input"
				r_tag = 255

			# проверка и обработка нажатия по холсту
			for i in range(len(canvas_ranges)):
				for ii in range(len(canvas_ranges[i])):
					if gui.checkClick(key, canvas_ranges[i][ii]):
						if key[0] == "L": canvas[frame][i][ii] = copy(color)
						elif key[0] == "R": canvas[frame][i][ii] = []
						elif key[0] == "M":
							color = copy(canvas[frame][i][ii])
							if color == []: color = [0,0,0]

			# проверка и обработка нажатия на кнопки управления кадрами
			for button in button_frames:
				if gui.checkClick(key, button_frames_ranges[button]):
					if button == "frame_left"and frame > 0 : frame -= 1
					elif button == "frame_right"and frame < len(canvas)-1: frame += 1
					elif button == "frame_add": 
						canvas.append(gui.getTable((8,8), []))
						frame = len(canvas)-1
					elif button == "frame_del" and len(canvas)>1:
						canvas = canvas[:-1]
						if frame >= len(canvas): frame = len(canvas)-1
					elif button == "frame_copy" and frame != 0: canvas[frame] = copy(canvas[frame-1])

			# проверка и обработка кнопок для сохранения
			for button in button_sprites:
				if gui.checkClick(key, button_sprites_ranges[button]):
					if button == "spr_save" and path != "": 
						SPRITES[path] = copy(canvas)
						canvas = [gui.getTable((8,8), [])]
						frame = 0
						path = ""
					if button == "spr_pack":
						gui.jsSave("C:\\Users\\kuvi\\Desktop\\codes\\python\\vw_crush\\src\\sprites.json", SPRITES)
						run = False

			# проверка и обработка нажатия на спрайты справа
			for button in spr_ranges:
				if gui.checkClick(key, spr_ranges[button]):
					if key[0] == "L":
						canvas = copy(SPRITES[button])
						path = copy(button)
					elif key[0] == "R":
						SPRITES.pop(button)

	# ------------------------------------------------------------

	t = display.update()