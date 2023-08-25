import pygame
import random

# Инициализация Pygame
pygame.init()

# Размер окна
width = 640
height = 480

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка")
# Текущая версия игры
current_version = "1.2"
# Словарь с версиями и их описаниями
version_changes = {
    "1.0": "Добавлено меню и версии игры.",
    "1.1": "Исправлены небольшие ошибки.",
    "1.2": "Добавлен счётчик очков и экран поражения.",
}
# Задайте значение для cell_size перед использованием в функции move_snake
cell_size = 20  # Замените это значение на то, которое соответствует вашей игре


def move_snake(snake_head, snake_position, border_behavior):
    new_snake_head = [snake_head[0] + snake_position[0][0], snake_head[1] + snake_position[0][1]]

    if border_behavior == "wrap":
        new_snake_head[0] = (new_snake_head[0] + cell_size) % cell_size
        new_snake_head[1] = (new_snake_head[1] + cell_size) % cell_size
    else:
        if new_snake_head[0] < 0:
            new_snake_head[0] = cell_size - 1
        elif new_snake_head[0] >= cell_size:
            new_snake_head[0] = 0

        if new_snake_head[1] < 0:
            new_snake_head[1] = cell_size - 1
        elif new_snake_head[1] >= cell_size:
            new_snake_head[1] = 0

    snake_position.insert(0, new_snake_head)
    snake_position.pop()


def show_menu():
    menu = True
    while menu:
        screen.fill(black)
        draw_text(screen, "Змейка", 64, width // 2, height // 4, white)

        play_button = pygame.Rect(width // 2 - 75, height // 2 - 50, 150, 50)
        settings_button = pygame.Rect(width // 2 - 75, height // 2 + 10, 150, 50)
        versions_button = pygame.Rect(width // 2 - 75, height // 2 + 70, 150, 50)  # Добавлена кнопка версий
        exit_button = pygame.Rect(width // 2 - 75, height // 2 + 130, 150, 50)  # Сдвинута кнопка выхода

        pygame.draw.rect(screen, white, play_button)
        pygame.draw.rect(screen, white, settings_button)
        pygame.draw.rect(screen, white, versions_button)  # Отрисовка кнопки версий
        pygame.draw.rect(screen, white, exit_button)

        draw_text(screen, "Играть", 32, width // 2, height // 2 - 25, black)
        draw_text(screen, "Настройки", 32, width // 2, height // 2 + 35, black)
        draw_text(screen, "Версии", 32, width // 2, height // 2 + 95, black)  # Текст кнопки версий
        draw_text(screen, "Выход", 32, width // 2, height // 2 + 155, black)  # Сдвинут текст кнопки выхода

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    game_loop()
                elif settings_button.collidepoint(event.pos):
                    show_settings()
                    menu = False
                elif versions_button.collidepoint(event.pos):  # Обработка нажатия на кнопку версий
                    show_versions()
                    menu = False
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()


def show_versions():
    versions = True
    version_offset = 0
    version_step = 100
    button_spacing = 60  # Увеличен отступ между версиями и кнопкой "Назад"

    while versions:
        screen.fill(black)
        draw_text(screen, "Версии игры", 48, width // 2, 50, white)

        version_index = 0
        for version, changes in version_changes.items():
            if version_index >= version_offset and version_index < version_offset + height // version_step - 1:
                draw_text(screen, f"Версия {version}", 24, width // 2,
                          150 + (version_index - version_offset) * version_step, white)
                draw_text(screen, changes, 20, width // 2, 180 + (version_index - version_offset) * version_step, white)
            version_index += 1

        back_button = pygame.Rect(10, height - button_spacing, 100, 50)  # Перенесена кнопка назад в левый нижний угол
        pygame.draw.rect(screen, white, back_button)
        draw_text(screen, "Назад", 24, 60, height - button_spacing + 25,
                  black)  # Перенесена кнопка назад в левый нижний угол

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    versions = False
            if event.type == pygame.MOUSEWHEEL:
                version_offset -= event.y

                if version_offset < 0:
                    version_offset = 0
                elif version_offset > len(version_changes) - height // version_step + 1:
                    version_offset = len(version_changes) - height // version_step + 1


# Функция для отображения текста на экране
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def show_game_over(score, reason):
    game_over = True
    while game_over:
        screen.fill(black)
        draw_text(screen, "Поражение", 48, width // 2, height // 4, white)

        draw_text(screen, f"Очки: {score}", 24, width // 2, height // 2 - 30, white)
        draw_text(screen, f"Причина: {reason}", 24, width // 2, height // 2, white)

        button_menu = pygame.Rect(width // 2 - 50, height // 2 + 50, 100, 50)
        pygame.draw.rect(screen, white, button_menu)
        draw_text(screen, "Меню", 24, width // 2, height // 2 + 75, black)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_menu.collidepoint(event.pos):
                    game_over = False


# Основная функция игры
def game_loop():
    # Начальные координаты головы змейки
    snake_x = width // 2
    snake_y = height // 2

    # Начальные координаты еды
    food_x = random.randrange(0, width, 10)
    food_y = random.randrange(0, height, 10)

    # Скорость змейки
    snake_speed = 15

    # Начальная длина змейки
    snake_length = 1
    snake_list = []

    # Направление движения
    direction = 'RIGHT'
    change_to = direction
    score = 0
    # Игровой цикл
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Изменение направления движения
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Движение змейки
        if direction == 'UP':
            snake_y -= 10
        if direction == 'DOWN':
            snake_y += 10
        if direction == 'LEFT':
            snake_x -= 10
        if direction == 'RIGHT':
            snake_x += 10

        # Обработка столкновения с краем экрана
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            show_game_over(score, "Змейка вышла за поле")
            game_over = True

        # Добавление координат головы в список змейки
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        # Управление длиной змейки
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Обработка столкновения с самой собой
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        # Генерация новых координат еды и увеличение длины змейки
        if snake_x == food_x and snake_y == food_y:
            food_x = random.randrange(0, width, 10)
            food_y = random.randrange(0, height, 10)
            snake_length += 1
            score += 10

        # Отрисовка на экране
        screen.fill(black)
        for segment in snake_list:
            pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], 10, 10))

        pygame.draw.rect(screen, white, pygame.Rect(food_x, food_y, 10, 10))

        # Обновление экрана
        pygame.display.update()

        # Ограничение скорости
        pygame.time.Clock().tick(snake_speed)

    # Закрытие Pygame
    pygame.quit()
    quit()


def show_settings():
    settings = True
    snake_speed = 15  # Скорость змейки по умолчанию
    border_behavior = "teleport"  # По умолчанию змейка переносится на противоположную сторону

    while settings:
        screen.fill(black)
        draw_text(screen, "Настройки", 48, width // 2, 50, white)

        draw_text(screen, f"Скорость змейки: {snake_speed}", 24, width // 2, height // 2 - 30, white)
        draw_text(screen, f"Поведение при выходе за границу: {border_behavior}", 20, width // 2, height // 2, white)

        snake_speed_up_button = pygame.Rect(width // 2 - 75, height // 2 + 50, 150, 50)
        snake_speed_down_button = pygame.Rect(width // 2 - 75, height // 2 + 110, 150, 50)
        border_behavior_button = pygame.Rect(width // 2 - 125, height // 2 + 170, 250, 50)
        back_button = pygame.Rect(10, height - 60, 100, 50)

        pygame.draw.rect(screen, white, snake_speed_up_button)
        pygame.draw.rect(screen, white, snake_speed_down_button)
        pygame.draw.rect(screen, white, border_behavior_button)
        pygame.draw.rect(screen, white, back_button)

        draw_text(screen, "Увеличить", 24, width // 2, height // 2 + 75, black)
        draw_text(screen, "Уменьшить", 24, width // 2, height // 2 + 135, black)
        draw_text(screen, "Изменить поведение", 24, width // 2, height // 2 + 195, black)
        draw_text(screen, "Назад", 24, 60, height - 35, black)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if snake_speed_up_button.collidepoint(event.pos):
                    snake_speed += 5
                elif snake_speed_down_button.collidepoint(event.pos):
                    snake_speed -= 5
                    if snake_speed < 5:
                        snake_speed = 5
                elif border_behavior_button.collidepoint(event.pos):
                    if border_behavior == "teleport":
                        border_behavior = "wrap"
                    else:
                        border_behavior = "teleport"
                elif back_button.collidepoint(event.pos):
                    settings = False

        screen.fill(black)

    # Запуск меню
    show_menu()



# Запуск игры
show_menu()