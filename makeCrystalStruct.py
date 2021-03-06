from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import itertools as itTl
from scipy import spatial
import symmetryLines as symLns

def mkXtlSt(xtlType,xtlView,numDifAt,res,org=np.array([0,0,0]),bxSdLen=1,scl=1,transp=0.8,linewidth=1):
	
	edges=False
	smooth=True
	shader='shaded'
	glSphr='translucent'
	glLn='opaque'
	antialias=True
	color=np.array([np.array([0,0,1]),np.array([1,0,0])])
	rad=scl/10

	md = gl.MeshData.sphere(rows=res, cols=res,radius=rad)
	strts=[]

	if xtlType=='zinc':
		if xtlView=='std':
			pstns=np.array([list(itTl.product([0,0.25,0.5,0.75,1],repeat=3))])[0]

		elif xtlView=='rcp':
			pstns=np.array([list(itTl.product([0,0.5,1],repeat=3))])[0]
			symline=symLns.addSymLns(org,scl,bxSdLen,transp)
			for i in symline:
				strts.append(i)

		adjt=np.array([list(itTl.product([-0.125,0.125],repeat=3))])[0]
		for i in pstns:
			if ((np.sum(i)==1.75 and (i.min()-i.max())==-0.5)
				or (np.sum(i)==0.75 and (i.min()-i.max())==0)):
				
				i=scl*(i+org)
				strts.append(gl.GLMeshItem(meshdata=md, drawEdges=edges, smooth=smooth, 
					color=(color[0][0], color[0][1], color[0][2], transp),
					shader=shader, glOptions=glSphr))

				strts[len(strts)-1].translate(i[0],i[1],i[2])
				strts[len(strts)-1].scale(scl,scl,scl)
				for j in adjt:
					if np.sum(j)==-0.375 or np.sum(j)==0.125:
						xl=np.transpose(np.array([[i[0],i[0]+j[0]],[i[1],
							i[1]+j[1]],[i[2],i[2]+j[2]]]))

						strts.append(gl.GLLinePlotItem(pos=(xl), 
							color=(color[0][0], color[0][1], color[0][2], transp),
							antialias=antialias, width=linewidth, glOptions=glLn))

			elif ((xtlView=='std' and (np.sum(i)==0 or (np.sum(i)==1 and (i.min()-i.max()==-1 or i.min()-i.max()==-0.5))
				or (np.sum(i)==2 and (i.min()-i.max()==-0.5 or i.min()-i.max()==-1))
				or (np.sum(i)==3 and i.min()-i.max()==0))) or (xtlView=='rcp'
				and (np.sum(i)==0 or (np.sum(i)==1 and i.min()-i.max()==-1)
				or (np.sum(i)==1.5 and i.max()-i.min()==0) or (np.sum(i)==2 and i.min()-i.max()==-1)
				or (np.sum(i)==3 and i.min()-i.max()==0)))):
				
				i=scl*(i+org)
				strts.append(gl.GLMeshItem(meshdata=md, drawEdges=edges, smooth=smooth, 
					color=(color[1][0], color[1][1], color[1][2], transp),
					shader=shader, glOptions=glSphr))

				strts[len(strts)-1].translate(i[0],i[1],i[2])
				strts[len(strts)-1].scale(scl,scl,scl)
				for j in adjt:
					if np.sum(j)==-0.375 or np.sum(j)==0.125:
						xl=np.transpose(np.array([[i[0],i[0]-j[0]],[i[1],
							i[1]-j[1]],[i[2],i[2]-j[2]]]))

						strts.append(gl.GLLinePlotItem(pos=(xl),
							color=(color[1][0], color[1][1], color[1][2], transp),
							antialias=antialias, width=linewidth, glOptions=glLn))
						
	return  strts