import numpy as np
import random
import Body
import math

class Spawner:
    def __init__(self, player: Body) -> None:
        self.size = player.radius * 4 # make the size of the spawner dependent on the mass
        self.currentParticles = 0
        return
    
    def spawnParticle(self, maxNumParticles, player: Body) -> Body:
        # spawn a particle within the size, random mass, random x y pos within radius, initial velocity of 0
        # make sure the particle is smaller than the player body mass
        massOfParticle = random.randint(10, player.mass / 2)
        minX = player.pos[0] - self.size
        maxX = player.pos[0] + self.size
        r = random.Random()
        randX = r.randint(minX, maxX)
        minY = player.pos[1] - math.sqrt(self.size ** 2 - randX ** 2)
        maxY = player.pos[1] + math.sqrt(self.size ** 2 - randX ** 2)
        randY = r.randint(minY, maxY)
        initialVelocity = 0
        return Body(massOfParticle, np.array([randX, randY]), np.array([0, 0]))

