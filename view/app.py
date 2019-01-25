import pygame
from control.agent.agent import Agent
from control.algorithms.algorithm import AlgorithmType

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STEP_COLOR = (0, 150, 0)
SPLIT_COLOR = (255, 0, 0)
MARGIN = 1
WIDTH = 25
HEIGHT = 25
SPLITS = 2
GRIDS = 3
HOVER_START = (0,255,0)
START_COLOR = (0,200,0)


class App:

    def __init__(self, rows=10, cols=10):
        # should be taken from text input
        self.__N, self.__M = rows, cols
        self.__agent = Agent(rows, cols)
        self.__path = set()
        self.__window_shape = [self.__N * (WIDTH + MARGIN) * GRIDS + WIDTH * SPLITS,
                               (self.__M + 2) * (HEIGHT + MARGIN)]
        self.__running = True
        self.__display_surf = None
        self.__block_image = None
        self.__agent_image = None
        self.__target_image = None
        self.__target_rect = None
        self.__clock = None
        self.__agent_rect = None
        self.__ticks = 60
        self.__fake_screen = None
        self.__pic = None

    def on_init(self):
        pygame.init()
        self.__display_surf = pygame.display.set_mode(self.__window_shape,
                                                      pygame.HWSURFACE |
                                                      pygame.DOUBLEBUF)
        pygame.display.set_caption('RL Maze Solver')
        self.__running = True
        self.__agent_image, self.__agent_rect = self.image_to_rect("view/images/agent.png")
        self.__target_image, self.__target_rect = self.image_to_rect("view/images/target.jpg")
        self.__clock = pygame.time.Clock()
        self.__fake_screen = self.__display_surf.copy()
        self.__pic = pygame.Surface((50, 50))
        self.__pic.fill((255, 100, 200))

    def image_to_rect(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (HEIGHT, WIDTH))
        rect = image.get_rect()
        return image, rect

    def run_game(self):
        while self.__running:
            for event in pygame.event.get():
                self.on_event(event)

            # rendering
            self.render()

            if self.__agent.is_goal():
                self.__ticks = 60

            # not finished yet, so wait for step time then advance the agent
            self.__clock.tick(self.__ticks)
            self.__path.add(self.__agent.get_agent_index())
            self.__agent.advance_agent()
        # finish the game so quite
        pygame.display.quit()
        pygame.quit()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False
        elif event.type == pygame.RESIZABLE:
            self.__display_surf = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE |
                                                          pygame.DOUBLEBUF)
            self.__display_surf.blit(pygame.transform.scale(self.__fake_screen, event.dict['size']), (0, 0))
            pygame.display.flip()

    def draw_split_rect_vertical(self, offset):
        pygame.draw.rect(self.__display_surf, SPLIT_COLOR,
                         [(MARGIN + WIDTH) * self.__N * offset + MARGIN +
                          (offset - 1) * WIDTH,
                          0,
                          WIDTH, (HEIGHT + MARGIN) * self.__M])

    def draw_split_rect_horizontal(self):
        rect = pygame.draw.rect(self.__display_surf, SPLIT_COLOR,
                        [0, (MARGIN + HEIGHT) * self.__M,
                          self.__window_shape[0], HEIGHT])

        margin = self.__window_shape[0] // 3
        sim_text_center = (rect.center[0] - margin, rect.center[1])
        policy_text_center = rect.center
        values_text_center = (rect.center[0] + margin, rect.center[1])
        self.draw_text("Simulation", sim_text_center, 20)
        self.draw_text("Policy", policy_text_center, 20)
        self.draw_text("Values", values_text_center, 20)

    def draw_buttons(self):
        # draw Solve Using Policy Iteration button
        x = 0
        y = (MARGIN + HEIGHT) * (self.__M + 1)
        w = self.__window_shape[0] * (3 / 11)
        h = HEIGHT
        mouse = pygame.mouse.get_pos()
        event = pygame.event.poll()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.__display_surf, HOVER_START, (x, y, w, h))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__agent.restart_same_maze()
                self.__agent.solve_maze(AlgorithmType.PolicyIteration)
                self.__path = set()
                self.__ticks = 3
        else:
            pygame.draw.rect(self.__display_surf, START_COLOR, (x, y, w, h))

        center = ((x + (w / 2)), (y + (h / 2)))
        self.draw_text("Solve Using Policy Iteration", center, 15)

        # draw Reset button
        x += w + self.__window_shape[0] / 11
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.__display_surf, HOVER_START, (x, y, w, h))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__agent.restart_same_maze()
                self.__path = set()
                self.__ticks = 60
        else:
            pygame.draw.rect(self.__display_surf, START_COLOR, (x, y, w, h))

        center = ((x + (w / 2)), (y + (h / 2)))
        self.draw_text("Reset Maze", center, 15)

        # draw Solve Using Value Iteration button
        x += w + self.__window_shape[0] / 11
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.__display_surf, HOVER_START, (x, y, w, h))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__agent.restart_same_maze()
                self.__agent.solve_maze(AlgorithmType.ValueIteration)
                self.__path = set()
                self.__ticks = 3
        else:
            pygame.draw.rect(self.__display_surf, START_COLOR, (x, y, w, h))

        center = ((x + (w / 2)), (y + (h / 2)))
        self.draw_text("Solve Using Value Iteration", center, 15)

    def draw_text(self, txt, center, sz):
        font = pygame.font.Font(pygame.font.get_default_font(), sz)
        text = font.render(txt, True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = center
        self.__display_surf.blit(text, text_rect)

    def draw_simulation_grid(self):
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

    # grid_type can be values or policy
    def draw_text_grid(self, offset, values, grid_type):
        for row in range(self.__N):
            for column in range(self.__M):
                topleft_x = (MARGIN + WIDTH) * (column + offset * self.__N) + MARGIN + offset * WIDTH
                topleft_y = (MARGIN + HEIGHT) * row + MARGIN

                if grid_type == 'values_grid':
                    if self.__agent.get_maze().get_grid_value(row, column) == 1:
                        color = BLACK
                        pygame.draw.rect(self.__display_surf, color,
                                        [topleft_x, topleft_y, WIDTH, HEIGHT])
                    else:
                        rect = pygame.draw.rect(self.__display_surf, WHITE, [topleft_x, topleft_y, WIDTH, HEIGHT])
                        self.draw_text(str("{0:.2f}".format(values[row * self.__M + column])), rect.center, 10)

                elif grid_type == 'policy_grid':
                    if self.__agent.get_maze().get_grid_value(row, column) == 1:
                        color = BLACK
                        pygame.draw.rect(self.__display_surf, color,
                                        [topleft_x, topleft_y, WIDTH, HEIGHT])
                        continue
                    actions = values[(row, column)]
                    if len(actions) == 1:
                        image_path = "view/images/" + actions[0] + ".png"
                    elif len(actions) == 4:
                        image_path = "view/images/all_arrows.png"
                    else:
                        continue
                    cell_image, cell_rect = self.image_to_rect(image_path)
                    cell_rect.topleft = topleft_x, topleft_y
                    self.__display_surf.blit(cell_image, cell_rect)
                else:
                    raise Exception("There is no grid with that type")

    def render(self):
        self.__display_surf.fill(BLACK)

        # Draw the grids
        self.draw_simulation_grid()
        self.draw_text_grid(1, self.__agent.get_state_values(), 'values_grid')
        self.draw_text_grid(2, self.__agent.get_policy_map(), 'policy_grid')

        # Draw the vertical splits
        self.draw_split_rect_vertical(1)
        self.draw_split_rect_vertical(2)

        # Draw horizontal split
        self.draw_split_rect_horizontal()

        # Draw the start button and menu
        self.draw_buttons()

        # Update the view
        pygame.display.flip()

