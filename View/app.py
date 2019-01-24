from Model.maze import Maze
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MARGIN = 1
WIDTH = 30
HEIGHT = 30


class App:

    def __init__(self):
        # should be taken from text input
        self.__N, self.__M = 10, 10
        self.__maze = Maze(self.__N, self.__M)
        self.__window_shape = [self.__N * (WIDTH + MARGIN), self.__M * (HEIGHT + MARGIN)]
        self.__running = True
        self.__display_surf = None
        self.__block_image = None
        self.__agent_image = None
        self.__target_image = None
        self.__target_rect = None
        self.__clock = None
        self.__agent_rect = None

    def on_init(self):
        pygame.init()
        self.__display_surf = pygame.display.set_mode(self.__window_shape)
        pygame.display.set_caption('RL Maze Solver')
        self.__running = True
        self.__agent_image = pygame.image.load("View/images/agent.png")
        self.__agent_image = pygame.transform.scale(self.__agent_image, (HEIGHT, WIDTH))
        self.__agent_rect = self.__agent_image.get_rect()

        self.__target_image = pygame.image.load("View/images/target.jpg")
        self.__target_image = pygame.transform.scale(self.__target_image, (HEIGHT, WIDTH))
        self.__target_rect = self.__agent_image.get_rect()

        self.__clock = pygame.time.Clock()

    def run_game(self):
        while self.__running:
            for event in pygame.event.get():
                self.on_event(event)
            self.__display_surf.fill(BLACK)
            agent_index = self.__maze.get_agent_index()

            for row in range(self.__N):
                for column in range(self.__M):

                    if row == agent_index[0] and column == agent_index[1]:
                        self.__agent_rect.topleft = ((MARGIN + WIDTH) * column + MARGIN,
                                                     (MARGIN + HEIGHT) * row + MARGIN)

                        self.__display_surf.blit(self.__agent_image, self.__agent_rect)
                    elif row == self.__N - 1 and column == self.__M - 1:
                        self.__target_rect.topleft = ((MARGIN + WIDTH) * column + MARGIN,
                                                     (MARGIN + HEIGHT) * row + MARGIN)

                        self.__display_surf.blit(self.__target_image, self.__target_rect)
                    else:
                        if self.__maze.get_grid_value(row, column) == 1:
                            color = BLACK
                        else:
                            color = WHITE
                        pygame.draw.rect(self.__display_surf, color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                 (MARGIN + HEIGHT) * row + MARGIN,
                                    WIDTH,
                                    HEIGHT])
            self.__clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False

    def on_render(self):
        self.__display_surf.fill((0, 0, 0))
        self.__display_surf.blit(self.__agent_image, (self.__maze.get_agent_index()[0], self.__maze.get_agent_index()[1]))
        pygame.display.flip()

    def on_execute(self):
        self.on_render()
