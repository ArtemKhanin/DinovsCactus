
import pygame as pg   # библиотека PyGame
import random         # библиотека Рандомных чисел

pg.init()            # инизиализация библиотеки PyGame

display_width = 800      # ширина дисплея игры
display_height = 600     # высота дисплея игры
icon = pg.image.load("icon_dino.png")    # иконка в верхнем левом углу с названием игры

display = pg.display.set_mode ((display_width, display_height)) #инизиализация дисплея игры
pg.display.set_caption ("Динозавр против Кактусов!") #инизиализация название дисплея игры
pg.display.set_icon(icon)    # инизиализация иконки игры

pg.mixer.music.load('track1.mp3')
pg.mixer.music.set_volume(0.4)

fall_sound = pg.mixer.Sound('dino_fall.wav')
crashed_sound = pg.mixer.Sound('dino_crashed.wav')
jump_sound = pg.mixer.Sound('dino_AaRrr.wav')
run_sound = pg.mixer.Sound('dino_run.wav')
loss_sound = pg.mixer.Sound('loss.wav')
healthUp_sound = pg.mixer.Sound('healthUp_sound.wav')

dino_width = 92      # Ширина Динозавра
dino_height = 92     # Высота Динозавра
dino_x = display_width - 600   # точка по координате Х (положение динозавра)
dino_y = display_height - 192 # точка по координате Y (положение динозавра)

dino_image = [pg.image.load('dino0.png'), pg.image.load('dino1.png'), pg.image.load('dino2.png'), 
              pg.image.load('dino3.png'),pg.image.load('dino4.png'), pg.image.load('dino5.png')]  
""" массив картинок динозавра покадрово"""
image_counter = 0
cactus_image = [pg.image.load('cactus0.png'), pg.image.load('cactus1.png'), 
                pg.image.load('cactus2.png'), pg.image.load('cactus3.png')]
"""Присваиваю переменную - массив, который подгружает различной величины картинки кактусов"""
cactus_options = [99, 365, 34, 429, 63, 390, 68, 380]
stone_image = [pg.image.load('stone0.png'), pg.image.load('stone1.png'), pg.image.load('stone2.png')] # массив картинок камней
bird_image = [pg.image.load('bird0.png'), pg.image.load('bird1.png')] # массив картинок птичек
cloud_image = [pg.image.load('cloud0.png'), pg.image.load('cloud1.png')] # массив картинок облачек
heart_image = pg.image.load('heart.png')

clock = pg.time.Clock()
make_jump = False    # при бездействии прыжок не делается
jump_counter = 30   # скорость прыжка
scores = 0
max_scores = 0
max_above = 0
heart = 3



class Object: 
    def __init__(self, x, y, width, image, speed):#функция инизиализации класса КАКТУС
    	self.x = x
    	self.y = y
    	self.width = width
    	self.image = image
    	self.speed = speed
    def move (self):        # функция движения Кактусов
    	if self.x >= -self.width:
    		display.blit(self.image, (self.x, self.y))
    		self.x -= self.speed
    		return True
    	else:
    		return False
    def return_self(self, radius, y, width, image):   # функция возвращающая радиус
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

def run_game ():             # основная функция игры
    global make_jump         # глобальные переменные
    pg.mixer.Sound.play(run_sound)
    run_sound.set_volume(0.6)
    pg.mixer.music.play(-1)
    game = True        # запуск игры
    cactus_arr = []         # масссив Кактусов
    create_cactus_arr(cactus_arr) # вызов создание массива Кактусов
    background = pg.image.load("background.png") # фон дисплея игры
    stone, cloud, bird = op_rand_odject()
    heart = Object(display_width, 250, 50, heart_image, 6)
   
    while game:                 #  основной цикл игры
        for event in pg.event.get():
            if event.type == pg.QUIT:  # при нажатии на КРАСНЫЙ КРЕСТИК закрывается игра
                pg.quit()  
                quit()       
        key = pg.key.get_pressed() # переменная для вызова клавиш клавиатуры
        if key[pg.K_SPACE]:    #  при нажатии на ПРОБЕЛ,
            make_jump = True   #  делается прыжок
        if key[pg.K_ESCAPE]:   #  при нажатии на Ескейп,
            pause()            #  цикл игры становиться на Паузу
        if make_jump:      #  делается прыжок
            jump()


        count_scores(cactus_arr)
        
        display.blit(background, (0, 0)) # цвет фона дисплея игры
        print_text('Очков: ' + str(scores), 5, 5, (102,205,170), 50)
        print_text('Space - прыжок', 5, display_height - 150, (242, 10, 10), 25)
        print_text('Escape - пауза', 5, display_height - 125, (242, 10, 10), 25) 
        heart.move()
        show_heart()
        draw_array(cactus_arr)   # рисуется массив Кактусов
        move_objects(stone, cloud, bird)
        draw_dino()  # Рисует Динозавра
        health_plus(heart)
        if check_collision(cactus_arr):
            pg.mixer.music.stop()
            pg.mixer.Sound.stop(run_sound)
            run_sound.set_volume(0.6)
            if not check_health():
                game = True
            else:
                game = False
        
        pg.display.update()    # обновление дисплея игры
        clock.tick(30)   # временная скорость(сложность игры) 
    return game_over()
        
def jump():                #  функция прыжка
    global dino_y, jump_counter, make_jump   # глобальные переменные
    if jump_counter >= -30:   # высота прыжка
        if jump_counter == 30:
            #pg.mixer.music.pause()
            pg.mixer.Sound.stop(run_sound)
            pg.mixer.Sound.play(jump_sound)
            jump_sound.set_volume(0.2)
        if jump_counter == - 26:
            #pg.mixer.music.unpause()
            pg.mixer.Sound.play(run_sound)
            run_sound.set_volume(0.6)
            pg.mixer.Sound.play(fall_sound)
        dino_y -= jump_counter/2.3 
        jump_counter -= 1      # скорость прыжка
    else:
        jump_counter = 30
        make_jump = False

def create_cactus_arr(array):           # создание экземпляра класса Кактус
	choice = random.randrange(0, 4)      # 1 кактус
	image = cactus_image[choice]
	width = cactus_options[choice * 2]
	height = cactus_options[choice * 2 + 1]
	array.append(Object(display_width - 50, height, width, image, 5))

	choice = random.randrange(0, 4)        # 2 кактус
	image = cactus_image[choice]
	width = cactus_options[choice * 2]
	height = cactus_options[choice * 2 + 1]
	array.append(Object(display_width + 300, height, width, image, 5))

	choice = random.randrange(0, 4)   # 3 кактус
	image = cactus_image[choice]
	width = cactus_options[choice * 2]
	height = cactus_options[choice * 2 + 1]
	array.append(Object(display_width + 600, height, width, image, 5))

	choice = random.randrange(0, 4)    # 4 кактус
	image = cactus_image[choice]
	width = cactus_options[choice * 2]
	height = cactus_options[choice * 2 + 1]
	array.append(Object(display_width + 900, height, width, image, 5))

def find_radius(array):       # функция поиска радиуса
	maximum = max(array[0].x, array[2].x)
	if maximum < display_width: #если макс. растояние между кактусами < ширины поля
		radius = display_width    # радиус равен ширины дисплея игры
		if radius - maximum < 50: #если радиус - максимум < 50, 
			radius += 90         #и радиус больше или равен 150 то
	else:
		radius = maximum          # радиус равен максимуму

	choice = random.randrange(0, 5)   # выбор равен рандомное число от 0 до 5 включительно
	if choice == 0:
		radius += random.randrange(10,15)
	else:
		radius += random.randrange(300,350)
	return radius

def draw_array(array):       # функция прорисовки кактуса
	for cactus in array:
		check = cactus.move()
		if not check:
			object_return(array, cactus)
	        			
def op_rand_odject ():    # открытие рандомных обьектов
    choice = random.randrange(0, 3)
    image_stone = stone_image[choice]

    choice = random.randrange(0, 2)
    image_cloud = cloud_image[choice]
    

    choice = random.randrange(0, 2)
    image_bird = bird_image[choice]

    stone = Object(display_width, display_height - 40 - random.randrange(0, 40), 55, image_stone, 4)


    cloud = Object(display_width, 110, 30, image_cloud, 3)
    bird = Object(display_width, 70, 165, image_bird, 6)

    return stone, cloud, bird

def move_objects (stone, cloud, bird):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 3)
        image_stone = stone_image[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 60), 55, image_stone)
        
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        image_cloud = cloud_image[choice]
        cloud.return_self(display_width, 90 + random.randrange(10, 30), 30, image_cloud)

    check = bird.move()
    if not check:
        choice = random.randrange(0, 2)
        image_bird = bird_image[choice]
        bird.return_self(display_width, 40 + random.randrange(10, 30), 165, image_bird)

def draw_dino():
    global image_counter
    if image_counter == 6:
        image_counter = 0
    display.blit(dino_image[image_counter], (dino_x, dino_y))
    image_counter += 1

def print_text(message, x, y, font_color, font_size, font_type = "font_type1.ttf"):
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render (message, True, font_color)
    display.blit (text, (x, y))

def pause():
    paused = True
    while paused:              
        for event in pg.event.get():
            if event.type == pg.QUIT:  
                pg.quit()  
                quit()
        print_text ("Пауза. Нажмите ПРОБЕЛ для продолжения!", 115, 250, (66, 87, 245), 50)
       
        key = pg.key.get_pressed() 
        if key[pg.K_SPACE]:   
            paused = False  

        pg.display.update()
        clock.tick() 

def object_return(objects, object):
	radius = find_radius(objects)
	choice = random.randrange(0, 4)
	image = cactus_image[choice]
	width = cactus_options[choice * 2]
	height = cactus_options[choice * 2 + 1]
	object.return_self(radius, height, width, image)


def check_collision(barriers):
	for barrier in barriers:
		if barrier.width == 99:  #cactus0.png
			if barrier.x + 10 <= dino_x + dino_width - 10 <= barrier.x + barrier.width - 10:  # точка xA0<=хD<=xC0
				if barrier.y + 9 <= dino_y + 15 <= barrier.y + 135:      # точка yD>=yB0
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x + 7 <= dino_x + dino_width - 34 <= barrier.x + 26: # точка xA0<=хC<=xC0
				if barrier.y + 50 <= dino_y + dino_height - 37 <= barrier.y + 135: # точка yB0<=yC<=y+height
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x + 10 <= dino_x + 6 <= barrier.x + barrier.width - 10: # точка xA0<=хA<=xC0
				if barrier.y + 9 <= dino_y + dino_height - 33 <= barrier.y + 135:   # точка yA>=yB0
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			else: 
				if barrier.x + 10 <= dino_x + dino_width - 45 <= barrier.x + barrier.width - 10: # точка xA0<=хB<=xC0
					if barrier.y + 9 <= dino_y + dino_height <= barrier.y + 135:   # точка yB>=yB0
						if check_health():
							object_return(barriers, barrier)
						else:
							return True

		elif barrier.width == 34:  # cactus1.png
			if barrier.x <= dino_x + dino_width - 5 <=  barrier.x + barrier.width - 5:  # точка xA1<=xD<=xC1
				if barrier.y <= dino_y + 15 <= barrier.y + 71:    #точка yD>=yB1
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x <= dino_x + dino_width - 15 <=  barrier.x + barrier.width - 5:  # точка xA1<=xC<=xC1
				if barrier.y <= dino_y + dino_height - 27 <= barrier.y + 71:    #точка yC>=yB1
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x <= dino_x + 6 <=  barrier.x + barrier.width - 5:  # точка xA1<=xA<=xC1
				if barrier.y <= dino_y + dino_height - 33 <= barrier.y + 71:    #точка yA>=yB1
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			else:
				if barrier.x <= dino_x + dino_width - 45 <=  barrier.x + barrier.width - 5:  # точка xA1<=xB<=xC1
					if barrier.y <= dino_y + dino_height - 6 <= barrier.y + 71:    #точка yB>=yB1
						if check_health():
							object_return(barriers, barrier)
						else:
							return True
        
		elif barrier.width == 63:  # cactus2.png
			if barrier.x + 10 <= dino_x + dino_width - 5 <=  barrier.x + barrier.width - 10:  # точка xA2<=xD<=xC2
				if barrier.y <= dino_y + 15 <= barrier.y + 110:    #точка yD>=yB2
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x + 10 <= dino_x + dino_width - 34 <=  barrier.x + barrier.width - 10:  # точка xA2<=xC<=xC2
				if barrier.y <= dino_y + dino_height - 37 <= barrier.y + 110:    #точка yC>=yB2
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			elif barrier.x + 10 <= dino_x + 6 <=  barrier.x + barrier.width - 10:  # точка xA2<=xA<=xC2
				if barrier.y <= dino_y + dino_height - 33 <= barrier.y + 110:    #точка yA>=yB2
					if check_health():
						object_return(barriers, barrier)
					else:
						return True
			else:
				if barrier.x + 10 <= dino_x + dino_width - 45 <=  barrier.x + barrier.width - 10:  # точка xA2<=xB<=xC2
					if barrier.y <= dino_y + dino_height - 6 <= barrier.y + 110:    #точка yB>=yB2
						if check_health():
							object_return(barriers, barrier)
						else:
							return True
       
		else:
			if barrier.width == 68:  # cactus3.png
				if barrier.x + 5 <= dino_x + dino_width - 10 <=  barrier.x + barrier.width - 5:  # точка xA3<=xD<=xC3
					if barrier.y + 10 <= dino_y + 15 <= barrier.y + 120:    #точка yD>=yB3
						if check_health():
							object_return(barriers, barrier)
						else:
							return True
				elif barrier.x + 5 <= dino_x + dino_width - 34 <=  barrier.x + barrier.width - 5:  # точка xA3<=xC<=xC3
					if barrier.y + 10 <= dino_y + dino_height - 37 <= barrier.y + 120:    #точка yC>=yB3
						if check_health():
							object_return(barriers, barrier)
						else:
							return True
				elif barrier.x + 5 <= dino_x + 6 <=  barrier.x + barrier.width - 5:  # точка xA3<=xA<=xC3
					if barrier.y + 10 <= dino_y + dino_height - 33 <= barrier.y + 120:    #точка yA>=yB3
						if check_health():
							object_return(barriers, barrier)
						else:
							return True
				else:
					if barrier.x + 5 <= dino_x + dino_width - 45 <=  barrier.x + barrier.width - 5:  # точка xA3<=xB<=xC3
						if barrier.y + 10 <= dino_y + dino_height - 6 <= barrier.y + 120:    #точка yB>=yB3
							if check_health():
								object_return(barriers, barrier)
							else:
								return True
	                   
	return False

def count_scores(barriers):
    global scores, max_above #above_cactus
       
    above_cactus = 0
    if - 20 <= jump_counter < 25:
        for barrier in barriers:
            if dino_y + dino_height - 5 <= barrier.y:
                if barrier.x <= dino_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= dino_x + dino_width <= barrier.x + barrier.width:
                    above_cactus += 1
        max_above = max(max_above, above_cactus) 
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0

def game_over():
    global scores, max_scores
    gamestop = True
    while gamestop:              
        for event in pg.event.get():
            if event.type == pg.QUIT:  
                pg.quit()  
                quit()
        print_text ('Конец игры!', 350, 115, (242, 10, 10), 35)
        print_text ('Твой динозавр пошел доставать иголки!', 250, 150, (242, 10, 10), 35)
        print_text ('Нажмите на "Enter" чтобы он вернулся или на "ESCAPE" чтобы выйти!', 45, 200, (242, 10, 10), 35)
        pg.mixer.Sound.stop(run_sound)
        run_sound.set_volume(0.6)
        if scores > max_scores or scores == max_scores:
            max_scores = scores
            print_text ('Молодец, твой новый рекорд равен: ' + str(max_scores) + '!', 150, 300, (75, 0, 130), 50)
          
        else: 
            if scores < max_scores:
                print_text ('Максимальное количесвто очков: ' + str(max_scores) + '!', 150, 300, (75, 0, 130), 50)
                print_text ('А у тебя: ' + str(scores) + '. Старайся лучше и ты сможешь!', 100, 350, (75, 0, 130), 50)
        key = pg.key.get_pressed() 
        if key[pg.K_RETURN]:   
            return True 
        if key[pg.K_ESCAPE]:   
            return False  
        pg.display.update()
        clock.tick() 

def show_heart():
	global heart
	show = 0
	heart_x = 550
	while show != heart:
		display.blit(heart_image, (heart_x, 10))
		heart_x += 55
		show += 1

def check_health():
	global health, heart
	heart -= 1
	if heart == 0:
		pg.mixer.Sound.play(loss_sound)
		game_over()
	else:
		pg.mixer.Sound.play(crashed_sound)
		crashed_sound.set_volume(0.6)
		return True

def health_plus(heart):
	global dino_x, dino_y, dino_width, dino_height
	
	if dino_x <= heart.x <= dino_x + dino_width:
		if dino_y <= heart.y <= dino_y + dino_height:
			pg.mixer.Sound.play(healthUp_sound)
			healthUp_sound.set_volume(0.6)
			#if health < 5:
			#	health += 1
			
			radius = display_width + random.randrange (700, 1700)
			heart.return_self(radius, 50 + random.randrange (70, 150), heart.width, heart_image)
				
			
			


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    dino_y = display_height - 192
    heart = 3

pg.quit()
quit()