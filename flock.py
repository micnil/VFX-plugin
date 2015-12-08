import maya.cmds as cmds
from boid import Boid
from boundary import Boundary
import vectors ; from vectors import *
import random
import math

boids = []
boundary = Boundary()
dt=1/100.0

cWeight = 1.0
aWeight = 1.0
sWeight = 2.0

def createBoids(numBoids):
	'''create numboids boids and randomize position'''
	boundaryPos = boundary.getPosition()
	boundaryDim = boundary.getSpawnDimensions()
	for i in range(numBoids):
		b = Boid("boid{0}".format(i))

		x = random.uniform(boundaryPos[0]-boundaryDim[0]/2 , boundaryPos[0]+boundaryDim[0]/2)
		y = random.uniform(boundaryPos[1]-boundaryDim[1]/2 , boundaryPos[1]+boundaryDim[1]/2)
		z = random.uniform(boundaryPos[2]-boundaryDim[2]/2 , boundaryPos[2]+boundaryDim[2]/2)
		b.setPosition(x, y, z)
		boids.append(b)

	print 'creating boids done'

def clear():
	'''cleanup'''
	while boids:
		b = boids.pop()
		b.delete()

def createKeyFrames(numFrames, boundary):
	'''create the keyframes for the animation'''
	for frame in range(numFrames):
		cmds.currentTime( frame, edit=True )
		for b in boids:
			alignment(b)
			separation(b)
			cohesion(b)
			boundary.avoidWalls(b)
			b.move(dt)
			b.setKeyFrame(frame)


def run():
	'''run the simulation'''
	nFrames = 2000

	boundary.setFromName('boundary')
	createBoids(20)
	createKeyFrames(nFrames, boundary)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)

	cmds.play()

def alignment(boid):
	'''flocking function'''
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue

		distance = vectors.distance(b.getPosition(), boid.getPosition())

		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getVelocity())

	if(len(neighborhood) > 0):
		avgVelocity = sum(neighborhood) / len(neighborhood)
		alignmentForce = avgVelocity - boid.getVelocity()
		boid.addForce(alignmentForce * aWeight)

def separation(boid):
	'''flocking function'''
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue

		distVector = b.getPosition() - boid.getPosition()
		distance = distVector.magnitude()

		if distance < boid.neighborhoodRadius:
			neighborhood.append(distVector)

	if(len(neighborhood) > 0):
		separationForce = (sum(neighborhood) / len(neighborhood)) * V(-1, -1, -1)
		boid.addForce(separationForce * sWeight)

def cohesion(boid):
	'''flocking function'''
	neighborhood = []
	for b in boids:
		if b.getName() == boid.getName():
			continue

		distance = vectors.distance(b.getPosition(), boid.getPosition())

		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getPosition())

	if(len(neighborhood) > 0):
		centerPoint = sum(neighborhood) / len(neighborhood)
		cohesionForce = centerPoint - boid.getPosition();
		boid.addForce(cohesionForce * cWeight)