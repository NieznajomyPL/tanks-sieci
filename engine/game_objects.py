import pygame
import math
import random


class GameObject:
    def __init__(self, x, y):
        self.radius = 15

        self.posx = x
        self.posy = y
        self.velox = 0.0
        self.veloy = 0.0
        self.accx = 0.0
        self.accy = 0.0

        self.stable = False
        self.angle = 0
        self.fricion = 0.8

        self.bounce_before = -1
        self.dead = False

        self.gravity = 20
        self.collison_points = 16
        self.phycics_accuracy = 5

    def after_death(self, game_engine):
        pass

    def detect_collision(self, potencialx, potencialy, terrain):
        responsex = 0
        responsey = 0
        collision = False

        row_len = len(terrain)
        col_len = len(terrain[0])

        for n in range(self.collison_points + 1):
            point_angle = (n * math.pi / self.collison_points) + self.angle - math.pi / 2

            testposx = self.radius* math.cos(point_angle) + potencialx
            testposy = self.radius* math.sin(point_angle) + potencialy

            testposx = col_len - 1 if testposx >= col_len else testposx
            testposy = row_len - 1 if testposy >= row_len else testposy

            testposx = 0 if testposx < 0 else testposx
            testposy = 0 if testposy < 0 else testposy

            if terrain[int(testposy)][int(testposx)] != 0:
                responsex += potencialx - testposx
                responsey += potencialy - testposy
                collision = True
                
        return collision, responsex, responsey
        

    def update_physics(self, terrain, deltatime):
        for _ in range(self.phycics_accuracy):
            self.accy += self.gravity
            self.stable = False

            self.velox += 0 if self.accx * deltatime < 0.0000000001 else self.accx * deltatime
            self.veloy += 0 if self.accy * deltatime < 0.0000000001 else self.accy * deltatime
            self.accx = 0
            self.accy = 0

            potencialx = 0 if self.posx + self.velox * deltatime < 0.0000001 else self.posx + self.velox * deltatime
            potencialy = 0 if self.posy + self.veloy * deltatime < 0.0000001 else self.posy + self.veloy * deltatime

            self.angle = math.atan2(self.veloy, self.velox)

            collision, responsex, responsey = self.detect_collision(potencialx, potencialy, terrain)

            magvelo = math.sqrt(self.velox * self.velox + self.veloy * self.veloy)
            magresponse = math.sqrt(responsex * responsex + responsey * responsey)
            if magresponse < 0.005:
                magresponse = 0.005

            if collision:
                self.stable = True

                dot = self.velox * (responsex / magresponse) + self.veloy * (responsey / magresponse)
                self.velox = self.fricion * (-2 * dot * (responsex / magresponse) + self.velox)
                self.veloy = self.fricion * (-2 * dot * (responsey / magresponse) + self.veloy)

                if self.bounce_before > 0:
                    self.bounce_before -= 1
                self.dead = self.bounce_before == 0
            else:
                self.posx = potencialx
                self.posy = potencialy

            if magvelo < 0.05:
                self.stable = True

    def draw(self, dispaly):
        pygame.draw.circle(dispaly, (255, 0, 0), (self.posx, self.posy), self.radius)
        endx = self.posx + self.radius * math.cos(self.angle)
        endy = self.posy + self.radius * math.sin(self.angle)
        pygame.draw.line(dispaly, (255, 255, 255), (self.posx, self.posy), (endx, endy))
        
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f"({self.velox}, {self.veloy})", False, (255, 255, 255))
        dispaly.blit(text_surface, (0,0))


class Debry(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 4
        self.fricion = 0.6
        self.bounce_before = 4

        angle = random.uniform(0, math.pi * 2)
        self.velox = math.cos(angle) * random.uniform(80, 150)
        self.veloy = math.sin(angle) * random.uniform(80, 150)

    def draw(self, dispaly):
        pygame.draw.circle(dispaly, (0, 255, 0), (self.posx, self.posy), self.radius)


class Missile(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 7
        self.fricion = 0
        self.bounce_before = 0
        self.blast_power = 40

    def after_death(self, game_engine):
        game_engine.terrain.boom(game_engine, self.posx, self.posy, self.blast_power)
        boom(game_engine, self.posx, self.posy, self.blast_power)
        
    def draw(self, dispaly):
        # pygame.draw.line(dispaly, (255, 255, 255), (self.posx, self.posy), (self.posx + self.radius* math.cos(self.angle), self.posy + self.radius* math.sin(self.angle)), width=3)
        pygame.draw.polygon(
            dispaly,
            (255, 0, 0),
            (
                (self.posx, self.posy),
                (
                    self.posx - 2 * self.radius* math.cos(self.angle + math.pi / 8),
                    self.posy - 2 * self.radius* math.sin(self.angle + math.pi / 8),
                ),
                (
                    self.posx - 2 * self.radius* math.cos(self.angle - math.pi / 8),
                    self.posy - 2 * self.radius* math.sin(self.angle - math.pi / 8),
                ),
            ),
        )

class Tank(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 12
        self.fricion = 0.3
        
        self.barrel_angle = 0
        self.shoot_power = 5

        self.health = 10
    
    def after_death(self, game_engine):
        game_engine.terrain.boom(game_engine, self.posx, self.posy, 50)
        boom(game_engine, self.posx, self.posy, 50)

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True

    def fire(self, objects):
        cosx = self.radius * math.cos(self.barrel_angle)
        siny = self.radius * math.sin(self.barrel_angle)
        missile = Missile(self.posx + cosx * self.radius/4, self.posy + siny * self.radius/4)
        missile.velox = cosx * self.shoot_power
        missile.veloy = siny * self.shoot_power
        missile.angle = self.barrel_angle
        objects.append(missile)
    
    def draw(self, dispaly):
        pygame.draw.circle(dispaly, (0, 102, 0), (self.posx, self.posy), self.radius)
        endx = self.posx + self.radius * math.cos(self.barrel_angle) * 1.5
        endy = self.posy + self.radius * math.sin(self.barrel_angle) * 1.5
        pygame.draw.line(dispaly, (0, 102, 0), (self.posx, self.posy), (endx, endy), width=10)
        pygame.draw.ellipse(dispaly, (0, 130, 0), pygame.Rect(self.posx - self.radius*1.5, self.posy, self.radius*3, self.radius))

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f"({self.health})", False, (255, 255, 255))
        dispaly.blit(text_surface, (0,0))

        
        

def boom(game_engine, x, y, r):
    objects = game_engine.game_objects_list
    for go in objects:
        dx = go.posx - x
        dy = go.posy - y

        dist = math.sqrt(dx * dx + dy * dy)
        dist = 0.0001 if dist < 0.0001 else dist

        if dist < r:
            if isinstance(go, Tank):
                go.get_damage((1/dist)*r)
            go.velox = (dx / dist) * (1/dist)*r*10
            go.veloy = (dy / dist) * (1/dist)*r*10
            go.stable = False

    for n in range(10):
        objects.append(Debry(x, y))

def boom_surface_terrain_update(terrain_surface, x, y, r):
    pygame.draw.circle(terrain_surface, (0, 0, 0), (x, y), r)