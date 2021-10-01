from gpiozero.input_devices import DistanceSensor
import pygame
import random
pygame.init()


class Color:
    black = (0, 0, 0)
    red = (255, 0, 0)


class Taxi:
    def __init__(self):
        self.x = 50
        self.y = Game.height / 2
        self.speed = 10
        self.dir = ''
        self.image = pygame.image.load('assets/img/taxi.png')
        self.area = Game.dsply.blit(self.image, (self.x, self.y))
        
    def show(self):
        self.area = Game.dsply.blit(self.image, (self.x, self.y))
        
    def move(self):
        if self.dir == 'b':
            self.y -= self.speed
            
        elif self.dir == 't':
            self.y += self.speed
          
            
class Car:
    cars_pic=['car1.png', 'car2.png', 'car3.png', 'car4.png', 'car5.png', 'car6.png']
    speed = 15
    def __init__(self):
        self.x = Game.width + 50
        self.y = random.randint(100, Game.height - 100)
        self.selected_car = 'assets/img/'+ random.choice(Car.cars_pic)
        self.image = pygame.image.load(self.selected_car)
        self.area = Game.dsply.blit(self.image, (self.x, self.y))
        
    def show(self):
        self.area = Game.dsply.blit(self.image, (self.x, self.y))
        self.x -= Car.speed

        
class Game:
    width = 1084
    height = 840
    fps = 15
    clock = pygame.time.Clock()
    dsply = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Crazy Taxi')
    bg = pygame.image.load("assets/img/street.png")
    bgY1 = 0
    bgY2 = width
    movingLeftSpeed = 10
    font_go = pygame.font.Font('assets/font/atari_full.ttf', 32)
    font_pak = pygame.font.Font('assets/font/atari_full.ttf', 12)

    s = DistanceSensor(23, 24)

    def update(self):
        Game.bgY1 -= Game.movingLeftSpeed
        Game.bgY2 -= Game.movingLeftSpeed
        if Game.bgY1 <= -Game.width:
            Game.bgY1 = Game.width
        if Game.bgY2 <= -Game.width:
            Game.bgY2 = Game.width
            
    def render(self):
        Game.dsply.blit(Game.bg, (Game.bgY1, 0))
        Game.dsply.blit(Game.bg, (Game.bgY2, 0))
        
    @staticmethod
    def play():
        cars = []
        taxi = Taxi()
        sensor_distance = 0

        while True:

            sensor_distance_pre = sensor_distance
            sensor_distance = Game.s.distance

            print(sensor_distance)

            if sensor_distance - sensor_distance_pre < -0.001:
                taxi.dir = 't'
            elif sensor_distance - sensor_distance_pre > 0.001:
                taxi.dir = 'b'

            Game.dsply.blit(Game.bg, (0, 0))
            Game.update(Game)
            Game.render(Game)

            if random.random() < 0.01:
                cars.append(Car())
                
            for car in cars:
                car.show()
                
            for car in cars:
                if taxi.area.colliderect(car.area):
                    text_go = Game.font_go.render('Game Over!', True, Color.red, Color.black)
                    textRect_go = text_go.get_rect()
                    textRect_go.center = (Game.width / 2, Game.height / 2)
                    text_pak = Game.font_pak.render('press any key  to continue', True, Color.red, Color.black)
                    textRect_pak = text_pak.get_rect()
                    textRect_pak.center = (Game.width / 2, Game.height / 2 + 50)
                    while True:
                        Game.dsply.blit(text_go, textRect_go) 
                        Game.dsply.blit(text_pak, textRect_pak) 
                        taxi.show()
                        pygame.display.update()
                        Game.clock.tick(Game.fps)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                exit()
                            elif event.type == pygame.KEYDOWN:
                                Game.play()
            Car.speed += 0.005   
            taxi.show()
            taxi.move()
            pygame.display.update()
            Game.clock.tick(Game.fps)

if __name__ == "__main__":
    Game.play()