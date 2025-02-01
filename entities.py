import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, BLOCK_SIZE, CHUNK_WIDTH, WORLD_DEPTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 0, 0))  # Red player
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.velocity = [0, 0]
        self.grounded = False

    def update(self, world):
        # Apply gravity
        self.velocity[1] += GRAVITY

        # Horizontal movement
        self.rect.x += self.velocity[0]

        # Check horizontal collisions
        self.check_collisions(world, self.velocity[0], 0)

        # Vertical movement
        self.rect.y += self.velocity[1]

        # Check vertical collisions
        self.grounded = False
        self.check_collisions(world, 0, self.velocity[1])

    def check_collisions(self, world, dx, dy):
        """Check collisions with blocks in the world."""
        # Get player's grid position
        player_left = self.rect.left // BLOCK_SIZE
        player_right = self.rect.right // BLOCK_SIZE
        player_top = self.rect.top // BLOCK_SIZE
        player_bottom = self.rect.bottom // BLOCK_SIZE

        # Check all blocks around the player
        for x in range(player_left, player_right + 1):
            for y in range(player_top, player_bottom + 1):
                # Get the chunk and block
                chunk_x = x // CHUNK_WIDTH
                chunk = world.get_chunk(chunk_x)
                block_x = x % CHUNK_WIDTH
                block_y = y + WORLD_DEPTH

                if 0 <= block_x < CHUNK_WIDTH and 0 <= block_y < len(chunk) // CHUNK_WIDTH:
                    block = chunk[block_x + block_y * CHUNK_WIDTH]
                    if block != 'air' and block != 'bedrock':
                        block_rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        if self.rect.colliderect(block_rect):
                            if dx > 0:  # Moving right
                                self.rect.right = block_rect.left
                            elif dx < 0:  # Moving left
                                self.rect.left = block_rect.right
                            if dy > 0:  # Falling
                                self.rect.bottom = block_rect.top
                                self.grounded = True
                                self.velocity[1] = 0
                            elif dy < 0:  # Jumping
                                self.rect.top = block_rect.bottom
                                self.velocity[1] = 0

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))  # Green mob
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = [0, 0]

    def update(self, world):
        # Basic AI (move left/right)
        self.velocity[0] = 1 if random.random() < 0.5 else -1
        self.rect.x += self.velocity[0]

        # Apply gravity
        self.velocity[1] += GRAVITY
        self.rect.y += self.velocity[1]

        # Check collisions
        for x in range(self.rect.left // BLOCK_SIZE, self.rect.right // BLOCK_SIZE + 1):
            for y in range(self.rect.top // BLOCK_SIZE, self.rect.bottom // BLOCK_SIZE + 1):
                chunk_x = x // CHUNK_WIDTH
                chunk = world.get_chunk(chunk_x)
                block_x = x % CHUNK_WIDTH
                block_y = y + WORLD_DEPTH

                if 0 <= block_x < CHUNK_WIDTH and 0 <= block_y < len(chunk) // CHUNK_WIDTH:
                    block = chunk[block_x + block_y * CHUNK_WIDTH]
                    if block != 'air' and block != 'bedrock':
                        block_rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        if self.rect.colliderect(block_rect):
                            if self.velocity[1] > 0:  # Falling
                                self.rect.bottom = block_rect.top
                                self.velocity[1] = 0

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))