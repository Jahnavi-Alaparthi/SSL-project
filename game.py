background = pygame.image.load("background.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#rpalce screen.fill(bLACK)
screen.blit(background, (0, 0))
