import pygame
import pandas as pd

def main():
    pygame.init()

    # Screen set-up
    WIDTH = 500
    HEIGHT = 700
    screen = pygame.display.set_mode([WIDTH,HEIGHT])
    pygame.display.set_caption('Wordle 2.0')
    fps = 60
    timer = pygame.time.Clock()

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    gray = (128, 128, 128)
    red = (255, 0, 0)


    # Set up board
    board = [[" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " "]]
    huge_font = pygame.font.Font('freesansbold.ttf', 56)

    # Initialize game relevant variables
    turn = 0
    game_over = False
    win = False
    letters = 0
    turn_active = True

    # Get secret word
    word_df = pd.read_csv('words_5.txt', header=None, names=['word'])
    secret_word = word_df.sample().iloc[0, 0]

    def draw_board():
        for col in range(0, 5):
            for row in range(0, 6):
                # Create rectangles
                pygame.draw.rect(screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
                # Render text from board
                piece_text = huge_font.render(board[row][col], True, gray)
                screen.blit(piece_text, (col*100 + 30, row * 100 +25))
        # Add turn highlighter
        pygame.draw.rect(screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)

    def check_words():
        # Loop through rows
        for row in range(0, 6):
            # Dictionary boolean representing number of characters in secret word
            char_count = {}
            for c in secret_word:
                char_count[c] = char_count.get(c, 0) + 1

            # Loop through columns
            for col in range(0, 5):
                char = board[row][col]
                # only check for the previous turns, replace letter if already marked as green
                if secret_word[col] == char and turn > row:
                    pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
                    char_count[char] -= 1
            for col in range(0, 5):
                char = board[row][col]
                # only check for the previous turns, replace letter as yellow
                if char in secret_word and turn > row and char_count[char] > 0:
                    pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
                    char_count[char] -= 1


    # Game Loop
    running = True
    while running:
        timer.tick(fps)
        screen.fill(black)
        check_words()
        draw_board()

        # Event handling
        for event in pygame.event.get():
            # End game condition
            if event.type == pygame.QUIT:
                running = False

            # Handle user text input, only accept if turn or game not over
            if event.type == pygame.TEXTINPUT and turn_active and not game_over:
                entry = event.__getattribute__('text')
                board[turn][letters] = entry
                letters += 1

            # Delete letters
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    board[turn][letters - 1] = ' '
                    letters -= 1

                # Finish turn by hitting Enter
                if event.key == pygame.K_RETURN and not game_over:
                    turn += 1
                    letters = 0

                # Restart game by hitting Enter after game over
                if event.key == pygame.K_RETURN and game_over:
                    turn = 0
                    letters = 0
                    game_over = False
                    board = [[" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "]]
                    secret_word = word_df.sample().iloc[0,0]

        # Check if word has been guessed correctly, in one of last turns
        for row in range(6):
            guess = ''.join([board[row][i] for i in range(5)])
            if guess == secret_word and row < turn:
                game_over = True
                win = True

        # End turn after 5 characters
        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        # Win handling
        if game_over and win:
            winner_text = huge_font.render('Winner!', True, white)
            screen.blit(winner_text, (160,620))

        # Loss handling
        if turn == 6 and not win:
            game_over = True
            correct_word = huge_font.render(f'{secret_word}', True, red)
            screen.blit(correct_word, (165,620))

        pygame.display.flip()
    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


