import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        self.settings_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.show_settings = False

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.font.render("2D Minecraft", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 4))

        # Draw buttons
        pygame.draw.rect(screen, (0, 200, 0), self.start_btn)
        start_text = self.font.render("Start", True, WHITE)
        screen.blit(start_text, (self.start_btn.x + 50, self.start_btn.y + 10))

        pygame.draw.rect(screen, (200, 0, 0), self.settings_btn)
        settings_text = self.font.render("Settings", True, WHITE)
        screen.blit(settings_text, (self.settings_btn.x + 20, self.settings_btn.y + 10))

        if self.show_settings:
            self.draw_settings(screen)

    def draw_settings(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        settings_font = pygame.font.Font(None, 48)
        settings_text = settings_font.render("Settings Menu", True, WHITE)
        screen.blit(settings_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 4 + 20))