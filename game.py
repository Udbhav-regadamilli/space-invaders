import pygame, random

pygame.init()

HEIGHT ,WIDTH = 700 , 900

ufo = pygame.transform.scale(pygame.image.load(r'images\\ufo.png'), (65, 65))
bg = pygame.transform.scale(pygame.image.load(r'images\\space.jpg'), (900, 700))
bull = pygame.transform.scale(pygame.image.load(r'images\\bullet.png'), (20, 50))
en1 = pygame.transform.scale(pygame.image.load(r'images\\enemy1.png'), (65, 65))
en2 = pygame.transform.scale(pygame.image.load(r'images\\enemy2.png'), (65, 65))

class player:
    x = WIDTH//2 - 32.5
    y = 550
    vel = 1
    score = 0
    level = 1
    health = 100
    bullets = []
    p_lose = False
    p_win = False

    def default():
        screen.blit(bg, (0, 0))
        draw(ufo, player.x, player.y)

    def win():
        font = pygame.font.SysFont('timesnewroman', 50)
        text = font.render("YOU WIN", False, (0, 255, 0))
        screen.blit(text, ((WIDTH//2)-110, (HEIGHT//2)-50))

    def lose():
        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("YOU LOSE", False, (255, 0, 0))
        screen.blit(text, ((WIDTH//2)-100, (HEIGHT//2)-50))

    def dis_score():
        font = pygame.font.SysFont('timesnewroman', 30)
        text = font.render(f"Score: {player.score}", False, (255, 255, 255))
        screen.blit(text, (750, 50))

    def dis_level():
        font = pygame.font.SysFont('timesnewroman', 30)
        text = font.render(f"Level: {player.level}", False, (255, 255, 255))
        screen.blit(text, (25, 50))

    def dis_health():
        font = pygame.font.SysFont('timesnewroman', 30)
        text = font.render(f"Health: {player.health}", False, (255, 255, 255))
        screen.blit(text, (25, 650))

class enemy:
    ene = [en1, en2]
    e = en1
    enemys = []
    bullets = []
    
    def move(self):
        for i in range(len(self.enemys)):
            x, y, z, t = self.enemys[i]
            t-=1
            if x+z+65 > WIDTH or x+z < 0:
                z *= -1
                y += 30

            if t==0:
                t = random.randint(1000, 2000)
                self.bullets.append((x, y))
            bullet.e_move()
            if 500-y < 65 or abs(player.y - y) < 65:
                player.p_lose = True
                player.x = (WIDTH//2)-32.5
                player.y = HEIGHT//2
            x+=z
            self.enemys[i] = (x, y, z, t)
            draw(self.e, x, y)


class bullet:
    x = player.x
    y = player.y
    vel = 0.5

    def e_move():
        for i in range(len(enemy.bullets)):
            if i == len(enemy.bullets):
                break
            if enemy.bullets[i]:
                x, y = enemy.bullets[i]
                if y < HEIGHT:
                    draw(bull, x, y)
                    enemy.bullets[i] = (x, y+0.1)
                else:
                    enemy.bullets.pop(i)

    def e_collide():
        for i in range(len(enemy.bullets)):
            if i>=len(enemy.bullets):
                break
            else:
                x = abs(enemy.bullets[i][0] - player.x)
                y = abs(enemy.bullets[i][1] - player.y)
                if x <= 55 and y <= 55:
                    player.health -= 10
                    if player.health == 0:
                        player.p_lose = True
                        player.x = (WIDTH//2)-32.5
                        player.y = HEIGHT//2
                    enemy.bullets.pop(i)


    def move(self):
        for i in range(len(player.bullets)):
            if i == len(player.bullets):
                break
            if player.bullets[i]:
                x, y = player.bullets[i]
                if y > 0:
                    draw(bull, x, y)
                    player.bullets[i] = (x, y-self.vel)
                else:
                    player.bullets.pop(i)

    def collide(self):
        for i in range(len(player.bullets)):
            if i >= len(player.bullets):
                break
            for j in range(len(enemy.enemys)):
                if j >= len(enemy.enemys) or i >= len(player.bullets):
                    break
                x = abs(player.bullets[i][0] - enemy.enemys[j][0])
                y = abs(player.bullets[i][1] - enemy.enemys[j][1])
                if x <= 16 and y <= 46:
                    player.score += 10
                    player.bullets.pop(i)
                    enemy.enemys.pop(j)
            

def draw(img, x, y):
    screen.blit(img, (x, y))

def ene(num):
    for i in range(num):
        x = random.randint(50, 800)
        y = random.randint(50, 300)
        t = random.randint(1000, 3000)
        enemy.enemys.append((x, y, 0.5, t//player.level))

def main():
    run = True
    ene(player.level * 5)
    while run:
        screen.blit(bg, (0,0))
        if player.p_lose:
            player.default()
            player.lose()
            player.y += player.vel
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
        elif player.p_win:
            player.default()
            player.win()
            player.y -= player.vel
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.bullets.append((player.x+22, player.y))
        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if player.x > 0:
                    player.x -= player.vel
            if keys[pygame.K_RIGHT]:
                if player.x < WIDTH-65:
                    player.x += player.vel
            if keys[pygame.K_UP]:
                if player.y > 500:
                    player.y -= player.vel 
            if keys[pygame.K_DOWN]:
                if player.y < HEIGHT-65:
                    player.y += player.vel
        
            bullet.move(bullet)
            enemy.move(enemy)
            bullet.collide(bullet)
            bullet.e_collide()
            draw(ufo, player.x, player.y)
            if (len(enemy.enemys) == 0) and player.level<3:
                draw(bg, 0, 0)
                draw(ufo, player.x, player.y)
                player.bullets.clear()
                enemy.bullets.clear()
                if enemy.e == en1:
                    enemy.e = en2
                else:
                    enemy.e = en1
                player.level += 1
                ene(player.level*3)
            if player.level == 3 and len(enemy.enemys) == 0:
                print("WIN")
                player.p_win = True

        player.dis_health()
        player.dis_level()
        player.dis_score()
        pygame.display.update()
    pygame.quit()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
main()