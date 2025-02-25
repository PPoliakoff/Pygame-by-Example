import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spiro")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

center_x, center_y = 400, 300
radius = 140  # Radius of the large circle
small_radius = -55
trace_radius = 205  # Radius of the trace points

angle = 0
speed = 0.02

# Create a surface for the trace
trace_surface = pygame.Surface((800, 600))
trace_surface.fill(WHITE)
small_x = center_x + (radius+small_radius) * math.cos(angle)
small_y = center_y + (radius+small_radius) * math.sin(angle)
small_angle = angle*(radius+small_radius)/small_radius
prev_trace_x = small_x + trace_radius * math.cos(small_angle)
prev_trace_y = small_y + trace_radius * math.sin(small_angle)

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update angle
    angle += speed
    small_angle = angle*(radius+small_radius)/small_radius
    # Calculate small circle's position
    small_x = center_x + (radius+small_radius) * math.cos(angle)
    small_y = center_y + (radius+small_radius) * math.sin(angle)

    # Calculate the trace point on the small circle (top point of the small circle)
    trace_x = small_x + trace_radius * math.cos(small_angle)
    trace_y = small_y + trace_radius * math.sin(small_angle)

    pygame.draw.line(trace_surface, BLUE, (int(prev_trace_x), int(prev_trace_y)),
                     (int(trace_x), int(trace_y)), 2)
    prev_trace_x = trace_x
    prev_trace_y = trace_y

    screen.blit(trace_surface, (0, 0))  # Draw the trace surface
    pygame.draw.circle(screen, RED, (center_x, center_y),
                       radius, 2)  # Draw large circle
    pygame.draw.circle(screen, RED, (int(small_x), int(small_y)),
                       abs(small_radius), 2)  # Draw small circle
    pygame.draw.circle(screen, BLUE, (int(small_x), int(small_y)), 4)
    pygame.draw.circle(screen, BLUE, (int(trace_x), int(trace_y)), 8)
    pygame.draw.line(screen, BLUE, (int(small_x), int(small_y)),
                     (int(trace_x), int(trace_y)), 2)
    pygame.display.flip()

pygame.quit()
