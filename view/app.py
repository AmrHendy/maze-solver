import pygame
from control.agent.agent import Agent
from control.algorithms.algorithm import AlgorithmType


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STEP_COLOR = (0, 150, 0)
MARGIN = 1
WIDTH = 30
HEIGHT = 30


class App:

    def __init__(self, rows=10, cols=10):
        # should be taken from text input
        self.__N, self.__M = rows, cols
        self.__agent = Agent(rows, cols)
        self.__agent.solve_maze(AlgorithmType.ValueIteration)
        self.__path = set()
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
        self.__agent_image = pygame.image.load("view/images/agent.png")
        self.__agent_image = pygame.transform.scale(self.__agent_image, (HEIGHT, WIDTH))
        self.__agent_rect = self.__agent_image.get_rect()

        self.__target_image = pygame.image.load("view/images/target.jpg")
        self.__target_image = pygame.transform.scale(self.__target_image, (HEIGHT, WIDTH))
        self.__target_rect = self.__agent_image.get_rect()

        self.__clock = pygame.time.Clock()

    def run_game(self):
        while self.__running:
            for event in pygame.event.get():
                self.on_event(event)

            # rendering
            self.render()

            # check the goal so we finished
            if self.__agent.is_goal():
                self.__running = False

            # not finished yet, so wait for step time then advance the agent
            self.__clock.tick(2)
            self.__path.add(self.__agent.get_agent_index())
            self.__agent.advance_agent()
        # finish the game so quite
        pygame.quit()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False

    def render(self):
        self.__display_surf.fill(BLACK)
        agent_index = self.__agent.get_agent_index()
        for row in range(self.__N):
            for column in range(self.__M):
                # draw agent position
                if row == agent_index[0] and column == agent_index[1]:
                    self.__agent_rect.topleft = ((MARGIN + WIDTH) * column + MARGIN,
                                                 (MARGIN + HEIGHT) * row + MARGIN)
                    self.__display_surf.blit(self.__agent_image, self.__agent_rect)
                # draw target cell
                elif row == self.__N - 1 and column == self.__M - 1:
                    self.__target_rect.topleft = ((MARGIN + WIDTH) * column + MARGIN,
                                                  (MARGIN + HEIGHT) * row + MARGIN)
                    self.__display_surf.blit(self.__target_image, self.__target_rect)
                # draw empty cells and blocked cells
                else:
                    if (row, column) in self.__path:
                        color = STEP_COLOR
                    elif self.__agent.get_maze().get_grid_value(row, column) == 1:
                        color = BLACK
                    else:
                        color = WHITE
                    pygame.draw.rect(self.__display_surf, color,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH, HEIGHT])
        pygame.display.flip()

