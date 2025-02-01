import pygame
import random
import noise
from settings import *

# Perlin noise configuration
OCTAVES = 4
FREQUENCY = 24.0
AMPLITUDE = 10.0


class World:
    def __init__(self):
        self.chunks = {}  # Store generated chunks
        self.villages = []  # Store village locations

    def get_chunk(self, chunk_x):
        """Generate or retrieve a chunk."""
        if chunk_x not in self.chunks:
            self.chunks[chunk_x] = self.generate_chunk(chunk_x)
        return self.chunks[chunk_x]

    def generate_chunk(self, chunk_x):
        """Generate a chunk using Perlin noise."""
        chunk_data = []
        for x in range(CHUNK_WIDTH):
            wx = x + chunk_x * CHUNK_WIDTH
            height = int(noise.snoise2(wx / FREQUENCY, 0, OCTAVES) * AMPLITUDE + (SCREEN_HEIGHT // BLOCK_SIZE) * 0.6)

            for y in range(-WORLD_DEPTH, SCREEN_HEIGHT // BLOCK_SIZE):
                if y > height + 1:
                    block = 'air'
                elif y == height + 1:
                    block = 'grass' if random.random() < 0.8 else 'sand'
                elif y > height - 4:
                    block = 'dirt'
                elif y > height - 10:
                    block = 'stone'
                elif y > BEDROCK_LEVEL + 5:
                    if random.random() < 0.02:  # 2% chance for diamond
                        block = 'diamond'
                    elif random.random() < 0.05:  # 5% chance for iron
                        block = 'iron'
                    elif random.random() < 0.1:  # 10% chance for coal
                        block = 'coal'
                    else:
                        block = 'stone'
                else:
                    block = 'bedrock'  # Unbreakable bedrock

                chunk_data.append(block)

        # Generate villages in plains biomes
        if noise.snoise2(chunk_x, 0, OCTAVES) > 0.5:  # Plains biome
            village_x = random.randint(0, CHUNK_WIDTH - 5)
            village_y = height - 2
            self.villages.append((chunk_x * CHUNK_WIDTH + village_x, village_y))

        return chunk_data

    def draw(self, screen, camera_x, camera_y):
        """Draw visible chunks."""
        start_chunk = int(camera_x // (CHUNK_WIDTH * BLOCK_SIZE)) - 1
        end_chunk = start_chunk + (SCREEN_WIDTH // (CHUNK_WIDTH * BLOCK_SIZE)) + 2

        for chunk_x in range(start_chunk, end_chunk):
            chunk = self.get_chunk(chunk_x)
            for x in range(CHUNK_WIDTH):
                for y in range(-WORLD_DEPTH, SCREEN_HEIGHT // BLOCK_SIZE):
                    block = chunk[x + (y + WORLD_DEPTH) * CHUNK_WIDTH]
                    if block == 'air':
                        continue

                    # Block colors
                    if block == 'grass':
                        color = GRASS_GREEN
                    elif block == 'dirt':
                        color = DIRT_BROWN
                    elif block == 'stone':
                        color = STONE_GRAY
                    elif block == 'coal':
                        color = COAL_BLACK
                    elif block == 'iron':
                        color = IRON_GRAY
                    elif block == 'diamond':
                        color = DIAMOND_BLUE
                    elif block == 'sand':
                        color = SAND_YELLOW
                    elif block == 'bedrock':
                        color = BEDROCK_BLACK
                    else:
                        color = BLACK

                    # Draw block
                    pygame.draw.rect(screen, color,
                                     ((chunk_x * CHUNK_WIDTH + x) * BLOCK_SIZE - camera_x,
                                      y * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw villages
        for village in self.villages:
            vx, vy = village
            if start_chunk * CHUNK_WIDTH <= vx < end_chunk * CHUNK_WIDTH:
                pygame.draw.rect(screen, (139, 69, 19),  # Brown for village houses
                                 (vx * BLOCK_SIZE - camera_x, vy * BLOCK_SIZE - camera_y, BLOCK_SIZE * 3,
                                  BLOCK_SIZE * 2))