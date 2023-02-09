#RMSD calculation of EL2 atoms
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

    el2 = ref.topology.select(f"resid 114 to 149 and name CA")

    ref_coords = ref.xyz[0][el2]

    for traj in sorted(glob.glob(f"../../strip-traj-all/{system_base}-CLONE*strip.xtc")):
        dir=os.path.dirname(traj)
        output_name=traj.replace(dir+'/','',1)
        output_name.replace("-strip.xtc","")

        output_file = f"{output_name}-el2-rmsd.npy"

        check_file = os.path.isfile(output_file)

        if check_file == False:
            t = md.load(traj, top=prmtop)

            t.superpose(ref)
            
            traj_coords = t.xyz[:,el2]

            diff = np.square(ref_coords-traj_coords)
            diff = np.sum(diff, axis=2)
            rmsd = np.sqrt(np.sum(diff, axis=1)/len(el2))

            dir=os.path.dirname(traj)
            filename=traj.replace(dir+'/','',1)
            np.save(filename+'-el2-rmsd.npy', rmsd)
            print(filename)
