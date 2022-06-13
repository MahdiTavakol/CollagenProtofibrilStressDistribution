#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import sqrt, pi
import pandas as pd
import seaborn as sns
from sklearn.metrics import pairwise_distances
import csv
import os

Strains = []
Frames = []
with open("strain-timestep.csv", 'r') as csvfile:
	plots = csv.reader(csvfile,delimiter=',')
	for row in plots:
		Strains.append(row[0])
		Frames.append(int(row[1]))

cidBorders = []
cid       = []
cidNumber = []




outputwidth   = 3.7
outputheight  = 6.38*(len(Strains)+1)/7
fontsize      = 13
lblfontsize   = 18
lblfontsize2  = 10
linewidth     = 2.5
lgndmarkersize= 3.5
markersize    = 5
linelength    = 5
lgndmarkersize = 5
elinewidth     = 2
smax           = 0.2e8 #3
smin           = 0.0


#Just for debugging, it should be turned off
plt.ioff()


# Create the figure
fig = plt.figure()

# Panel sizes
spec1 = gridspec.GridSpec(len(Strains)+1,2,width_ratios = [0.9,0.05], hspace=0, wspace=0.1)


axes     = []
zColl0   = []
zCollUp0 = []
zCollDn0 = []
idColl0  = []
zMiner0  = []
zMinerUp0= []
zMinerDn0= []
idMiner0 = []
cidMiner0= []
cidC     = []
cidCR    = []
cidCT    = []
cidM     = []
cidMR    = []
cidMT    = []
cidEM    = []
cidEMR   = []
cidEMT   = []


for axNumber, frame, strain in zip(range(len(Strains)), Frames, Strains):
	ax = fig.add_subplot(spec1[axNumber,0])
	axes.append(ax)
	warnCount = 1

	cidColl   = []
	idColl    = []
	zColl     = []
	cidMiner  = []
	idMiner   = []
	zMiner    = []
	zCollUp   = []
	zCollDn   = []
	zMinerUp  = []
	zMinerDn  = []
	CollDef   = []
	CollDefUp = []
	CollDefDn = []
	MinerDef  = []
	MinerDefUp= []
	MinerDefDn= []
	typ       = []

	with open("../dump.defo.lammpstrj", 'r') as dumpFile :

		dump = dumpFile.readlines()
	tsFound = False
	numAtoms = 0
	xmin = xmax = ymin = ymax = zmin = zmax = 0.0
	for i in range(len(dump)):
		line = dump[i]
		if "ITEM: TIMESTEP" in line:
			ts = int(dump[i+1])
			i = i + 1
			if (ts == frame):
				print "Reading timestep: ", ts
				tsFound = True
		elif "ITEM: NUMBER OF ATOMS" in line:
			numAtoms = int(dump[i+1])
			i = i + 1
		elif "ITEM: BOX BOUNDS" in line:
			line = dump[i+1].split()
			i = i + 1
			xmin = float(line[0])
			xmax = float(line[1])
			line = dump[i+1].split()
			i = i + 1
			ymin = float(line[0])
			ymax = float(line[1])
			line = dump[i+1].split()
			i = i + 1
			zmin = float(line[0])
			zmax = float(line[1])
		elif "ITEM: ATOMS" in line:
			if tsFound == False :
				i = i + numAtoms
			else :
				for j in range(numAtoms):
					#print j
					i = i + 1
					line  = dump[i].split()
					aid   = int(line[1])
					pType = int(line[2])
					strs  = abs(float(line[8]))
					if (pType == 1):
						#x    = float(line[2])
						#y    = float(line[3])
						z    = float(line[5])
						z    = zmin + z*(zmax-zmin)
						zColl.append(z)
						idColl.append(aid)
						CollDef.append(strs)
					elif (pType == 2):
						#x    = float(line[2])
						#y    = float(line[3])
						z    = float(line[5])
						z    = zmin + z*(zmax-zmin)
						zMiner.append(z)
						idMiner.append(aid)
						typ.append(2)
						MinerDef.append(strs)
					elif (pType == 3):
						#x    = float(line[2])
						#y    = float(line[3])
						z    = float(line[5])
						z    = zmin + z*(zmax-zmin)
						zMiner.append(z)
						idMiner.append(aid)
						MinerDef.append(strs)
						typ.append(3)
				break

  




	if (frame == Frames[0]):
		zColl0    = zColl
		zMiner0   = zMiner
		idColl0   = idColl
		idMiner0  = idMiner
		z0min     = zmin
		z0max     = zmax
		zCollUp0  = [x+z0max-z0min for x in zColl0]
		zCollDn0  = [x-z0max+z0min for x in zColl0]
		zMinerUp0 = [x+z0max-z0min for x in zMiner0]
		zMinerDn0 = [x-z0max+z0min for x in zMiner0]
		for i in range(len(idMiner0)):
			dum = int((zMiner0[i]-z0min)/((z0max-z0min)/5))
			if (typ[i] == 2):
				cidMiner0.append(dum+156)
			elif (typ[i] == 3):
				cidMiner0.append(dum+156+5)

			
		#ax.add_patch(plt.Rectangle((10, -100),20, 5100, ls="solid",  ec="c", fc="w"))
		#ax.add_patch(plt.Rectangle((11,    0),10, 5000, ls="solid", ec="b", fc="b"))
		#plt.text(25.5,2500,'500 nm', fontsize=lblfontsize , color='k',rotation=90, alpha=1, ha='center')

	for a in idColl:
		cidColl.append(int(a/219+1))
	for a in idMiner:
		cidMiner.append(cidMiner0[idMiner0.index(a)])


 	cl = {'cidColl': cidColl, 'xColl': xColl,'yColl': yColl, 'zColl': zColl, 'CollDef': CollDef, 'CollR': CollR}
	clPd = pd.DataFrame(data=cl)
	clPd2 = clPd[['cidColl','CollR']].groupby('cidColl').mean()
	clPd = clPd.drop('CollR',axis=1)
	clPd3 = pd.DataFrame.merge(clPd,clPd2,on='cidColl')
	clPd3 = clPd3.sort_values(by=['CollR'])

	cidColl = clPd3['cidColl'].to_numpy()
	collR   = clPd3['CollR'].to_numpy()
	xColl   = clPd3['xColl'].to_numpy()
	yColl   = clPd3['yColl'].to_numpy()
	zColl   = clPd3['zColl'].to_numpy()
	CollDef = clPd3['CollDef'].to_numpy()

	zCollUp  = [x+zmax-zmin for x in zColl]
	zCollDn  = [x-zmax+zmin for x in zColl]
	zMinerUp = [x+zmax-zmin for x in zMiner]
	zMinerDn = [x-zmax+zmin for x in zMiner]

	CollIndex = []
	cid = 0
	index = 0
	for cidC in cidColl:
		if (cid != cidC):
			index = index + 1
			cid = cidC
		CollIndex.append(index)
	



	color = 'red'
	linestyle = 'solid'
	ax.scatter( CollIndex, zColl,   s=0.01,alpha=1, marker='o', c = CollDef  , cmap='rainbow', vmin=smin, vmax=smax)
	ax.scatter( CollIndex, zCollUp, s=0.01,alpha=1, marker='o', c = CollDef  , cmap='rainbow', vmin=smin, vmax=smax)
	ax.scatter( CollIndex, zCollDn, s=0.01,alpha=1, marker='o', c = CollDef  , cmap='rainbow', vmin=smin, vmax=smax)

	color = 'blue'
	linestyle = 'none'
	ax.scatter( cidMiner, zMiner  ,s=0.01,alpha=1, marker='.', c = MinerDef  , cmap='rainbow', vmin=smin, vmax=smax)
	ax.scatter( cidMiner, zMinerUp,s=0.01,alpha=1, marker='.', c = MinerDef  , cmap='rainbow', vmin=smin, vmax=smax)
	ax.scatter( cidMiner, zMinerDn,s=0.01,alpha=1, marker='.', c = MinerDef  , cmap='rainbow', vmin=smin, vmax=smax)

	for i in range(len(cidBorders)):
		ax.vlines(cidBorders[i],-3000,6400, linestyle='dotted',lw=1)
	
	ax.set_xlim(0,160)
	ax.set_ylim(-3000,6400)
	ax.set_yticks([])
	ax.set_ylabel(strain,color='k')
	
	ax.set_xticklabels([])

		
ax = fig.add_subplot(spec1[len(Strains),0])
axes.append(ax)
ax.set_ylabel("Radius",color='k')
ax.set_xlabel("Microfibril Id",color='k')


cidC  = []
cidCR = []
cidM  = []
cidMR = []

with open("../dump.equilibrate.lammpstrj", 'r') as eqFile :
	dump = eqFile.readlines()
tsFound = False
numAtoms = 0
xmin = xmax = ymin = ymax = zmin = zmax = 0.0
for i in range(len(dump)):
	line = dump[i]
	if "ITEM: TIMESTEP" in line:
		ts = int(dump[i+1])
		i = i + 1
		if (ts == 0):
			tsFound = True
	elif "ITEM: NUMBER OF ATOMS" in line:
		numAtoms = int(dump[i+1])
		i = i + 1
	elif "ITEM: BOX BOUNDS" in line:
		line = dump[i+1].split()
		i = i + 1
		xmin = float(line[0])
		xmax = float(line[1])
		line = dump[i+1].split()
		i = i + 1
		ymin = float(line[0])
		ymax = float(line[1])
		line = dump[i+1].split()
		i = i + 1
		zmin = float(line[0])
		zmax = float(line[1])
	elif "ITEM: ATOMS" in line:
		if tsFound == False :
			i = i + numAtoms
		else :
			for j in range(numAtoms):
				#print j
				i = i + 1
				line   = dump[i].split()
				aid    = int(line[0])
				pType  = int(line[1])
				x      = float(line[2])
				y      = float(line[3])
				z      = float(line[4])
				x      = xmin + (xmax-xmin)*x
				y      = ymin + (ymax-ymin)*y
				radius = sqrt((x+46.5)*(x+46.5)+(y-147.9)*(y-147.9))
	
				if (pType == 1):
					cid = int(aid/219+1)
					cidC.append(cid)
					cidCR.append(radius)
				elif (pType == 2):
					cid = 160
					if (z < 0.2):
						cid = 156
					elif (z < 0.4):
						cid = 157
					elif (z < 0.6):
						cid = 158
					elif (z < 0.8):
						cid = 159
					elif (z < 1):
						cid = 160
					cidM.append(cid)
					cidMR.append(radius)
			break

color = 'red'
linestyle = 'solid'
ax.scatter( cidC, cidCR, s=0.1,alpha=1, marker='o', c = color)
color = 'blue'
linestyle = 'solid'
ax.scatter( cidM, cidMR, s=0.1,alpha=1, marker='.', c = color)
ax.set_xlim(0,160)

		

fig.tight_layout()


# colormap
ax = fig.add_subplot(spec1[:,1])
ax.set_title("Local strain",fontsize=fontsize-5, pad=12)
N = 100
cmap = plt.get_cmap('rainbow', N)
# Normalizer
norm = mpl.colors.Normalize(vmin=smin, vmax=smax)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

plt.colorbar(sm,ax)


plt.subplots_adjust(top=0.95, bottom=0.08, left=0.15, right=0.90)




#Setting the output resolution
figName = "FigV-StressYZ"
fig.set_dpi(300)
fig.set_size_inches(outputwidth, outputheight)
fig.savefig(figName + "-test.tif")

# Compressing the image
command = "tiffcp -c lzw " + figName + "-test.tif " + figName + ".tif"
os.popen(command)
command = "rm " + figName + "-test.tif"
os.popen(command)
