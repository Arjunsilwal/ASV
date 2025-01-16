import pygame
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Scene:
    def __init__(self, width, height, color=WHITE):
        self.width = width
        self.height = height
        self.color = color
        self.boxes = []  # List to store boxes on scene
        self.click_location = None  # Store last left-click position (x, y)
        self.circle_radius = 5  # Set circle radius

    def draw(self, screen):
        screen.fill(self.color)  # Fill the screen with the background color
        for box in self.boxes:
            box.draw(screen)  # Draw every box on scene
        if self.click_location:  # check for valid location click to draw
            self.draw_click_circle(screen)

    def draw_click_circle(self, screen):  # draw the circle
        pygame.draw.circle(screen, BLUE, self.click_location, self.circle_radius)

    def add_box(self, x, y):
        box = Box(x, y)  # Create new box
        self.boxes.append(box)  # Add the box to the scene

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and self.click_location:  # Move boxes only if there is a valid click location
                self.move_boxes()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                self.click_location = event.pos  # Record the click location
            elif event.button == 3:  # Right mouse button click
                self.add_box(event.pos[0], event.pos[1])  # Add new box where mouse was clicked

    def move_boxes(self):
      if self.click_location:
          for box in self.boxes:
              box.set_target(self.click_location)

class Box:
    def __init__(self, x, y, size=50, color=RED, speed=0, acceleration=0.2, max_speed=1, slow_down_distance=50): #modified max speed and slow down distance
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.acceleration = acceleration
        self.max_speed = max_speed # max speed is now 2
        self.slow_down_distance = slow_down_distance # slow down distance is now 50
        self.target = None # target for box movement
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)  # create a rectangle for the box to draw
        # center the rectangle

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # Draw the box

    def set_target(self, target):
      self.target = target # set the goal for the box.

    def update(self): # update the box every frame
      if self.target:
         dx = self.target[0] - self.x
         dy = self.target[1] - self.y
         distance = math.sqrt(dx**2 + dy**2)

         if distance != 0:
            #Normalized movement vector
            dx /= distance
            dy /= distance

            if distance < self.slow_down_distance: # if inside slow down distance, start to decelerate
               self.speed = max(0,self.speed - self.acceleration)  # decelerate to zero
            else:
               self.speed = min(self.max_speed, self.speed + self.acceleration) #accelerate to max speed

            #move the box
            self.x += dx * self.speed
            self.y += dy * self.speed
            #update the rect
            self.rect.center = (self.x, self.y)

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Click to Generate Boxes and Capture Locations")

    scene = Scene(screen_width, screen_height)  # Create the scene

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.handle_event(event) # Pass the event to the scene

        for box in scene.boxes: # update every box.
           box.update()

        scene.draw(screen)  # Draw the scene
        pygame.display.flip()  # Update the screen

    pygame.quit()

if __name__ == "__main__":
    main()