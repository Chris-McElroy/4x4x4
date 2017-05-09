import pygame
 
pygame.init()
 
display = (800,600)
 
gameDisplay = pygame.display.set_mode(display)
 
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()    

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill((255,255,255))
        largeText = pygame.font.Font('freesansbold.ttf',36)
        TextSurf, TextRect = text_objects("Not Racey", largeText)
        TextRect.center = ((400,300))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        pygame.time.wait(15)

game_intro()
pygame.quit()
quit()