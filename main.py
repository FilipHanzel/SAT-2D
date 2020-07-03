import pygame
from pygame import Surface
from sat import Shape, Vector
from sat import sat, sat_resolve


def display_message(surface: Surface,
                    text: str,
                    coords=(300, 30),
                    font_size=20) -> None:
    """
    Displays custom message on the screen.
    :param surface: Surface to draw.
    :param text: Message.
    :param coords: Message position.
    :param font_size: Int.
    :return: None.
    """
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text_surface = font.render(text, True, (0.1, 0.7, 0.2))
    text_rect = text_surface.get_rect()
    text_rect.center = coords
    surface.blit(text_surface, text_rect)


def showcase_sat(screen: Surface,
                 shape1: Shape,
                 shape2: Shape) -> None:
    """
    Algorithm without collision resolution.
    :param screen: Pygame Surface.
    :param shape1: Shape.
    :param shape2: Shape.
    :return: None.
    """
    result = sat(shape1, shape2)
    display_message(screen, "Collision:", (400, 10), 15)
    display_message(screen, str(result), (400, 25), 15)

    shape1.update()
    shape2.update()

    if result:
        shape1.draw(screen, (255, 0, 0))
        shape2.draw(screen, (255, 0, 0))
    else:
        shape1.draw(screen, (0, 0, 255))
        shape2.draw(screen, (0, 0, 255))


def showcase_sat_resolve(screen: Surface,
                         shape1: Shape,
                         shape2: Shape) -> None:
    """
    Algorithm with collision resolution.
    :param screen: Pygame Surface.
    :param shape1: Shape.
    :param shape2: Shape.
    :return: None.
    """
    result = sat_resolve(shape1, shape2)
    display_message(screen, "Collision:", (400, 10), 15)
    display_message(screen, str(result), (400, 25), 15)

    shape1.update()
    shape2.update()

    if result:
        shape1.draw(screen, (255, 0, 0))
        shape2.draw(screen, (255, 0, 0))
    else:
        shape1.draw(screen, (0, 0, 255))
        shape2.draw(screen, (0, 0, 255))


def main() -> None:
    # Set up pygame window:
    pygame.init()
    disp_width = 800
    disp_height = 600
    disp_dims = (disp_width, disp_height)
    screen = pygame.display.set_mode(disp_dims)
    pygame.display.set_caption('SAT')
    # icon = pygame.image.load('icon.png')
    # pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    square = Shape([Vector(-40, 40),
                    Vector(40, 40),
                    Vector(40, -40),
                    Vector(-40, -40)])
    triangle = Shape([Vector(-40, -40),
                      Vector(-40, 40),
                      Vector(40, 0)])

    end = False
    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            end = True

        # Square controls (w s a d):
        if keys[pygame.K_w]:
            square.forward()
        if keys[pygame.K_s]:
            square.backwards()
        if keys[pygame.K_a]:
            square.turn_left()
        if keys[pygame.K_d]:
            square.turn_right()

        # Triangle controls (arrow keys):
        if keys[pygame.K_UP]:
            triangle.forward()
        if keys[pygame.K_DOWN]:
            triangle.backwards()
        if keys[pygame.K_LEFT]:
            triangle.turn_left()
        if keys[pygame.K_RIGHT]:
            triangle.turn_right()
            
        # Clear screen:
        screen.fill((170, 180, 110))

        # Algorithm:
        # showcase_sat(screen, triangle, square)
        showcase_sat_resolve(screen, triangle, square)

        pygame.display.flip()

        # Frame rate set to max 120 FPS:
        clock.tick(120)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
