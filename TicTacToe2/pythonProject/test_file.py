import pygame
import sys


pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Дістаю resolution
SCREEN_INFO = pygame.display.Info()
WIDTH, HEIGHT = SCREEN_INFO.current_w, SCREEN_INFO.current_h

# Fullscreen of course
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Хрестики-нулики')

# Фон
main_menu_bg = pygame.image.load('main_theme.png')
main_menu_bg = pygame.transform.scale(main_menu_bg, (WIDTH, HEIGHT))
game_bg = pygame.image.load('game_theme.png')
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Змінні
current_player = 'X'
board = [['' for _ in range(3)] for _ in range(3)]
game_over = False

# Розміри фігурок
CROSS_SIZE = (min(WIDTH, HEIGHT) // 6 + 20) // 2
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 6 - 20


# Відображення меню
def show_main_menu():
    screen.blit(main_menu_bg, (0, 0))

    font = pygame.font.SysFont(None, 50)
    play_button = font.render('Play', True, BLACK)
    exit_button = font.render('Exit', True, BLACK)
    play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    exit_button_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(play_button, play_button_rect)
    screen.blit(exit_button, exit_button_rect)

    pygame.display.update()


# Відображення ігрового поля
def show_game():
    screen.blit(game_bg, (0, 0))
    draw_board()
    pygame.display.update()


# Малюю ігрове поле
def draw_board():
    # Лінії поля
    pygame.draw.line(screen, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)

    # Розміщую хрестики і нулики у відповідних клітинках
    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol == 'X':
                draw_X(row, col)
            elif symbol == 'O':
                draw_O(row, col)


# Малюю хрестик
def draw_X(row, col):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.line(screen, BLACK, (x - CROSS_SIZE, y - CROSS_SIZE), (x + CROSS_SIZE, y + CROSS_SIZE), 5)
    pygame.draw.line(screen, BLACK, (x + CROSS_SIZE, y - CROSS_SIZE), (x - CROSS_SIZE, y + CROSS_SIZE), 5)


# Малюю нолик
def draw_O(row, col):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6
    pygame.draw.circle(screen, BLACK, (x, y), CIRCLE_RADIUS, 5)

# Ця функція для функції нижче(перевірка на нічию)
def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                return False
    return True

# Перевірка на перемогу або нічию
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

# Кроки
def make_move(row, col):
    global current_player
    if not game_over and board[row][col] == '':
        board[row][col] = current_player
        if check_win_or_draw():
            return
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

# Відображаю Aftergame menu
def show_endgame_menu():
    font = pygame.font.SysFont(None, 50)
    play_again_button = font.render('Play again', True, BLACK)
    main_menu_button = font.render('Exit to main menu', True, BLACK)

    play_again_button_rect = play_again_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    main_menu_button_rect = main_menu_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(play_again_button, play_again_button_rect)
    screen.blit(main_menu_button, main_menu_button_rect)

    pygame.display.update()


# гра та її відображення
def run_game():
    global game_over, current_player, board
    game_over = False
    current_player = 'X'
    board = [['' for _ in range(3)] for _ in range(3)]
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)
                make_move(row, col)
        show_game()

    # After game менюшка
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


# Дії в головному меню
def main_menu():
    show_main_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 0 < mouse_pos[0] < WIDTH and HEIGHT // 2 - 75 < mouse_pos[1] < HEIGHT // 2 - 25:
                    run_game()
                elif 0 < mouse_pos[0] < WIDTH and HEIGHT // 2 + 25 < mouse_pos[1] < HEIGHT // 2 + 75:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    main_menu()