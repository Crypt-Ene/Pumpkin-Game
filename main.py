import pygame, sprites, random

def initialize():
    #open the game and set some starting values
    pygame.init()

    #make all info in the Window class as well as the clock global
    global Window, Entitiys, clock

    #define the window size, the score and the game time
    class Window(object):
        windowsize = (int(pygame.display.get_desktop_sizes()[0][0] / 1.5), int(pygame.display.get_desktop_sizes()[0][1] / 1.5))
        window = pygame.display.set_mode((windowsize))
        score = 0
        timeleft = 30
        characterlist = ["skippy", "hoppy"]
        characterindex = 0

    #define the player, the pumpkin and a group for the pumpkin
    class Entitiys:
        character = "skippy"
        pumpkins = pygame.sprite.Group()
        player = ""
        pumpkin = sprites.Pumpkin(Window.windowsize[0] / 2, -50)
        pumpkins.add(pumpkin)

    clock = pygame.time.Clock()

    #move into the main menu
    return mainmenu()

def mainmenu():
    inmenu = True
    tickingdown = False
    tickingup = False
    tickdelay = 0
    screencolor = "#aaaaaa"
    while inmenu:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                #if escape key pressed, close the game
                if event.key == pygame.K_ESCAPE:
                    inmenu = False
                    quit("Escape key pressed")

                #if the space key is pressed, start the game with the current settings
                if event.key == pygame.K_SPACE:
                    inmenu = False
                    tickingdown = False
                    tickingup = False
                    return mainloop()
                
                #if the a key is pressed, reduce the game time and start ticking it down
                if event.key == pygame.K_a:
                    if Window.timeleft > 10:
                        Window.timeleft -= 1
                        tickingdown = True
                        #set initial delay for holding down the key till it starts ticking up
                        tickdelay = -50

                #if the d key is pressed, increase the game time and start ticking it up
                if event.key == pygame.K_d:
                    if Window.timeleft < 120:
                        Window.timeleft += 1
                        tickingup = True
                        #set initial delay for holding down the key till it starts ticking up
                        tickdelay = -50

                if event.key == pygame.K_q:
                    scrollcharacter(-1)

                if event.key == pygame.K_e:
                    scrollcharacter(1)

            if event.type == pygame.KEYUP:
                #if the a key is released, stop ticking the game time down
                if event.key == pygame.K_a:
                    tickingdown = False

                #if the d key is pressed, stop ticking the game time up
                if event.key == pygame.K_d:
                    tickingup = False

            #if the close window button is pressed, close the game
            if event.type == pygame.QUIT:
                    inmenu = False
                    quit("Exit button pressed")

        #checks if the delay is above five
        #if it is, check if it should tick up, down, or neither, then do that and reset delay
        if tickdelay >= 5:
            if tickingup:
                if Window.timeleft < 120:
                    Window.timeleft += 1
                tickdelay = 0

            if tickingdown:
                if Window.timeleft > 10:
                    Window.timeleft -= 1
                tickdelay = 0
        else:
            tickdelay += 1

        pygame.Surface.fill(Window.window, screencolor)
        textblit("Please select how long you'd like the round to", (1, 2), (1,8), (0, 0, 0), 30)
        textblit("last, and which character you want to play as", (1, 2), (3, 16), (0, 0, 0), 30)
        textblit(Window.timeleft, (3, 10), (4, 10), (0, 0, 0), 36)
        textblit("Use A and D to change time", (3, 10), (6, 10), (0, 0, 0), 24)
        textblit(Entitiys.character, (7, 10), (4, 10), (0, 0, 0), 36)
        textblit("Use Q and E to change character", (7, 10), (6, 10), (0, 0, 0), 24)
        textblit("Press space to start!", (1, 2), (7, 8), (0, 0, 0), 34)
        pygame.display.flip()
        clock.tick(60)
    
def mainloop():
    running = True
    screencolor = "#79270a"
    timedelay = 0

    #Create player
    Entitiys.player = sprites.Player(Window.windowsize[0] / 2, 200, Entitiys.character)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                
                #if the escape key is pressed, close the game
                if event.key == pygame.K_ESCAPE:
                    running = False
                    quit("Escape key pressed")

            #if the window is closed, close the game
            if event.type == pygame.QUIT:
                    running = False
                    quit("Exit button pressed")

        #update the player and the pumpkin, then check if they're colliding
        Entitiys.player.update(Window)
        Entitiys.pumpkin.update(Window, Entitiys.player)
        Entitiys.player.checkpumpkin(Window, Entitiys.pumpkins, Entitiys.pumpkin)

        #reduce the time once every 60 frames (1 second)
        if timedelay >= 60:
            Window.timeleft -= 1
            timedelay = 0

            #when the timer reaches 0, go to gameover
            if Window.timeleft == 0:
                running = False
                textblit("Time's Up!", (1, 2), (1, 2), (0, 0, 0), 50)
                pygame.display.flip()
                pygame.time.wait(1000)
                return gameover()
        else:
            timedelay += 1

        pygame.Surface.fill(Window.window, screencolor)
        textblit(Window.score, (1, 20), (1, 20), (0, 0, 0), 32)
        textblit(Window.timeleft, (1, 20), (3, 20), (0, 0, 0), 32)
        Entitiys.player.draw(Window.window)
        Entitiys.pumpkin.draw(Window.window)
        pygame.display.flip()
        clock.tick(60)

def gameover():
    screencolor = "#444444"
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                
                #if the escape key is pressed, close the game
                if event.key == pygame.K_ESCAPE:
                    running = False
                    quit("Escape key pressed")

                #if the space key is pressed, reset the time and the score, then open the menu
                if event.key == pygame.K_SPACE:
                    Window.score = 0
                    Window.timeleft = 30
                    running = False
                    return mainmenu()

            #if the window is closed, close the game
            if event.type == pygame.QUIT:
                    running = False
                    quit("Exit button pressed")

        pygame.Surface.fill(Window.window, screencolor)
        textblit(("You collected " + str(Window.score) + " pumpkins, well done!"), (1, 2), (9, 20), (0, 0, 0), 40)
        textblit(("Press space to play again, or escape to quit"), (1, 2), (11, 20), (0, 0, 0), 26)
        pygame.display.flip()
        clock.tick(60)

def textblit(text, ratiox, ratioy, color, size):
    #Blits text the the screen at ratio's on the screen (a ratiox and ratioy of (1, 2) would put text in the center)
    Output = pygame.font.Font('freesansbold.ttf', size).render(str(text), True, color)
    Window.window.blit(Output, ((((Window.windowsize[0] * ratiox[0]) / ratiox[1]) - (Output.get_size()[0] / 2)), ((Window.windowsize[1] * ratioy[0] / ratioy[1]) - (Output.get_size()[1] / 2))))

def scrollcharacter(scroll):
    while True:
        if Window.characterindex + scroll >= len(Window.characterlist):
            Window.characterindex = 0
            break
        if Window.characterindex + scroll < 0:
            Window.characterindex = len(Window.characterlist) - 1
            break
        Window.characterindex += scroll
        break

    Entitiys.character = Window.characterlist[Window.characterindex]

#start running
initialize()