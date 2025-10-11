

# Grain-scale LTNE heat transport model in 2D 

This repository accompanies the manuscript:

Lee, H., Gebhardt, H., Blum, P., Bayer, P., Rau, G.C. (202X): Numerical analysis of local thermal non-equilibrium experiments reveals conceptual regimes of grain-scale heat transport

The repository provides scripts to perform transient heat transport simulation at the granular scale in 2D porous media using the Multiphysics Object-Oriented Simulation Environment ([MOOSE](https://mooseframework.inl.gov/)), an open-source, parallel finite element framework for numerical modelling (Permann et al., 2020). The heat transport model is created using the MOOSE library [PorousFlow](https://mooseframework.inl.gov/modules/porous_flow/index.html) (Wilkins et al., 2021) and [HeatTransfer](https://mooseframework.inl.gov/modules/heat_transfer/index.html), which enable the simulation of flow in porous media and heat conduction within the solid grain. This repository further provides routines to produce thermal breakthrough curves and temperature difference between the fluid and solid phases (i.e., LTNE effect at the grain-scale).

To run this grain-scale heat transport model, [MOOSE](https://mooseframework.inl.gov/) must be [installed](https://mooseframework.inl.gov/getting_started/installation/index.html) and an [application created](https://mooseframework.inl.gov/getting_started/new_users.html), with the [PorousFlow](https://mooseframework.inl.gov/modules/porous_flow/index.html), [HeatTransfer](https://mooseframework.inl.gov/modules/heat_transfer/index.html) and [Misc](https://mooseframework.inl.gov/modules/misc/index.html) libraries enabled in the Makefile. 

## Structure

- `README.md` - description of the repository
- `LICENSE` - the default license is MIT
- `requirements.txt` - requirements for [pip](https://pip.pypa.io/en/stable/user_guide/#requirements-files) to install all needed packages
- `data/` - contains experimental data and boundary condition data required for the simulations
  - `bc_data/` - experimental data used for model boundary condition
- `input/` - contains MOOSE input files to run grain-scale heat transport simulations
	- `mesh/` - contains mesh generating script and text files with coordiates of a grain
	- `K_distribution/` - contains permeability distribution profile for the non-uniform flow model
	- `model_hsf_empirical/` - contains input files for the model using the heat transfer coefficient estimated by empirical correlation
  - `model_hsf_max/` -  contains input files for the model using the possible maximum heat transfer coefficient
  - `model_non_uniform_flow/` -  contains input files for the non-uniform flow model with varied permeability distribution
- `results/` - contains grain-scale heat transport model results
	- `hsf_empirical/` - contains results from the model simulation using the heat transfer coefficient estimated by empirical correlation
  - `hsf_max/` -  contains results from the model simulations using the possible maximum heat transfer coefficient
  - `non_uniform_flow/` -  contains results from the non-uniform flow model simulations with varied permeability distribution
- `script/` - contains all scripts used for post-analysis and plotting the results
	- `package/` - contains modules for running the scripts


## References
Harbour, L., Giudicelli, G., Lindsay, A. D., German, P., Hansel, J., Icenhour, C., . . . Permann, C. J. (2025). 4.0 MOOSE: Enabling massively parallel multiphysics simulation. SoftwareX , 31 , 102264. doi: 10.1016/j.softx.2025.102264

Wilkins, A., Green, C. P., & Ennis-King, J. (2021). An open-source multiphysics simulation code for coupled problems in porous media. Computers & Geosciences, 154(2a), 104820. doi: 10.1016/j.cageo.2021.104820

## Contact

You can contact us via <haegyeong.lee@kit.edu>.


## License

MIT © 2025
