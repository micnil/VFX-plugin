import maya.cmds as cmds
import vectors ; from vectors import *
import math

class Boid:
	def __init__(self, n):
		self._object		= cmds.polyCone(name = n, height = 0.8, radius = 0.3)
		self._name 			= n
		self._position 		= V(0.00, 0.0, 0.0)
		self._velocity 		= V(0.01, 0.0, 0.0)
		self._acceleration 	= V(0.01, 0.0, 0.0)
		self._maxSpeed		= 4.0
		self._maxForce		= 2.0

		self.neighborhoodRadius = 5

	def setPosition(self, x, y, z):
		self._position = V(x, y, z)

	def getPosition(self):
		return self._position

	def getName(self):
		return self._name

	def getVelocity(self):
		return self._velocity

	def addForce(self, force):
		#clamp force if it exceeds maximum.
		if (force.magnitude() > self._maxForce):
			force = force.magnitude(self._maxForce)

		self._acceleration += force # could incorporate mass: a = F / m

	def move(self, dt):
		self._velocity += self._acceleration * dt

		#clamp velocity to maximum speed if it exceeds it.
		if (self._velocity.magnitude() > self._maxSpeed):
			self._velocity = self._velocity.magnitude(self._maxSpeed)

		self._position += self._velocity * dt

		# set acceleration to zero each frame
		self._acceleration = V(0.0, 0.0, 0.0)

	def setKeyFrame(self, t):

		# set the position for a specific time frame
		cmds.setKeyframe(self._object, time = t, v = self._position[0], at = "tx")
		cmds.setKeyframe(self._object, time = t, v = self._position[1], at = "ty")
		cmds.setKeyframe(self._object, time = t, v = self._position[2], at = "tz")

		# take the euler from the boid (compared from original orientation)
		rotation = vectors.angle(self._velocity, V(0.0, 1.0, 0.0))
		rotationMatrix = M().rotate(self._velocity.cross(V(0.0, 1.0, 0.0)), rotation)
		eulerAngles = rotationMatrix.rotation()

		# set the euler angles for a specific time frame
		cmds.setKeyframe(self._object, time = t, v = -math.degrees(eulerAngles[0]), at = "rx")
		cmds.setKeyframe(self._object, time = t, v = -math.degrees(eulerAngles[1]), at = "ry")
		cmds.setKeyframe(self._object, time = t, v = -math.degrees(eulerAngles[2]), at = "rz")

	def delete(self):
		cmds.delete(at = self._name)