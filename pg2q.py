# pygame2Q [InDev 290823]

import pygame as pg
import json

# клавиши pg_code:name
_KEYS = {
	# цифры
	48: "0",
	49: 1,
	50: 2,
	51: 3,
	52: 4,
	53: 5,
	54: 6,
	55: 7,
	56: 8,
	57: 9,
	# буквы
	97: "a",
	98: "b",
	99: "c",
	100: "d",
	101: "e",
	102: "f",
	103: "g",
	104: "h",
	105: "i",
	106: "j",
	107: "k",
	108: "l",
	109: "m",
	110: "n",
	111: "o",
	112: "p",
	113: "q",
	114: "r",
	115: "s",
	116: "t",
	117: "u",
	118: "v",
	119: "w",
	120: "x",
	121: "y",
	122: "z",
	# остальные
	13: "Enter",
	27: "Esc",
	32: "Space",
	8: "Backspace",
	9: "Tab",
	1073741906: "Up",
	1073741905: "Down",
	1073741904: "Left",
	1073741903: "Right",
	45: "-",
	61: "+"}
_MBS = {
	1: "L",
	2: "M",
	3: "R",
	4: "M_Up",
	5: "M_Down"}

# === полезные функции -------------------------------------

# открытие json и забор данных
def jsOpen(path):
	with open(path, "r", encoding="utf-8") as file:
		data = json.load(file)
	return data
# сохранение данных в json
def jsSave(path, data):
	with open(path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=2)

# создание матрицы заполненной одной переменной
def getTable(size, el=0):
	table = []
	for i in range(size[0]):
		table.append([])
		for ii in range(size[1]):
			table[i].append(el)
	return table

# нормализация индекса
def sliceIndex(i, size):
	while True:
		if i >= size: i -= size; continue
		elif i <= -size: i += size; continue
		else: return i

# проверка нажатия мыши в регионе
def checkClick(key, rang):
	try:
		pos = key[1]
	except:
		return False
	else:
		if pos[0] in range(rang[0], rang[1]) and pos[1] in range(rang[2], rang[3]):
			return True
		else:
			return False

# главный класс -----------------------------------------
class Scene:

	# инициализация экрана
	def __init__(self, gui_info):
		# входные данные
		self.title = gui_info["title"] # заголовок
		self.size = gui_info["size"] # размер окна
		self.fps = gui_info["fps"] # скорость обновления экрана в секунду
		self.speed = gui_info["speed"] # скорость анимации (смены фреймов) в секунду
		self.color_bg = gui_info["color_bg"] # цвет фона
		self.icon_path = gui_info["icon_path"] # ссылка на иконку
		self.font = gui_info["font"] # название шрифта

		# сбор файлов json
		if "json_sprites" in gui_info.keys():
			file = jsOpen(gui_info["json_sprites"])
			self.SPR_js = file

		# инициализация звука 
		sound_sfx = "sfx_paths" in gui_info.keys()
		if sound_sfx: pg.mixer.pre_init(44100, -16, 1, 512)

		# инициализация окна
		pg.init() # инициализация графики
		screen = pg.display.set_mode(self.size) # создание и размер экрана
		pg.display.set_caption(self.title) # заголовок
		if self.icon_path: pg.display.set_icon(pg.image.load(self.icon_path)) # иконка
		screen.fill(self.color_bg) # цвет фона
		clock = pg.time.Clock() # задание скорости обнволения экрана

		sound_mus = "music_paths" in gui_info.keys()
		if sound_mus:
			self.music_paths = gui_info["music_paths"]
		if sound_sfx:
			self.sfx_pack = {}
			for key in gui_info["sfx_paths"]:
				self.sfx_pack[key] = pg.mixer.Sound(gui_info["sfx_paths"][key])

		# переменные для других функций
		self.clock = clock # скорость экрана
		self.screen = screen # сам экран
		self.t = 0 # счетчик
		self.a = 0 # счетчик фреймов

	# удаление сцены
	def __del__(self):
		pass 

	# == экран

	# очистка экрана
	def clear(self):
		self.screen.fill(self.color_bg)

	# обновление экрана (возвращает номер счетчика)
	def update(self):

		# скорость экрана и счетчик
		self.clock.tick(self.fps)
		if self.t < self.fps-1: self.t += 1
		else: self.t = 0

		# скорость анимации
		if self.t%(self.fps/self.speed)==0: self.a += 1
		if self.a < self.fps-1: pass
		else: self.a = 0

		# отрисовка экрана
		pg.display.update()
		# возвращение счетчика
		return self.t

	# == действия со стороны пользователя

	# получение нажатых клавиш
	def getKey(self):
		try: cmd = pg.event.get()[0]
		except: return False
		else:
			if cmd.type == pg.KEYDOWN:
				try:
					return _KEYS[cmd.key]
				except:
					return "Unknown key [{}]".format(cmd.key)
			elif cmd.type == pg.MOUSEBUTTONDOWN:
				return [_MBS[cmd.button], cmd.pos]

	# == отрисовка

	# отрисовка текста на экране
	def drawText(self, text, size, color, xy):
		f = pg.font.SysFont(self.font, size)
		textout = f.render(str(text), 1, color)
		self.screen.blit(textout, xy)

	# отрисовка прямоугольника на экране
	def drawBox(self, color, xy, size):
		pg.draw.rect(self.screen, color, xy+size)

	# отрисовка спрайта из json
	def drawSprite(self, name, xy, sizeup):
		frames = self.SPR_js[name]
		frame = sliceIndex(self.a, len(frames))
		canvas = frames[frame]
		for i in range(len(canvas)):
			for ii in range(len(canvas[i])):
				if canvas[i][ii] != []:
					x = xy[0]+i*sizeup
					y = xy[1]+ii*sizeup
					self.drawBox(canvas[i][ii], (x, y), (sizeup, sizeup))

	# отрисовка матрицы со спрайтами
	def drawSpriteField(self, data, xy, size, sizeup):
		for i in range(len(data)):
			for ii in range(len(data[i])):
				if data[i][ii] != 0:
					x = xy[0]+i*sizeup*size
					y = xy[1]+ii*sizeup*size
					self.drawSprite(data[i][ii], (x, y), sizeup)

	# == отрисовка с возвратом

	# отрисовка кнопки (фона и текста) с возвращением 
	def drawButton(self, xy, size, text, text_size=10, text_color=(0,0,0), bg_color=(200,200,200), border=1):
		x = xy[0]+border
		y = xy[1]+border
		self.drawBox(bg_color, (x, y), (size[0]-2*border, size[1]-2*border))
		self.drawText(text, text_size, text_color, (x, y))
		range_xy = [x, x+size[0]-2*border, y, y+size[1]-2*border]
		return range_xy

	# отрисовка панели кнопок с возвращением
	def drawButtonPad(self, buttons, xy, button_size, text_size=10, text_color=(0,0,0), bg_color=(200,200,200), border=1):
		ranges = {}
		for key in buttons.keys():
			x = xy[0] + buttons[key][1][0]*button_size[0]
			y = xy[1] + buttons[key][1][1]*button_size[1]
			ranges[key] = self.drawButton((x,y), button_size, buttons[key][0], text_size, text_color, bg_color, border)
		return ranges

	# отрисовка холста
	def drawCanvas(self, data, xy, cell_size, border=1):
		ranges = []
		cell_size_t = (cell_size[0]-2*border, cell_size[1]-2*border)
		for i in range(len(data)):
			ranges.append([])
			for ii in range(len(data[i])):
				if data[i][ii] == []: color = (50,50,50)
				else: color = data[i][ii]
				cell_xy = ((xy[0]+i*cell_size[0])+border, (xy[1]+ii*cell_size[1])+border)
				self.drawBox(color, cell_xy, cell_size_t)
				ranges[i].append([cell_xy[0], cell_xy[0]+cell_size_t[0], cell_xy[1], cell_xy[1]+cell_size_t[1]])
		return ranges

	# отрисовка таблицы
	def drawTable(self, data, xy, cell_size, cell_color=(255,255,255), text_color=(0,0,0), text_size=10, border=0):
		ranges = []
		for i in range(len(data)):
			ranges.append([])
			for ii in range(len(data[i])):
				x = xy[0]+i*cell_size[0]
				y = xy[1]+ii*cell_size[1]
				ranges[i].append(self.drawButton((x, y), cell_size, data[i][ii], text_size, text_color, cell_color, border))
		return ranges

	# == воспроизведение звука

	# включить фоновый звук
	def playBG(self, name, volume=1, loop=1, fade=1000):
		pg.mixer.music.load(self.music_paths[name])
		pg.mixer.music.play(loop, 0, fade)
		pg.mixer.music.set_volume(volume)

	# остановить фоновый звук
	def stopBG(self):
		pg.mixer.music.stop()

	# воспроизвести звуковой эффект
	def playSFX(self, name, volume=1):
		self.sfx_pack[name].set_volume(volume)
		self.sfx_pack[name].play(0, 0, 0)