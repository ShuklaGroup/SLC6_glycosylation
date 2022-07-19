#RMSD calculation of all CA atoms
import os
import glob
import numpy as np
import mdtraj as md

for system in sorted(glob.glob('../*strip.prmtop')):
	dir=os.path.dirname(system)
	name=system.replace(dir+'/','',1)

	system_base = name.replace("-strip.prmtop","")

	prmtop = f"../{system_base}-strip.prmtop"
	ref_xtc = f"../{system_base}-heat-ref-strip.xtc"

	ref = md.load(ref_xtc, top=prmtop)

	for traj in sorted(glob.glob(f"../../strip-traj-all/{system_base}-CLONE*strip.xtc")):
		dir=os.path.dirname(traj)
		output_name=traj.replace(dir+'/','',1)
		output_name.replace("-strip.xtc","")

		output_file = f"{output_name}-backbone-rmsd.npy"

		check_file = os.path.isfile(output_file)
		if check_file == False:

			t = md.load(traj, top=prmtop)

			ca = t.topology.select("protein and name CA")
			rmsd = md.rmsd(t,ref, atom_indices=ca)
			
			np.save(f"{output_file}", rmsd)


