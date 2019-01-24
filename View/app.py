from Model.maze import Maze
import pygame


class App:

    def __init__(self, window_width=800, window_height=600):
        self.__window_shape = (window_width, window_height)
        self.__running = True
        self.__display_surf = None
        self.__block_image = None
        self.__agent_image = None
        # should be taken from text input
        N, M = None, None
        self.__maze = Maze(N, M)

    def on_init(self):
        pygame.init()
        self.__display_surf = pygame.display.set_mode((self.__window_shape[0], self.__window_shape[1]), pygame.HWSURFACE)
        pygame.display.set_caption('RL Maze Solver')
        self.__running = True
        self.__agent_image = pygame.image.load("agent.png").convert()
        self.__block_image = pygame.image.load("block.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self.__running = False
            pygame.quit()

    def on_render(self):
        self.__display_surf.fill((0, 0, 0))
        self.__display_surf.blit(self.__agent_image, (self.__maze.get_agent_index()[0], self.__maze.get_agent_index()[1]))
        pygame.display.flip()

    def on_execute(self):
        self.on_render()
