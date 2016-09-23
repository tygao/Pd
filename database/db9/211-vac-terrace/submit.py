#!/usr/bin/env python
from __future__ import print_function
from vasp import Vasp
from ase.md.langevin import Langevin
from ase.io.trajectory import Trajectory
from ase import units
from amp import Amp

calc = Vasp("./../../../NDFT/surface=fcc211/type=vacancy/site=terrace")

atoms = calc.get_atoms()

atoms.set_calculator(Amp(load="./../../../networks/db9/15-15/checkpoint-parameters.json"))

dyn = Langevin(atoms, 5 * units.fs, 900 * units.kB, 0.002)


def printenergy(a=atoms):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    
dyn.attach(printenergy, interval=5)

traj = Trajectory("./MD.traj", "w", atoms)
dyn.attach(traj.write, interval=5)

dyn.run(200)
