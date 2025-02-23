import data
from typing import List, Tuple
from collections import defaultdict


class FluidHashGrid:
    def __init__(self, cellSize: int, particles: List[data.Particle]):
        self.cellSize = cellSize
        self.hashMap = defaultdict(list)
        self.hashMapSize = 100000000
        self.prime1 = 10000000141
        self.prime2 = 10000000093
        self.particles = particles

    def clearGrid(self):
        self.hashMap.clear()

    def getGridIdFromPosition(self, position: data.Vector2):
        x = int(position.x / self.cellSize)
        y = int(position.y / self.cellSize)
        return data.Vector2(x, y)

    def getGridHashFromPosition(self, position: data.Vector2):
        x = int(position.x / self.cellSize)
        y = int(position.y / self.cellSize)
        return self.cellIndexToHash(x, y)

    def cellIndexToHash(self, x: int, y: int) -> int:
        hash_value = (x * self.prime1) ^ (y * self.prime2)
        return hash_value % self.hashMapSize

    def mapParticleToCell(self) -> None:
        for p in self.particles:
            hash = self.getGridHashFromPosition(p.position)
            self.hashMap[hash].append(p)

    def getContentOfCell(self, id):
        content = self.hashMap.get(id, None)
        return content

    def getNeighboursOfParticleIdx(self, i):
        """
        Gets list of neighbours of particle from particles[i] via the hashGrid
        """
        neighbours = []
        position = self.particles[i].position
        particleGridX = int(position.x / self.cellSize)
        particleGridY = int(position.y / self.cellSize)

        for offsetX in range(-1, 2, 1):
            for offsetY in range(-1, 2, 1):
                gridX = particleGridX + offsetX
                gridY = particleGridY + offsetY

                hashID = self.cellIndexToHash(gridX, gridY)
                cellContent = self.getContentOfCell(hashID)

                neighbours.append(cellContent)

        # flatten list for east iteration later
        neighbours = [
            particle for sublist in neighbours if sublist is not None for particle in sublist]
        return neighbours
