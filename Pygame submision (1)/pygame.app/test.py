import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.mixer.init()
laser_sound = pygame.mixer.Sound("laser.wav")  # Put laser.wav in the same folder
laser_sound.set_volume(0.5)

stars = [(random.randint(0, 750), random.randint(0, 550)) for _ in range(100)]

px, py = 400, 300
speed, size = 5, 64
player_img = pygame.transform.scale(
    pygame.image.load("superman.png").convert_alpha(), (size, size)
)

lasers, asteroids = [], []
laser_speed, asteroid_speed = 10, 3
spawn_timer = 0

running = True
while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            # LASERS FIRE RIGHT
            lasers.append([px + size, py + size // 2])
            laser_sound.play()  # Play laser sound

    keys = pygame.key.get_pressed()
    px += (-speed if keys[pygame.K_a] or keys[pygame.K_LEFT] else 0) \
          + (speed if keys[pygame.K_d] or keys[pygame.K_RIGHT] else 0)
    py += (-speed if keys[pygame.K_w] or keys[pygame.K_UP] else 0) \
          + (speed if keys[pygame.K_s] or keys[pygame.K_DOWN] else 0)

    px = max(0, min(px, 800 - size))
    py = max(0, min(py, 600 - size))

    lasers = [[lx + laser_speed, ly] for lx, ly in lasers if lx + laser_speed <= 800]

    spawn_timer += 1
    if spawn_timer >= 60:
        spawn_timer = 0
        asteroids.append([800, random.randint(0, 550), random.randint(30, 60)])

    asteroids = [[ax - asteroid_speed, ay, s] for ax, ay, s in asteroids if ax + s - asteroid_speed > 0]

    new_lasers = []
    for lx, ly in lasers:
        hit = False
        for ax, ay, s in asteroids:
            if ax < lx < ax + s and ay < ly < ay + s:
                hit = True
                asteroids.remove([ax, ay, s])
                break
        if not hit:
            new_lasers.append([lx, ly])
    lasers = new_lasers

    screen.fill((0, 0, 0))
    for sx, sy in stars:
        pygame.draw.rect(screen, (255, 255, 255), (sx, sy, 8, 8))
    screen.blit(player_img, (px, py))
    for lx, ly in lasers:
        pygame.draw.rect(screen, (255, 0, 0), (lx, ly - 2, 12, 4))
    for ax, ay, s in asteroids:
        pygame.draw.rect(screen, (128, 128, 128), (ax, ay, s, s))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
