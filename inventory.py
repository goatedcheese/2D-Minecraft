import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class Inventory:
    def __init__(self):
        self.items = ['dirt', 'grass', 'sand', 'stone']
        self.selected_slot = 0

    def draw(self, screen):
        # Draw inventory bar background
        pygame.draw.rect(screen, (50, 50, 50, 200), (0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60))

        # Draw items
        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            color = (255, 215, 0) if i == self.selected_slot else WHITE
            text = font.render(item, True, color)
            screen.blit(text, (20 + i * 100, SCREEN_HEIGHT - 50))