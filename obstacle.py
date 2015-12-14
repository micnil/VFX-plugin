import maya.cmds as cmds
import vectors ; from vectors import *
import math

class Obstacle:
	def __init__(self, name, r = 1.0, h = 6.0, x = 0.0, y = 0.0, z = 0.0):
		self._name = name
		self.force = 4.0
		self.direction = V(0.0, 1.0, 0.0)
		if cmds.objExists(name):
			self.position = V(cmds.getAttr("{0}.translate".format(name))[0])
			obstacleScale = cmds.getAttr("{0}.scale".format(name))[0]
			self.radius = cmds.polyCylinder(name, query=True, radius=True) * obstacleScale[0] + 0.8
			self.height = cmds.polyCylinder(name, query=True, height=True) * obstacleScale[1]
		else:
			print "box with name \"{0}\" does not exist".format(name)
			self.radius = r
			self.height = h
			self.position = V(x, y, z)

	def distanceFrom(self, v):
		vToObstacle = self.position - v
		parallel = (vToObstacle.dot(self.direction)) * self.direction
		orthogonal = vToObstacle - parallel
		return orthogonal.magnitude()

	def intersects(self, v):
		#parallel = V(self.direction*(v.dot(self.direction) / self.direction.dot(self.direction)))
		#https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Vector_formulation
		vToObstacle = self.position - v
		parallel = (vToObstacle.dot(self.direction)) * self.direction
		orthogonal = vToObstacle - parallel
		#if intersects
		if (parallel.magnitude() < (self.height / 2) and orthogonal.magnitude() < self.radius):
			return True
		else:
			return False

	def orthoProject(self, v):
		'''Project v on ostacle and return the result.'''
		vToObstacle = self.position - v
		parallel = (vToObstacle.dot(self.direction)) * self.direction
		orthogonal = vToObstacle - parallel
		return orthogonal

	def delete(self):
		cmds.delete(at = self._name)