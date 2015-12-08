import maya.cmds as cmds
from boid import Boid
from boundary import Boundary
import vectors ; from vectors import *
import random
import math
import os.path
import sys

boids = []
boundary = Boundary()
dt=1/100.0

cWeight = 1.0
aWeight = 2.0
sWeight = 1.5

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

			# How to stop a running maya script:
			# When a script is running in maya, Everything
			# freezes and maya does not repond to input.
			# To get around this maya has to be stopped from
			# the outside. This if-statement looks for a empty file
			# named "stop.maya" anywhere you want in your filesystem.
			# If it is found, maya exits the script. To stop a script,
			# just add this file to your defined path and it exits. When
			# you want to start the script again, just rename it to something
			# else, eg: run.maya.
			if os.path.isfile('C:\\dev\\stop.maya'):
				sys.exit()

			neighborhood = getNeighborhood(b)
			alignment(b, neighborhood)
			separation(b, neighborhood)
			cohesion(b, neighborhood)
			boundary.avoidWalls(b)
			b.move(dt)
			b.setKeyFrame(frame)

def limit(v, limit):
	#clamp vector if it exceeds magnitude limit.
	if (v.magnitude() > limit):
		v = v.magnitude(limit)

	return v;

def getNeighborhood(boid):
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue

		distance = vectors.distance(b.getPosition(), boid.getPosition())
		if distance < boid.neighborhoodRadius:
			neighborhood.append(b)

	return neighborhood


def run():
	'''run the simulation'''
	nFrames = 2000

	boundary.setFromName('boundary')
	createBoids(40)
	createKeyFrames(nFrames, boundary)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)

	cmds.play()

def alignment(boid, neighborhood):
	'''flocking function'''
	velocities = []
	for b in neighborhood:
		velocities.append(b.getVelocity())

	if(len(neighborhood) > 0):
		avgVelocity = sum(velocities) / len(neighborhood)
		alignmentForce = avgVelocity.magnitude(boid._maxSpeed) - boid.getVelocity()
		alignmentForce = limit(alignmentForce * aWeight, 2.0)
		#print "alignment"
		boid.addForce(alignmentForce)

def separation(boid, neighborhood):
	'''flocking function'''
	distances = []
	for b in neighborhood:
		distVector = boid.getPosition() - b.getPosition()
		distances.append(distVector)

	if(len(neighborhood) > 0):
		separationForce = (sum(distances) / len(neighborhood))
		separationForce = limit(separationForce * sWeight, 2.0)
		#print "separation"
		boid.addForce(separationForce)

def cohesion(boid, neighborhood):
	'''flocking function'''
	positions = []
	for b in neighborhood:
		positions.append(b.getPosition())

	if(len(neighborhood) > 0):
		centerPoint = sum(positions) / len(neighborhood)
		cohesionForce = centerPoint - boid.getPosition();
		cohesionForce = limit(cohesionForce * cWeight, 2.0)
		#print "cohesionForce"
		boid.addForce(cohesionForce)