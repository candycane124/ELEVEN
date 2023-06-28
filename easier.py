import pygame

def genText(screen, text, colour, size, pos, align, font="freesansbold.ttf"):
    '''
    '''
    font = pygame.font.Font(font, size)
    rendered = font.render(text, True, colour)
    rendRect = rendered.get_rect()
    if align == "top-right":
        rendRect.top = pos[1]
        rendRect.right = pos[0]
    elif align == "bottom-left":
        rendRect.bottom = pos[1]
        rendRect.left = pos[0]
    elif align == "bottom-right":
        rendRect.bottom = pos[1]
        rendRect.right = pos[0]
    elif align == "top-left":
        rendRect.top = pos[1]
        rendRect.left = pos[0]
    elif align == "middle":
        rendRect.center = (pos[0], pos[1])
    screen.blit(rendered,rendRect)

def loadImage(location, width, height):
    return pygame.transform.scale(pygame.image.load(location),(width,height))