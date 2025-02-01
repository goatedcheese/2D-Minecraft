import pygame
import sys
import random
from settings import *
from worldgen import World
from inventory import Inventory
from entities import Player, Mob
from menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Minecraft")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"

        # Initialize systems
        self.world = World()
        self.player = Player()
        self.inventory = Inventory()
        self.main_menu = MainMenu()
        self.mobs = []

        # Camera
        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        while self.running:
            if self.game_state == "menu":
                self.handle_menu()
            elif self.game_state == "playing":
                self.handle_game()

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_menu(self):
        self.main_menu.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu.start_btn.collidepoint(event.pos):
                    self.game_state = "playing"
                if self.main_menu.settings_btn.collidepoint(event.pos):
                    self.main_menu.show_settings = True

    def handle_game(self):
        self.handle_input()
        self.update()
        self.draw()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.break_block()
                elif event.button == 3:  # Right click
                    self.place_block()

        # Player movement
        if keys[pygame.K_a]:
            self.player.velocity[0] = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.player.velocity[0] = PLAYER_SPEED
        else:
            self.player.velocity[0] = 0

        if keys[pygame.K_SPACE] and self.player.grounded:
            self.player.velocity[1] = JUMP_FORCE
            self.player.grounded = False

    def break_block(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x + self.camera_x) // BLOCK_SIZE
        grid_y = (mouse_y + self.camera_y) // BLOCK_SIZE

        chunk_x = grid_x // CHUNK_WIDTH
        if chunk_x in self.world.chunks:
            chunk = self.world.chunks[chunk_x]
            index = (grid_x % CHUNK_WIDTH) + (grid_y + WORLD_DEPTH) * CHUNK_WIDTH
            if 0 <= index < len(chunk) and chunk[index] != 'bedrock':  # Can't break bedrock
                chunk[index] = 'air'

    def place_block(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x + self.camera_x) // BLOCK_SIZE
        grid_y = (mouse_y + self.camera_y) // BLOCK_SIZE

        chunk_x = grid_x // CHUNK_WIDTH
        if chunk_x in self.world.chunks:
            chunk = self.world.chunks[chunk_x]
            index = (grid_x % CHUNK_WIDTH) + (grid_y + WORLD_DEPTH) * CHUNK_WIDTH
            if 0 <= index < len(chunk) and chunk[index] == 'air':
                chunk[index] = 'dirt'  # Change to selected block type

    def update(self):
        self.player.update(self.world)

        # Update camera position
        self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2

        # Spawn mobs randomly
        if random.random() < 0.01:  # 1% chance per frame
            self.mobs.append(Mob(self.player.rect.x + random.randint(-200, 200),
                                 self.player.rect.y - 100))

        # Update mobs
        for mob in self.mobs:
            mob.update(self.world)

    def draw(self):
        self.screen.fill(SKY_BLUE)

        # Draw world with camera offset
        self.world.draw(self.screen, self.camera_x, self.camera_y)

        # Draw player with camera offset
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Draw mobs
        for mob in self.mobs:
            mob.draw(self.screen, self.camera_x, self.camera_y)

        # Draw HUD
        self.inventory.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()