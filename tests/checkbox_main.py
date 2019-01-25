from View.pygame_checkbox import Checkbox, CheckboxGroup
import pygame as pg


def main():

    WIDTH = 800
    HEIGHT = 600
    display = pg.display.set_mode((WIDTH, HEIGHT))

    chkboxes = CheckboxGroup(display, 400, 400, ["Policy Iteration", "Value Iteration"])

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()
            chkboxes.update_checkboxes(event)

        display.fill((200, 200, 200))
        chkboxes.render_checkboxes()
        pg.display.flip()

if __name__ == '__main__': main()