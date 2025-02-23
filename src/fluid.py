import numpy as np
from typing import List, Tuple
import data as Data
import HashGrid
import math

# gooey plastic: REST_DENSITY = 6, K_NEAR = 4, K = 0.5
# plastic 2: REST_DENSITY = 5, K_NEAR = 6, K = 1
# strange water: REST_DENSITY = 8, K_NEAR = 2.5, K = 0.6
# splashy water: REST_DENSITY = 4, K_NEAR = 2.0, K = 0.5
# sploshy water: REST_DENSITY = 4, K_NEAR = 1.5, K = 0.5


class VEFluid:
    def __init__(self, particle_count: int, boundary_box: Tuple[float, float]):
        self.particle_count = particle_count
        self.boundary_box = boundary_box
        self.velocity_damping = 1
        self.REST_DENSITY = 2
        self.K_NEAR = 1.5
        self.K = 0.5
        self.INTERACTION_RADIUS = 2  # can be a float
        self.INTERACTION_RADIUS_2 = self.INTERACTION_RADIUS**2
        self.GRAVITY: Data.Vector2 = Data.Vector2(0, 0.2)
        self.particles: List[Data.Particle] = self.initialize_particlesB()
        self.fluidHashGrid = HashGrid.FluidHashGrid(
            self.INTERACTION_RADIUS, self.particles)

    def neighbourSearch(self, mousePos):
        self.fluidHashGrid.clearGrid()
        self.fluidHashGrid.mapParticleToCell()

        # i.e. 1/scale factor established on main
        mouseVector2 = Data.Vector2(mousePos[0], mousePos[1])*(1/8)

        hashGridID = self.fluidHashGrid.getGridHashFromPosition(mouseVector2)
        contentOfCell = self.fluidHashGrid.getContentOfCell(hashGridID)
        for p in self.particles:
            p.colour = (50, 80, 255)

        if contentOfCell != None:
            for p in contentOfCell:
                p.colour = (255, 200, 0)

    def neighbourSearchB(self, mousePos):
        self.fluidHashGrid.clearGrid()
        self.fluidHashGrid.mapParticleToCell()

        # i.e. 1/scale factor established on main
        mouseVector2 = Data.Vector2(mousePos[0], mousePos[1])*0.2

        self.particles[0].position = mouseVector2
        cellsAroundMouse: List[Data.Particle] = self.fluidHashGrid.getNeighboursOfParticleIdx(
            0)

        self.resetParticleColours()

        if len(cellsAroundMouse) > 0:
            for p in cellsAroundMouse:
                distanceSquared = (
                    p.position - mouseVector2).magnitudeSquared()
                p.colour = (
                    255, 200, 0) if distanceSquared < self.INTERACTION_RADIUS_2 else p.colour

    def neighbourSearchC(self):
        self.fluidHashGrid.clearGrid()
        self.fluidHashGrid.mapParticleToCell()

    def initialize_particles(self) -> List[Data.Particle]:
        particles: List[Data.Particle] = []
        for _ in range(self.particle_count):
            x = np.random.uniform(0, self.boundary_box[0])
            y = np.random.uniform(0, self.boundary_box[1])
            particles.append(Data.Particle(x, y))
        return particles

    def initialize_particlesB(self) -> List[Data.Particle]:
        particles: List[Data.Particle] = []
        sideLength = round(math.sqrt(self.particle_count))
        for i in range(sideLength):
            for j in range(sideLength):
                x = i
                y = j
                particles.append(Data.Particle(x, y))
        return particles

    def predict_positions(self, dt: float):
        for p in self.particles:
            p.prevPosition = p.position
            damped_time = dt*self.velocity_damping
            positionDelta: Data.Vector2 = p.velocity * damped_time
            p.position = p.position + positionDelta

    def applyGravity(self, dt):
        for p in self.particles:
            p.velocity = p.velocity + (self.GRAVITY * dt)

    def compute_next_velocity(self, dt):
        inverse_dt = 1.0/dt
        for p in self.particles:
            velocity: Data.Vector2 = (
                p.position - p.prevPosition) * (inverse_dt)
            p.velocity = velocity

    def resetParticleColours(self):
        for p in self.particles:
            p.colour = (50, 80, 255)

    def doubleDensityRelaxation(self, dt):
        for i in range(len(self.particles)):
            density = 0
            densityNear = 0
            neighbours: List[Data.Particle] = self.fluidHashGrid.getNeighboursOfParticleIdx(
                i)
            particle_A = self.particles[i]

            for n in neighbours:
                particle_B = n
                if (particle_A == particle_B):
                    continue
                r_ij = particle_B.position - particle_A.position
                q = r_ij.magnitude() / self.INTERACTION_RADIUS
                if q < 1.0:
                    density += math.pow(1-q, 2)
                    densityNear += math.pow(1-q, 3)
            pressure = self.K * (density - self.REST_DENSITY)
            pressureNear = self.K_NEAR * densityNear
            particleADisplacement = Data.Vector2(0, 0)

            for n in neighbours:
                particle_B = n
                if (particle_A == particle_B):
                    continue
                r_ij = particle_B.position - particle_A.position
                q = r_ij.magnitude() / self.INTERACTION_RADIUS

                if q < 1.0:
                    r_ij.normalize()
                    displacementTerm: float = math.pow(
                        dt, 2)*(pressure * (1-q) + pressureNear*math.pow((1-q), 2))
                    displacementVector = r_ij * displacementTerm
                    particle_B.position += displacementVector*0.5
                    particleADisplacement -= displacementVector*0.5
            particle_A.position += particleADisplacement

    def doubleDensityRelaxationB(self, dt):
        interaction_radius = self.INTERACTION_RADIUS
        k = self.K
        k_near = self.K_NEAR
        rest_density = self.REST_DENSITY
        particles_num = len(self.particles)
        dt_sqr = dt ** 2

        for i in range(particles_num):
            density = 0
            densityNear = 0
            neighbours: List[Data.Particle] = self.fluidHashGrid.getNeighboursOfParticleIdx(
                i)
            particle_A = self.particles[i]
            pos_A = particle_A.position

            for particle_B in neighbours:
                if particle_A == particle_B:
                    continue
                r_ij = particle_B.position - pos_A
                q = r_ij.magnitude() / interaction_radius
                if q < 1.0:
                    one_minus_q = 1 - q
                    density += one_minus_q ** 2
                    densityNear += one_minus_q ** 3

            pressure = k * (density - rest_density)
            pressureNear = k_near * densityNear
            particleADisplacement = Data.Vector2(0, 0)

            for particle_B in neighbours:
                if particle_A == particle_B:
                    continue
                r_ij = particle_B.position - pos_A
                q = r_ij.magnitude() / interaction_radius

                if q < 1.0:
                    r_ij.normalize()
                    one_minus_q = 1 - q
                    displacementTerm = (
                        dt_sqr) * (pressure * one_minus_q + pressureNear * (one_minus_q ** 2))
                    displacementVector = r_ij * displacementTerm
                    particle_B.position += displacementVector * 0.5
                    particleADisplacement -= displacementVector * 0.5

            particle_A.position += particleADisplacement

    def update(self, dt, mousePos):
        self.applyGravity(dt)
        self.predict_positions(dt)
        # self.neighbourSearchB(mousePos)
        self.neighbourSearchC()

        # double relaxation method
        self.doubleDensityRelaxationB(dt)

        self.boundary_collisions()
        self.compute_next_velocity(dt)

    def apply_forces(self, particle):
        pass

    def integrate(self, particle, dt):
        pass

    def boundary_collisions(self):
        for p in self.particles:
            position = p.position

            if p.position.x < 0:
                p.position.x = 0
                p.prevPosition.x = 0
            elif p.position.x > self.boundary_box[0]:
                p.position.x = self.boundary_box[0]
                p.prevPosition.x = self.boundary_box[0]

            if p.position.y < 0:
                p.position.y = 0
                p.prevPosition.y = 0
            elif p.position.y > self.boundary_box[1]:
                p.position.y = self.boundary_box[1]
                p.prevPosition.y = self.boundary_box[1]

    def simulate(self, steps, dt, mousePos):
        for _ in range(steps):
            self.update(dt, mousePos)
