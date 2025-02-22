import pygame
import sys
import pygame_methods as pm
#import fluid as VEF
import fluid as VEF

# Initialize Pygame
pygame.init()

# Set up the display
internal_width, internal_height = 64, 32
scale_factor = 5  # Scale factor to enlarge the window
window_width, window_height = internal_width * scale_factor, internal_height * scale_factor
surface = pygame.Surface((internal_width, internal_height))
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pygame Window')

viscosity = 0.1
elasticity = 10
particle_number = 100
fluid = VEF.VEFluid(particle_number, (internal_width -1, internal_height - 1))
white = (255, 255, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    surface.fill((5, 5, 5))
    #pm.draw_pixel(surface, 20, 20, (255,255,255))
    mousePos = pygame.mouse.get_pos()
    fluid.simulate(1, 0.1, mousePos)

    for particle in fluid.particles:
        x = int(particle.position.x)
        y = int(particle.position.y)
        pm.draw_pixel(surface, x, y, particle.colour)

    # Scale the internal surface to the window size
    scaled_surface = pygame.transform.scale(surface, (window_width, window_height))
    window.blit(scaled_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()