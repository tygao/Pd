#!/usr/bin/env python
import os
from amp import Amp
from amp.descriptor import Gaussian
from amp.regression import NeuralNetwork
from ase.db import connect
from amp import SimulatedAnnealing

db = connect('../../../database/db10/data.db')
wd = os.getcwd()
images = []
for d in db.select('train_set=True'):
    atoms = db.get_atoms(d.id)
    del atoms.constraints
    images += [atoms]

calc = Amp(
           label='./',
	   dblabel='../../',
	   descriptor=Gaussian(cutoff=6.5),
	   regression=NeuralNetwork(hiddenlayers=(2, 24)))

calc.train(images=images,
	   data_format='db',
	   cores=8,
	   energy_goal=1e-3,
	   force_goal=1e-1,
	   global_search=SimulatedAnnealing(temperature=70,
					    steps=50),
	   extend_variables=False)
