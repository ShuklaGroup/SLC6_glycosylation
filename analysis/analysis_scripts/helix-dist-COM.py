#Center of mass distance calculation for gating helicies

import numpy as np
import glob
import pytraj as pt
import os

for system in sorted(glob.glob('../*strip.prmtop')):
	dir=os.path.dirname(system)
	name=system.replace(dir+'/','',1)

	system_base = name.replace("-strip.prmtop","")

	prmtop = f"../{system_base}-strip.prmtop"

	for traj in sorted(glob.glob(f"../../strip-traj-all/{system_base}-CLONE*strip.xtc")):
		dir=os.path.dirname(traj)
		filename=traj.replace(dir+'/','',1)
		dist_file = f"{filename}-extra-COM-dist.npy"
		a = os.path.isfile(dist_file)
		if a == False:
			t = pt.load(traj, prmtop)

			#SERT
			tm1b=':24-37&(@CA)'
			tm6a=':248-263&(@CA)'
			tm10= ':409-422&(@CA)'

			dist_extra = pt.distance(t, [f"{tm1b} {tm10}", f"{tm6a} {tm10}"])
			
			#SERT
			tm1a=':10-21&(@CA)'
			tm5=':199-211&(@CA)'
			tm6b= ':268-275&(@CA)'

			dist_intra = pt.distance(t, [f"{tm1a} {tm5}", f"{tm1a} {tm6b}"])

			np.save(f"{filename}-extra-COM-dist.npy", dist_extra)
			np.save(f"{filename}-intra-COM-dist.npy", dist_intra)
			

			print(filename)
