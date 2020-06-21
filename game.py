import pygame, math, random, sys
from os import path

images_dir = path.join(path.dirname(__file__), 'images')

# pygame initialisation
pygame.init()

# screen class
class Screen():
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Star Wars space shooter!')
        self.clock = pygame.time.Clock()

# window resolution
screen = Screen(1280, 720)

# player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, v):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 60))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.width // 2, 680)
        self.vel = v
        self.speedup = 0
        self.score = 0

# meteorite sprite class
class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sizes = [(30, 30), (40, 40), (50, 50), (60, 60)]
        self.ran_size = math.floor(random.random() * len(self.sizes) - 1)
        self.image = pygame.transform.scale(meteorite_img, (self.sizes[self.ran_size]))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = math.floor(random.randrange(-4, screen.width))
        self.rect.y = math.floor(random.randrange(-10, -2))
        self.speed_y = math.floor(random.randrange(2, 5))
        self.speed_x = math.floor(random.randrange(-3, 5))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > screen.height or self.rect.x > screen.width or self.rect.x < 0:
            self.rect.x = math.floor(random.randrange(0, screen.width))
            self.rect.y = math.floor(random.randrange(-4, -2))
            self.speed_y = math.floor(random.randrange(2, 7))

# bullet sprite class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = x
        self.rect.bottom = y
        self.speed_y = -15

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 1:
            self.kill()

# particle class
class Particle():
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.color_list = [(66, 53, 38), (117, 94, 69), (97, 78, 57), (128, 102, 74)]
        self.ran_color = math.floor(random.random() * len(self.color_list))
        self.rad = random.randrange(2, 6)
        self.vel_x = random.randrange(-3, 3)
        self.vel_y = random.randrange(-8, -1)
        self.lifetime = 0

    def draw(self, surf):
        self.lifetime += 1
        if self.lifetime < 30:
            self.pos_x += self.vel_x
            self.pos_y += self.vel_y
            pygame.draw.circle(screen.window, self.color_list[self.ran_color], (self.pos_x, self.pos_y), self.rad)

# particle list
particles = []

# showing text on screen
def showTextOnWindow(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('verdana'), size)
    font.set_bold(True)
    textSurface = font.render(text, True, (255, 255, 255))
    textArea = textSurface.get_rect()
    textArea.midtop = (x, y)
    surf.blit(textSurface, textArea)

# load all game graphics
background = pygame.image.load(path.join(images_dir, 'space.png')).convert()
background_rect = background.get_rect()

meteorite_img = pygame.image.load(path.join(images_dir, 'meteorite.png')).convert()
player_img = pygame.image.load(path.join(images_dir, 'rocket.png')).convert()

# sprite groups
sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# sprites
player = Player(10)

# add sprite to group
sprites.add(player)

# loop for meteorite rain
for m in range(10):
    meteor = Meteorite()
    meteor.add(mobs)

# game loop
while True:
    # max fps
    screen.clock.tick(60)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.center, player.rect.top)
                sprites.add(bullet)
                bullets.add(bullet)

    # pressed keys list
    keys = pygame.key.get_pressed()

    # movement
    if keys[pygame.K_LEFT] and player.rect.x > 0:
        player.rect.x -= player.vel
    if keys[pygame.K_RIGHT] and player.rect.x < screen.width - 80:
        player.rect.x += player.vel

    # painting window in black on frame
    screen.window.fill((0, 0, 0))
    screen.window.blit(pygame.transform.scale(background, (screen.width, screen.height)), background_rect)

    # updating sprite group
    sprites.update()
    mobs.update()

    # check if bullet hit a meteor
    if pygame.sprite.groupcollide(bullets, mobs, True, True):
        meteor = Meteorite()
        meteor.add(mobs)
        for p in range(20):
            particles.append(Particle(bullet.rect.x, bullet.rect.y))
        player.score += 1

    # drawing particles
    for particle in particles:
        particle.draw(screen.window)

    # check if meteor hit a player
    if pygame.sprite.spritecollide(player, mobs, False):
        sys.exit()

    # drawing sprite
    sprites.draw(screen.window)
    mobs.draw(screen.window)

    # displaying score text
    showTextOnWindow(screen.window, 'Score: ' + str(player.score), 40, 640, 10)

    # updating frame
    pygame.display.update()

pygame.quit()