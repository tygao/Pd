#!/usr/bin/env python
from __future__ import print_function

from ase.md.langevin import Langevin
from ase.io.trajectory import Trajectory
from ase import units
from amp import Amp
from ase.constraints import FixAtoms
from vasp import Vasp

calc = Vasp("./../../../NDFT/surface=fcc111/type=neb/class=vacancy/image=5")
atoms = calc.get_atoms()

constraint = FixAtoms(mask=[atom.tag > 3 for atom in atoms])
atoms.set_constraint(constraint)
atoms.set_calculator(Amp(load="./../../../networks/db8/18-18/checkpoint-parameters.json"))

dyn = Langevin(atoms, 5 * units.fs, 900 * units.kB, 0.002)


def printenergy(a=atoms):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    
dyn.attach(printenergy, interval=10)

traj = Trajectory("./MD.traj", "w", atoms)
dyn.attach(traj.write, interval=10)

dyn.run(500)
