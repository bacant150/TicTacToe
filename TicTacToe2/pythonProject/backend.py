import pygame
import sys
import random
import tkinter as tk
from tkinter import filedialog

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def choose_background_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Виберіть файл фону", filetypes=[("Картинка", "*.png *.jpg")])
    return file_path

def choose_difficulty():
    screen.blit(main_menu_bg, (0, 0))

    font = pygame.font.SysFont(None, 50)
    easy_button = font.render('Easy', True, BLACK)
    medium_button = font.render('Medium', True, BLACK)
    hard_button = font.render('Hard', True, BLACK)
    impossible_button = font.render('Impossible', True, BLACK)
    friend_button = font.render('Play with friend', True, BLACK)  # Добаввляємо кнопку для гри с другом

    easy_button_rect = easy_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    medium_button_rect = medium_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    hard_button_rect = hard_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    impossible_button_rect = impossible_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    friend_button_rect = friend_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # Рорзміщаємо кнопку

    screen.blit(easy_button, easy_button_rect)
    screen.blit(medium_button, medium_button_rect)
    screen.blit(hard_button, hard_button_rect)
    screen.blit(impossible_button, impossible_button_rect)
    screen.blit(friend_button, friend_button_rect)  # Відображаємо кнопку

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if easy_button_rect.collidepoint(x, y):
                    return bot_easy_move
                elif medium_button_rect.collidepoint(x, y):
                    return bot_medium_move
                elif hard_button_rect.collidepoint(x, y):
                    return bot_hard_move
                elif impossible_button_rect.collidepoint(x, y):
                    return bot_impossible_move
                elif friend_button_rect.collidepoint(x, y):  # Обробляємо кнопку
                    play_with_friend()  # Запуск гри з другом


# Функція для гри з другом
def play_with_friend():
    global game_over, board
    game_over = False
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'  # Перший ход

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)
                if board[row][col] == '':  # Пеервірка на пусту клітинку
                    board[row][col] = current_player  # Ход теперішнього гравця
                    if check_win_or_draw():
                        show_endgame_menu()
                        game_over = True
                        break
                    current_player = 'O' if current_player == 'X' else 'X'  # Переключення до наступного гравця
        show_game()

    show_endgame_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 < x < WIDTH // 2 + 100 and HEIGHT // 2 - 75 < y < HEIGHT // 2 - 25:
                    play_with_friend()  # Перезапуск гри, якщо користувач вибрав
                elif WIDTH // 2 - 250 < x < WIDTH // 2 + 250 and HEIGHT // 2 + 25 < y < HEIGHT // 2 + 75:
                    main_menu()  # Вертаємося в головне меню, якщо користувач вибрав


def bot_easy_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    return random.choice(empty_cells) if empty_cells else None


def bot_medium_move():
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                if check_win_or_draw():
                    return i, j
                board[i][j] = ''
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'X'
                if check_win_or_draw():
                    board[i][j] = 'O'
                    return i, j
                board[i][j] = ''
    return bot_easy_move()

def minimax(board, depth, is_maximizing):
    result = check_win_or_draw()
    if result is not None:
        if result == 'X':
            return -10 + depth
        elif result == 'O':
            return 10 - depth
        else:
            return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def minimax_ab(board, depth, is_maximizing, alpha, beta):
    result = check_win_or_draw()
    if result is not None:
        if result == 'X':
            return -10 + depth
        elif result == 'O':
            return 10 - depth
        else:
            return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax_ab(board, depth + 1, False, alpha, beta)
                    board[i][j] = ''
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax_ab(board, depth + 1, True, alpha, beta)
                    board[i][j] = ''
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def bot_hard_move():
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def bot_impossible_move():
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax_ab(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def make_move(row, col):
    global current_player, game_over
    if not game_over and board[row][col] == '':
        board[row][col] = current_player
        if check_win_or_draw():
            show_endgame_menu()
            game_over = True
            return
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

        # Хід бота
        if not game_over and current_player == 'O':
            bot_row, bot_col = bot_easy_move()
            if bot_row is not None and bot_col is not None:
                make_move(bot_row, bot_col)


# Екран
SCREEN_INFO = pygame.display.Info()
WIDTH, HEIGHT = SCREEN_INFO.current_w, SCREEN_INFO.current_h

# Fullscreen resolution
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Хрестики та нулики')

# Фон гри
main_menu_bg = pygame.image.load('images.png')
main_menu_bg = pygame.transform.scale(main_menu_bg, (WIDTH, HEIGHT))
game_bg = pygame.image.load('images.png')
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Змінні
current_player = 'X'
board = [['' for _ in range(3)] for _ in range(3)]
game_over = False

CROSS_SIZE = (min(WIDTH, HEIGHT) // 6 + 20) // 2
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 6 - 20



def show_main_menu():
    screen.blit(main_menu_bg, (0, 0))

    font = pygame.font.SysFont(None, 50)
    play_button = font.render('Play', True, BLACK)
    exit_button = font.render('Exit', True, BLACK)
    background_button = font.render('Change Background', True, BLACK)  # Зміна фона
    play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    exit_button_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    background_button_rect = background_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Розміщаємо кнопку
    screen.blit(play_button, play_button_rect)
    screen.blit(exit_button, exit_button_rect)
    screen.blit(background_button, background_button_rect)  # Відображення кнопки

    pygame.display.update()


def show_game():
    screen.blit(game_bg, (0, 0))
    draw_board()
    pygame.display.update()

def draw_board():
    pygame.draw.line(screen, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)

    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol == 'X':
                draw_X(row, col)
            elif symbol == 'O':
                draw_O(row, col)

# Малюємо хрестики
def draw_X(row, col):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.line(screen, BLACK, (x - CROSS_SIZE, y - CROSS_SIZE), (x + CROSS_SIZE, y + CROSS_SIZE), 5)
    pygame.draw.line(screen, BLACK, (x + CROSS_SIZE, y - CROSS_SIZE), (x - CROSS_SIZE, y + CROSS_SIZE), 5)

# Малюємо нулики
def draw_O(row, col):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.circle(screen, BLACK, (x, y), CIRCLE_RADIUS, 5)

# Перевірка на нічию
def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                return False
    return True

# Перевірка на перемогу чи програщ
def check_win_or_draw():
    global game_over
    if check_draw():
        game_over = True
        return True
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            pygame.draw.line(screen, BLACK, (0, row * HEIGHT // 3 + HEIGHT // 6),
                             (WIDTH, row * HEIGHT // 3 + HEIGHT // 6), 5)
            game_over = True
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            pygame.draw.line(screen, BLACK, (col * WIDTH // 3 + WIDTH // 6, 0), (col * WIDTH // 3 + WIDTH // 6, HEIGHT),
                             5)
            game_over = True
            return True
    if board[0][0] == board[1][1] == board[2][2] != '':
        pygame.draw.line(screen, BLACK, (50, 50), (WIDTH - 50, HEIGHT - 50), 5)
        game_over = True
        return True
    if board[0][2] == board[1][1] == board[2][0] != '':
        pygame.draw.line(screen, BLACK, (WIDTH - 50, 50), (50, HEIGHT - 50), 5)
        game_over = True
        return True
    return False

# Відображення після ігрового вікна
def show_endgame_menu():
    font = pygame.font.SysFont(None, 50)
    play_again_button = font.render('Play again', True, BLACK)
    main_menu_button = font.render('Exit to main menu', True, BLACK)

    play_again_button_rect = play_again_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    main_menu_button_rect = main_menu_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(play_again_button, play_again_button_rect)
    screen.blit(main_menu_button, main_menu_button_rect)

    pygame.display.update()

# Зміна фону
def change_background():
    global game_bg
    file_path = choose_background_file()
    if file_path:
        game_bg = pygame.image.load(file_path)
        game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Запуск гри
def run_game():
    global game_over, current_player, board
    game_over = False
    current_player = 'X'
    board = [['' for _ in range(3)] for _ in range(3)]

    # Вибір рівня складності
    bot_move_func = choose_difficulty()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X':
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)
                make_move(row, col)

        if current_player == 'O':
            bot_row, bot_col = bot_move_func()
            if bot_row is not None and bot_col is not None:
                make_move(bot_row, bot_col)

        show_game()

    show_endgame_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 < x < WIDTH // 2 + 100 and HEIGHT // 2 - 75 < y < HEIGHT // 2 - 25:
                    run_game()
                elif WIDTH // 2 - 250 < x < WIDTH // 2 + 250 and HEIGHT // 2 + 25 < y < HEIGHT // 2 + 75:
                    main_menu()
                elif WIDTH // 2 - 250 < x < WIDTH // 2 + 250 and HEIGHT // 2 + 125 < y < HEIGHT // 2 + 175:
                    change_background()


# Головне меню
def main_menu():
    show_main_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 0 < mouse_pos[0] < WIDTH and HEIGHT // 2 - 100 < mouse_pos[1] < HEIGHT // 2 - 50:
                    run_game()
                elif 0 < mouse_pos[0] < WIDTH and HEIGHT // 2 < mouse_pos[1] < HEIGHT // 2 + 50:
                    pygame.quit()
                    sys.exit()
                elif 0 < mouse_pos[0] < WIDTH and HEIGHT // 2 + 100 < mouse_pos[1] < HEIGHT // 2 + 150:
                    change_background()

if __name__ == '__main__':
    main_menu()