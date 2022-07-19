import os
import sys
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
from simtk.openmm import XmlSerializer
import argparse
from parmed.amber import LoadParm
from parmed.openmm import RestartReporter

parser = argparse.ArgumentParser()

parser.add_argument('--system', type=str, required=True)
parser.add_argument('--integrator', type=str, required=True)
parser.add_argument('--state', type=str, required=True)
parser.add_argument('--prmtop', type=str, required=True)
parser.add_argument('--rst', type=str, required=True)

args = parser.parse_args()

#Xml_read function ------------------------------------------------------------
def read_xml(file_path):
    with open(file_path, 'r') as f:
        xml = openmm.XmlSerializer.deserialize(f.read())
    return xml
##################

steps = 250000000

integrator = read_xml(args.integrator)

system = read_xml(args.system)

#state = read_xml(args.state)

platform = Platform.getPlatformByName('CUDA')
platformProperties = {'Precision': 'mixed', 'DeviceIndex': '0'}

system_name = args.state.replace("_state.xml","")
#system_name = args.checkpoint.replace(".chk","")

prmtop = LoadParm(args.prmtop, args.rst)

#TRAJECTORY OUTPUT -----------------------------------------------------------------
dcdReporter = DCDReporter(system_name+'.dcd', 25000)  #100 ps frame save rate
dataReporter = StateDataReporter(system_name+'.log', 500000, totalSteps=steps,
    step=True, speed=True, progress=True, elapsedTime=True, remainingTime=True, potentialEnergy=True, temperature=True, separator='\t')
checkpointReporter = CheckpointReporter(system_name+'-new.chk', 25000)
restartReporter = RestartReporter(system_name+'.rst',reportInterval=25000,netcdf=True)

simulation = Simulation(prmtop.topology, system, integrator,platform, platformProperties)
simulation.loadState(args.state)
#simulation.loadCheckpoint(args.checkpoint)

simulation.reporters.append(dcdReporter)
simulation.reporters.append(dataReporter)
simulation.reporters.append(checkpointReporter)
simulation.reporters.append(restartReporter)

simulation.step(steps)
