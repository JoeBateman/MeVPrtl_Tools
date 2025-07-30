# MeV Portal Tools

This repo contains the tools I've made/modified to begin working with the outputs of the MeVPrtl generator.

Take a look at `mevprtl_hnl_test.fcl` to begin running the generator and simulating various HNL decays, then use the `visualiser.ipynb` notebook to take a look at the output `hist_*.root` files. 

Compatibility:

- `mevprtl_hnl_test.fcl` runs out of the box with the (current) latest version of `sbndcode`, `v10_06_02`


- `visualiser.ipynb` was developed using python 3.10, and uses uproot, pandas and awkward to process files, and matplotlib/plotly to generate 2D/3D figures. 