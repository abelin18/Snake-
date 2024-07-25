import pygame
import random as rand

from constants import (
    columns,
    rows,
    snake_slowness,
    padding,
    cell_size,
    background_color,
    border_color,
    snake_color,
    fruit_color,
    move_cooldown,
    width,
    height
)

UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"

class Snake:
    """
    Represents the snake in the game.

    Attributes:
        body_positions (list): A list of tuples representing the positions of the snake's body segments.
        direction (string): The current direction of the snake's movement.
        eaten_fruit (bool): A flag indicating whether the snake has eaten a fruit.
        snake_size (int): The current size of the snake.
    """

    def __init__(self):
        """
        Initializes the Snake object with a starting position, direction, and size.

        The snake's initial position is set to the center of the game board.
        The direction is initially set to None, indicating no movement.
        """

        self.body_positions = []
        self.body_positions.append((columns//2, rows//2))
        self.direction = None
        self.eaten_fruit = False
        self.snake_size = 1

    def move_snake(self):
        """
        Moves the snake in the current direction and updates its body positions.

        If the snake hasn't received a direction input yet, the function returns 
        None and the snake doesn't move. Based on the current direction, the 
        snake's head moves to a new position. If the snake has eaten a fruit, 
        its body length increases. Otherwise, the old position of the tail is 
        removed.

        Returns:
            tuple or None: The new position of the snake's head if moved, 
                otherwise None.
        """
        if self.direction == None:
            return None
        x, y = self.body_positions[-1] 
        if self.direction == UP:
            self.body_positions.append((x, y - 1))
        if self.direction == DOWN:
            self.body_positions.append((x, y + 1))
        if self.direction == LEFT:
            self.body_positions.append((x - 1, y))
        if self.direction == RIGHT:
            self.body_positions.append((x + 1, y))

        if self.eaten_fruit:
            self.snake_size += 1
            self.eaten_fruit = False
        else:
            self.body_positions.pop(0)

        return self.body_positions[-1]
    def change_direction(self, direction):
        """
        Changes the direction of the snake's movement.

        The direction can only be changed to a perpendicular direction.
        For example, if the snake is moving up or down, it can only change to 
        left or right. If the direction is none the snake can move any direction

        Inputs:
            direction (string): The new direction for the snake to move in.

        Returns:
            bool: True if the direction was successfully changed, False otherwise.
        """
        if self.direction == None:
            self.direction = direction
            return True
        if self.direction == UP:
            if direction == LEFT or direction == RIGHT:
                self.direction = direction
                return True
        if self.direction == DOWN:
            if direction == LEFT or direction == RIGHT:
                self.direction = direction
                return True
        if self.direction == LEFT:
            if direction == UP or direction == DOWN:
                self.direction = direction
                return True
        if self.direction == RIGHT:
            if direction == UP or direction == DOWN:
                self.direction = direction
                return True
        return False

    def eat_fruit(self):
        """
        Sets the self.eaten_fruit to true. Indicating that the snake has eaten
        a fruit
        """
        self.eaten_fruit = True
class GameState:
    """
    represents the game state

    Attributes:
    frame_count (int): The number of frames that have passed since the game started.
    move_cooldown (int): A counter to manage the snake's movement timing.
    snake (Snake): An instance of the Snake class representing the player's snake.
    all_cells (set): A set containing all the possible positions on the game board.
    fruit_position (tuple): The current position of the fruit on the game board.
    has_won (bool): A flag indicating whether the game is paused.
    """

    def __init__(self):
        """
        Initializes the game state object with a starting frame count, move
        cool down, the snake, a set of all cells locations, and fruit postion.
        """
        self.frame_count = 0
        self.move_cooldown = 0

        self.snake = Snake()

        self.all_cells = self.create_set_of_all_cells()
        self.fruit_position = rand.choice(list(self.all_cells - set(self.snake.body_positions)))

        self.pause = False
        self.has_won = False
    
    def create_set_of_all_cells(self):
        """
        Creates a set of all possible cells on the game board.

        The function iterates over the defined number of rows and columns,
        adding each cell's (x, y) coordinate to a set.

        Returns:
            set: A set containing tuples representing all possible positions on the game board.
        """
        snake_set = set()
        for x in range(0, columns):
            for y in range(0, rows):
                snake_tup = (x, y)
                snake_set.add(snake_tup)
        return snake_set
    def create_new_fruit(self):
        """
        Randomly generates a new position for the fruit on the game board.

        The new fruit position is chosen from the set of all possible cells,
        excluding the current positions occupied by the snake's body.

        Returns:
            None
        """
        self.fruit_position = rand.choice(list(self.all_cells - set(self.snake.body_positions)))
        return None

    def has_snake_lost(self, new_position):
        """
        Determines if the snake has lost the game based on its new position. The
        snake has lost if the snake's new position is in its body (excluding the
        head, which is now at the new postion) or if snake new position is out
        of bounds 

        Inputs:
            new_position (tuple): The new (x, y) position of the snake's head.

        Returns
            bool: True if the snake has lost (either by colliding with itself or going out of bounds), False otherwise.
        """
        if new_position == None:
            return False
        (x, y) = new_position
        if new_position in self.snake.body_positions[0:-1:1]:
            return True
        
        if  x < 0 or x >= columns:
            return True
        if  y < 0 or y >= rows:
            return True
        return False        
    def update(self):
        """
        Updates the game state for each frame.

        This function increments the frame count, processes input events by 
        calling, self.handle_events(), moves the snake, checks for collisions,
        and handles snake eating fruit.

        Returns:
            bool: True if the game should exit, False otherwise.
        """
        # increment the frame count because the snake only moves
        # every few frames.

        self.frame_count = self.frame_count + 1
        # Call handle events and if it returns `True`, then we should exit game
        if self.handle_events():
            return True
        #update the snake every X frames using the variable snake_slowness\
        if 0 == self.frame_count % snake_slowness:
            if self.has_won == True:
                return False
            snake_frame = self.snake.move_snake() 
            #if the snake new position is in snake_body_position then snake hit itself 
            if self.has_snake_lost(snake_frame):
                self.has_won = True
                return False
            #if the snakes new position is the fruit position then snake hit fruit
            if snake_frame == self.fruit_position:
                self.snake.eat_fruit()
                self.create_new_fruit()
                return False
            if self.snake.snake_size == rows * columns:
                self.has_won = True
                return False
        #we return `False` to not exit game 

        return False

    def handle_events(self):
        """
        Handles user inputs and game events.

        This function processes events such as quitting the game and changing
        the snake's direction based on key presses. It also manages the move
        cooldown to ensure the snake doesn't change direction too quickly.

        Returns:
            bool: True if the game should exit (e.g., if the quit event is triggered), False otherwise.
        """
        # First, check for the `pygame.QUIT` event and return `True` if we find it.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        #handle key imputs for moving the snake   
        keys = pygame.key.get_pressed()

        is_left = keys[pygame.K_LEFT] or keys[pygame.K_a]

        is_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        is_up = keys[pygame.K_UP] or keys[pygame.K_w]

        is_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return False

        if is_left: 
            if self.snake.change_direction(LEFT):
                self.move_cooldown = move_cooldown
                return False
        if is_right:
            if self.snake.change_direction(RIGHT):
                self.move_cooldown = move_cooldown
                return False
        if is_up:
            if self.snake.change_direction(UP):
                self.move_cooldown = move_cooldown
                return False
        if is_down:
            if self.snake.change_direction(DOWN):
                self.move_cooldown = move_cooldown
                return False
        if self.has_won and keys[pygame.K_SPACE]:
            self.reset()
        return False
        


    def reset(self) :
        """
        Resets the game state to its initial conditions.

        Returns:
            None
        """
        self.frame_count = 0
        self.move_cooldown = 0

        self.snake = Snake()

        self.all_cells = self.create_set_of_all_cells()
        self.fruit_position = rand.choice(list(self.all_cells - set(self.snake.body_positions)))

        self.pause = False
        self.has_won = False
        

    def draw_to(self, screen) -> None:
        """
        Draws the game state to the provided screen.

        This function fills the screen with the border color, draws the game area, 
        the snake, and the fruit in their current positions.

        Inputs:
            screen (pygame.Surface): The screen surface to draw on.
        
        Returns:
            None
        """
        # First, create the border and game area.
        screen.fill(border_color)
        pygame.draw.rect(
            screen,
            background_color,
            pygame.Rect(padding, padding, columns * cell_size, rows * cell_size),
        )

        #drawing the Snake
        for body in self.snake.body_positions:
            x, y = body
            pygame.draw.rect(
                screen,
                snake_color,
                pygame.Rect(
                    padding + x * cell_size + 1,
                    padding + y * cell_size + 1,
                    cell_size - 2,
                    cell_size - 2,
                )
            )
        if not self.has_won:
            #drawing the fruit
            x, y = self.fruit_position
            pygame.draw.rect(
                screen,
                fruit_color,
                pygame.Rect(
                    padding + x * cell_size,
                    padding + y * cell_size,
                    cell_size,
                    cell_size
                )
            )

        if self.has_won:
            win_text = pygame.font.SysFont('freesansbold.ttf', 30)
            txt_render = win_text.render("Press Spacebar to Play Again", True, (255, 255, 255), (20, 20, 20))
            txt_rect = txt_render.get_rect()
            txt_rect.center = (width // 2, height // 2)
            screen.blit(txt_render, txt_rect)
        
        pygame.display.flip()