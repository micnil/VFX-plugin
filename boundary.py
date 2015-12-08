import maya.cmds as cmds
import vectors ; from vectors import *
import math

class Boid:
	def __init__(self, w = 20.0, h = 20.0, d = 20.0):
		self.dimensions = [w, h, d]
		self.scale = V(1.0, 1.0, 1.0)
		self.position = V(0.0, 0.0, 0.0)


	def setFromName(self, name):
		if cmds.objExists(name):
			boundaryTranslation = cmds.getAttr("{0}.translate".format(name))[0]
			boundaryScale = cmds.getAttr("{0}.scale".format(name))[0]
			w = cmds.polyCube(name, query=True, width=True) * boundaryScale[0]
			h = cmds.polyCube(name, query=True, height=True) * boundaryScale[1]
			d = cmds.polyCube(name, query=True, depth=True) * boundaryScale[2]
	def setPosition(self, x, y, z):
		self._position = V(x, y, z)