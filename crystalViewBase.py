from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
import makeCrystalBase
import pyqtgraph as pg
import pyqtgraph.exporters
import pyqtgraph.opengl as gl
# import numpy as np
# import makeBox as mkBx
# import itertools as itTl
# import makeGrids as mkGds
# import makePlanes as mkPlns
# import makeOcthedron as mkOct
# import makeCrystalStruct as mkXtlSt

class crystalViewBase(pTypes.GroupParameter):

	def __init__(self, paramsToApply):
		self.dockList = {}
		defs = dict(name = paramsToApply.param('Chemical Formula').value(),
			removable = True, children = [
			dict(name = 'Polytype', type = 'str', 
				value = paramsToApply.param('Polytype').value(), readonly = True),

			dict(name = 'Temperature', type = 'float', 
				value = paramsToApply.param('Temperature').value(), 
				readonly = True, siPrefix = True, suffix = 'K'),

			dict(name = 'Pressure', type = 'float',
				value = paramsToApply.param('Pressure').value(),
				readonly = True, siPrefix = True, suffix = 'kPa'),
			
			dict(name = 'Display...', children = [
			 	dict(name = 'Crystal Lattice', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Dimension to Display (X)', type = 'float', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Y)', type = 'float', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Z)', type = 'float', value = 1,
			 			default = 1)
			 		]),

			 	dict(name = 'Reciprocal Lattice', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Dimension to Display (X)', type = 'float', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Y)', type = 'float', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Z)', type = 'float', value = 1,
			 			default = 1),

			 		dict(name = 'Brillouin Zones to Show', type = 'int', value = 0, default = 0)
			 		]),

			 	dict(name = 'Show Planes in...', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Lattice', type = 'bool', value = False, default = False),
					dict(name = 'Reciprocal Lattice', type = 'bool', value = False, default = False),
			 		dict(name = 'Axis', type = 'int', value = 000, default = 000) 
			 		]),

			 	dict(name = 'X-Ray Diffraction Pattern', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Axis', type = 'int', value = 000, default = 000) 
			 			]),

			 	dict(name = 'Phonon Dispersion Curve', type = 'bool', value = False, default = False),
			 	dict(name = 'Electronic Band Structure', type = 'bool', value = False, default = False),
		 		]),
		 	])

		pTypes.GroupParameter.__init__(self, **defs)
		self.area = DockArea()
		self.param('Display...').sigTreeStateChanged.connect(self.displayChecked)

	def displayChecked(self, param, changes):
		for param, change, data in changes:
			path = self.param('Display...').childPath(param)
			if path is not None:
				childName = '.'.join(path)
			
			else:
				childName = param.name()
			
			if data and isinstance(data, bool):	
				graphicView = makeCrystalBase.makeCrystals()#self.param, self.param.parent().parent())
				self.addDock(self.param('Display...').parent().name()
					+' '+childName, graphicView.w)

			elif not data and isinstance(data, bool):			
				self.removeDock(self.param('Display...').parent().name()
					+' '+childName)

	def addDock(self, name, w):
		d = Dock(name)
		d.addWidget(w)
		self.dockList[name] = d
		self.area.addDock(d)

	def removeDock(self, name):
		self.dockList[name].close()
		del self.dockList[name]