#solvent accessible surface area calculation implimented by mdtraj
import os
import glob
import numpy as np
import mdtraj as md

for system in sorted(glob.glob('../*strip.prmtop')):
	dir=os.path.dirname(system)
	name=system.replace(dir+'/','',1)

	system_base = name.replace("-strip.prmtop","")

	prmtop = f"../{system_base}-strip.prmtop"

	for traj in sorted(glob.glob(f"../../strip-traj-all/{system_base}-CLONE*strip.xtc")):
		dir=os.path.dirname(traj)
		output_name=traj.replace(dir+'/','',1)
		output_name.replace("-strip.xtc","")

		output_file = f"{output_name}-sasa.npy"

		check_file = os.path.isfile(output_file)
		if check_file == False:

			t = md.load(traj, top=prmtop)

			sasa = md.shrake_rupley(t, mode="residue")
			
			np.save(f"{output_file}", sasa)
			print(output_file)




