import pygame, random

class Player(pygame.sprite.Sprite):
    def __init__(self, startx, starty, character):
        #starting values
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load(f"{character}-idle.png")
        self.rect = self.sprite.get_rect()
        self.rect.center = [startx, starty]
        self.speed = 3
        self.speedecay = 0

    def update(self, Window):
        inputs = pygame.key.get_pressed()
        #check if speed is above 3 and if it is, increment the decay counter
        #when the decay counter surpasses a value, decay the players speed
        if self.speed > 3 and self.speedecay >= 20:
            self.speed -= 0.5
            self.speedecay = 0
        else:
            self.speedecay += 1

        #set temp value for speed to use when moving
        #if moving both vertically and horizontally, reduce this value to give more fluid motion
        speedtemp = self.speed
        if (inputs[pygame.K_a] or inputs[pygame.K_d]) and (inputs[pygame.K_w] or inputs[pygame.K_s]):
            speedtemp = self.speed * 0.8

        #horizontal movement
        if inputs[pygame.K_d]:
            self.rect.move_ip(speedtemp, 0)
        if inputs[pygame.K_a]:
            self.rect.move_ip(-speedtemp, 0)

        #vertical movement
        if inputs[pygame.K_s]:
            self.rect.move_ip(0, speedtemp)
        if inputs[pygame.K_w]:
            self.rect.move_ip(0, -speedtemp)

        #check if player has passed a trigger just past either side of the screen
        #if they are, move them to the other side of the screen, just before that side's trigger
        if self.rect.x < -75:
            self.rect.x = Window.windowsize[0] + 50
        elif self.rect.x > Window.windowsize[0] + 75:
            self.rect.x = -50

        #check if player is above or below the screen
        #if they are, set their position to the top or bottom of the screen respectively
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > Window.windowsize[1] - self.rect.size[1]:
            self.rect.y = Window.windowsize[1] - self.rect.size[1]

    def checkpumpkin(self, Window, Pumpkins, Pumpkin):
        #check if colliding with anything in the pumpkins group
        #if true, increment speed and reset the pumpkin's position
        if pygame.sprite.spritecollideany(self, Pumpkins):
            if self.speed < 15:
                self.speed += 2
            Pumpkin.resetpos(Window)
            Window.score += 1

    def draw(self, window):
        window.blit(self.sprite, self.rect)

class Pumpkin(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        #starting values
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load("pumpkin.png")
        self.rect = self.sprite.get_rect() 
        self.rect.center = [startx, starty]
        self.speed = 6

    def update(self, Window, player):
        #vertical movement
        #movement is increased by 50% of the player's speed
        self.rect.move_ip(0, self.speed + (player.speed / 2))
        #if the pumpkin has gone off the screen, reset it's position
        if self.rect.y > (Window.windowsize[1] + 50):
            self.resetpos(Window)

    def resetpos(self, Window):
        #set the vertical position to just above the screen
        self.rect.y = -50
        #set the horizontal position to a random value inside the screen, ignoring the 200px on either side
        self.rect.x = random.randint(200, Window.windowsize[0] - 200)

    def draw(self, window):
        window.blit(self.sprite, self.rect)