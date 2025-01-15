import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Scene:
    def __init__(self, width, height, color=WHITE):
        self.width = width
        self.height = height
        self.color = color
        self.boxes = []  # list to store boxes on scene

    def draw(self, screen):
        screen.fill(self.color)  # fill the screen with the background color
        for box in self.boxes:
            box.draw(screen)  # draw every box on scene

    def add_box(self, x, y):
        box = Box(x, y)  # create new box
        self.boxes.append(box)  # add the box to the scene
        print(box.x, box.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse button click
            self.add_box(event.pos[0], event.pos[1])  # add new box where mouse was clicked


class Box:
    def __init__(self, x, y, size=50, color=RED):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size,
                                self.size)  # create a rectangle for the box to draw
        # center the rectangle

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # draw the box


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Click to Generate Boxes")

    scene = Scene(screen_width, screen_height)  # create the scene

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.handle_event(event)  # Pass the event to the scene

        scene.draw(screen)  # Draw the scene
        pygame.display.flip()  # update the screen

    pygame.quit()


if __name__ == "__main__":
    main()