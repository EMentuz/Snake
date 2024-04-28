import pygame
import random
import sys


def get_eat_coord(coords_list: list) -> tuple:
    """Проверка чтобы коорд еды не равнялись коорд змеи"""
    eat_list = (random.randrange(0, width - speed, speed), random.randrange(0, height - speed, speed))
    while True:
        count = 0
        for i in coords_list:
            if i == eat_list:
                eat_list = (random.randrange(0, width - speed, speed), random.randrange(0, height - speed, speed))
            else:
                count += 1
        if count == len(coords_list):
            break
    return eat_list


def start_values():
    """Задаем начальные значения для новой игры"""
    start_coord = [(100, height / 2), (100 - speed, height / 2), (100 - 2 * speed, height / 2), (100 - 3 * speed, height / 2)]
    return start_coord, 10, 0, 0, get_eat_coord(start_coord), True


pygame.init()  #Инициализация игры

clock = pygame.time.Clock()  # добавление часов внутрь игры, сделаем за 1 сек 15 раз
fps = 10

width = 600
height = 300
screen = pygame.display.set_mode((width, height)) #размеры для экрана, (ширина, высота)
pygame.display.set_caption("Snake Mentuz.Inc") # название окошка
icon = pygame.image.load("image/snake.png")  # подгрузка иконки
pygame.display.set_icon(icon)
speed = 10

coords, x1_change, y1_change, points, eat, gameplay = start_values() # пытаюсь не дублировать код, надеюсь руки за такое не оторвут

font = pygame.font.SysFont(None, 50)  # создание шрифта, шрифт размер
font2 = pygame.font.SysFont(None, 25)
lose_text = font.render('YOU RESULT', True, "RED")  # создание самого текста
restart_text = font.render('RESTART', True, "Yellow")
exit_text = font.render('EXIT', True, "Black")

lose_text_rec = lose_text.get_rect(center=(width / 2, 50))
restart_text_rec = restart_text.get_rect(center=(width / 2, 150))
exit_text_rec = exit_text.get_rect(center=(width / 2, 190))


running = True
while running:
    if gameplay:

        screen.fill((33, 166, 55))  # заливка для фона RGB 255
        points_text = font2.render('Points ' + str(points), True, "Yellow")  # создание самого текста
        screen.blit(points_text, (0, 0))  # вывод текста
        pygame.draw.rect(screen, "White", [eat[0], eat[1], 10, 10])

        for event in pygame.event.get():  # получаем список из всех возможных событий
            if event.type == pygame.QUIT:  # закрытие приложения
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != speed:
                    x1_change = -speed
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -speed:
                    x1_change = speed
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != speed:
                    y1_change = -speed
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -speed:
                    y1_change = speed
                    x1_change = 0

        # Перемещение змейки
        coords[1:] = coords[:len(coords) - 1]
        coords[0] = (coords[0][0] + x1_change, coords[0][1] + y1_change)

        # прохождение змейки через стены
        if coords[0][0] >= width:
            coords[0] = (0, coords[0][1])
        if coords[0][0] < 0:
            coords[0] = (width - speed, coords[0][1])
        if coords[0][1] >= height:
            coords[0] = (coords[0][0], 0)
        if coords[0][1] < 0:
            coords[0] = (coords[0][0], height - speed)

        # рисование всей змейки
        for coord in coords:
            pygame.draw.rect(screen, "White", [coord[0], coord[1], speed, speed])

        # поедание
        if coords[0] == eat:
            coords.append(coords[-1])
            eat = get_eat_coord(coords)
            points += 1

        # проверка на пересечение головы змейки с ее телом
        for el in coords[1:]:
            if el == coords[0]:
                gameplay = False
    else:

        # текст для меню
        points_text = font.render(str(points), True, "Red")
        points_text_rec = points_text.get_rect(center=(width / 2, 90))
        screen.blit(points_text, points_text_rec)
        screen.blit(lose_text, lose_text_rec)
        screen.blit(exit_text, exit_text_rec)
        screen.blit(restart_text, restart_text_rec)


        mouse = pygame.mouse.get_pos()
        if restart_text_rec.collidepoint(mouse) and pygame.mouse.get_pressed()[0]: # Если навели мышь на рестарт и нажали то заново
            #начальные значение если начал заново
            coords, x1_change, y1_change, points, eat, gameplay = start_values()

        elif exit_text_rec.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
        for event in pygame.event.get():  # получаем список из всех возможных событий
            if event.type == pygame.QUIT:  # закрытие приложения
                running = False
                sys.exit()

    pygame.display.update()
    clock.tick(fps)  # добавление часов внутрь игры, сделаем за 1 сек 15 раз

