import numpy as np
import random
import Body
import math
import pygame as pg
import time

class Spawner:
    def __init__(self, player: Body, spawn_seed = -1):
        self.size = self.new_radius(player) # Make the size of the spawner dependent on the mass
        self.currentParticles = 0
        if spawn_seed < 0:
            seed = int(time.time())
            print(f"seed: {seed}")
            random.seed(seed)
        else:
            random.seed(spawn_seed)
    
    def new_radius(self, player: Body):
        return player.radius * 20 + 100

    def spawn_particle(self, player: Body, uid: int, anywhere: bool) -> Body:
        # spawn a particle within the size, random mass, random x y pos within radius, initial velocity of 0
        # make sure the particle is smaller than the player body mass

        add_to_spawn_radius = 0.0

        mass_algorithm = random.random()
        if mass_algorithm < 0.005:
            mass_of_particle = random.randint(int(player.mass), int(player.mass * 8))
            add_to_spawn_radius += player.radius * 30
        elif mass_algorithm < 0.1:
            mass_of_particle = random.randint(int(player.mass/20), int(player.mass/10))
        elif mass_algorithm < 0.15:
            mass_of_particle = random.randint(int(player.mass/30), int(player.mass/15))
        else:
            mass_of_particle = random.randint(int(1/2 * math.sqrt(player.mass)), int(6 * math.sqrt(player.mass)))

        min_x = int(player.pos[0] - self.size)
        max_x = int(player.pos[0] + self.size)
        rand_x = random.randint(min_x + 1, max_x - 1)

        y_pos = math.sqrt(self.size**2 - (player.pos[0] - rand_x)**2)
        
        if anywhere:
            rand_y = random.randint(int(player.pos[1] - self.size) + 1, int(player.pos[1] + self.size) - 1)
        else:
            rand_y = player.pos[1] + random.choice([y_pos, -y_pos])
        

        # Update size
        self.size = self.new_radius(player)

        return Body.Body(mass_of_particle, np.array([float(rand_x + random.random() * 50), float(rand_y + random.random() * 50)]), np.array([random.uniform(-5, 5), random.uniform(-5, 5)]), uid)
