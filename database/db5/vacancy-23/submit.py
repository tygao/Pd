#!/usr/bin/env python
from __future__ import print_function
from ase.lattice.surface import fcc111
from ase.md.langevin import Langevin
from ase.io.trajectory import Trajectory
from ase import units
from amp import Amp
from ase.constraints import FixAtoms

atoms = fcc111("Pd", size=(2, 3, 5), a=3.939, vacuum=6.0)
del atoms[-1]
constraint = FixAtoms(mask=[atom.tag > 3 for atom in atoms])
atoms.set_constraint(constraint)
atoms.set_calculator(Amp(load="./../../../networks/db5/20-20/checkpoint-parameters.json"))

dyn = Langevin(atoms, 5 * units.fs, 900 * units.kB, 0.002)


def printenergy(a=atoms):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    
dyn.attach(printenergy, interval=10)

traj = Trajectory("./MD.traj", "w", atoms)
dyn.attach(traj.write, interval=10)

dyn.run(2000)
