import pygame

from send_script.gameObject import *
#from gameObject import *

WIDTH = 1000
HEIGHT = 800

CHOOSE_SHAPE = 0
CHOOSE_COLOR = 1
MOVE = 2
FINISH = -1

def play():
    pygame.init()
    canvas = pygame.display.set_mode((WIDTH, HEIGHT))
    canvas.fill(WHITE)
    clock = pygame.time.Clock()
    
    state = CHOOSE_COLOR
    instruction_panel = InstructionPanel(WIDTH, HEIGHT)
    instruction_panel.chooseColorPanel(canvas)
    
    color_list = [GREEN, RED, BLUE, YELLOW]
    color_str_list = ["GREEN", "RED", "BLUE", "YELLOW"]
    shape_list = [Circle, Triangle, Rectangle, Square]

    shape_idx = 0
    color_idx = 0
    game = WorkSpace(WIDTH, HEIGHT, 25 + HEIGHT//8)
    block = None
    init_pos = (WIDTH//2, HEIGHT//8+65)
    while state != FINISH:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = FINISH
                elif event.key == pygame.K_f:
                    game.getOrder()
                    print("Save Image and clear")
                    instruction_panel.fill(canvas, WHITE)
                    pygame.image.save(canvas, "game_template.png")
                    return
                    game.restart(canvas)
                    state = instruction_panel.chooseColorPanel(canvas)

                if state == CHOOSE_COLOR:
                    if event.key == pygame.K_1:
                        color_idx = 0
                    elif event.key == pygame.K_2:
                        color_idx = 1
                    elif event.key == pygame.K_3:
                        color_idx = 2
                    elif event.key == pygame.K_4:
                        color_idx = 3
                    else:
                        continue
                    color = color_list[color_idx]
                    color_str = color_str_list[color_idx]
                    state = CHOOSE_SHAPE
                    instruction_panel.chooseShapePanel(canvas)

                elif state == CHOOSE_SHAPE:
                    if event.key == pygame.K_1:
                        shape_idx = 0
                    elif event.key == pygame.K_2:
                        shape_idx = 1
                    elif event.key == pygame.K_3:
                        shape_idx = 2
                    elif event.key == pygame.K_4:
                        shape_idx = 3 
                    else:
                        continue
                    block = shape_list[shape_idx](init_pos, color, color_str = color_str)
                    game.push(block)
                    game.moveStop = False
                    instruction_panel.movePanel(canvas)
                    state = MOVE

                elif state == MOVE:
                    if event.key == pygame.K_UP:
                        block.changeView()

        if state == MOVE:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                block.update((-1, 0))
            elif keys[pygame.K_RIGHT]:
                block.update((1, 0))
            game.fill(canvas, WHITE)
            game.draw(canvas)
            game.update()
            if game.moveStop:
                state = CHOOSE_COLOR
                instruction_panel.chooseColorPanel(canvas)

        pygame.display.update()
        clock.tick(100)

if __name__ == "__main__":
    play()
