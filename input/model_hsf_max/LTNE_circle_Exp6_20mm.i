###########################
#  LTNE MOOSE input file  #
###########################

# ==============================================================================
# MODEL PARAMETERS
# Unit: m, s, kg, K
# ==============================================================================

hsf_guess = 100000000000.0   
T_0 = 304.28          #[K] from BC file '../../data/bc_data/Exp6_20mm_BC_input_temp.csv'
q = 8.7e-05          #[m/s]
K_hydrau = 0.00323    #[m/s]
g = 9.8               #[m/s2]
lambda_sol = 1.0    #[W/(m*K)]
cs = 759              #[J/(kg*K)]
rho_s = 2585          #[kg/m3]
cf = 4182             #[J/(kg*K)]
rho_f = 997          #[kg/cm3]
mu = 0.001002         #[kg/(m*s)]
n = 0.37              #[-]
column_length = 0.4   #[m]
delta_pp = ${fparse q * rho_f * g * column_length / K_hydrau}
pp_in = 10000         #[Pa]
pp_out = ${fparse pp_in - delta_pp}
hsf = ${hsf_guess}


# ==============================================================================
# MESH
# ==============================================================================
[Mesh]
  [mesh_file]
    type = FileMeshGenerator
    file = '../mesh/sq_circle_20mm.msh'
  []
  [sideset]
    input = mesh_file
    type = SideSetsBetweenSubdomainsGenerator
    primary_block = domain
    paired_block = 'g1'
    new_boundary = sideset
  []
  [grain_boundary]
    input = sideset
    type = LowerDBlockFromSidesetGenerator
    sidesets = sideset
    new_block_id = 2
  []
[]


# ==============================================================================
# PHYSICS AND NUMERICS
# ==============================================================================
[UserObjects]
  [dictator]
   type = PorousFlowDictator
    porous_flow_vars = 'pp temp'
    number_fluid_phases = 1
    number_fluid_components = 1
  []
[]

[GlobalParams]
  PorousFlowDictator = dictator
   gravity = '0 0 0'
[]

[Variables]
  [pp]
   block = 'domain 2'
    initial_condition = 0
  []
  [temp]
    initial_condition = ${T_0}
    scaling = 1E-6
    block = 'domain 2'
  []
  [Tsolid]
    initial_condition = ${T_0}
    scaling = 1E-6
    block = '2 g1'
  []
[]

[Kernels]
  [mass_water_dot]
    type = PorousFlowMassTimeDerivative
    fluid_component = 0
    variable = pp
    block = 'domain'
  []
  [flux]
    type = PorousFlowFullySaturatedAdvectiveFlux
    fluid_component = 0
    variable = pp
    gravity = '0 0 0'
    block = 'domain'
  []
  [energy_dot]
    type = PorousFlowEnergyTimeDerivative
    variable = temp
    block = 'domain'
  []
  [heat_conduction]
    type = PorousFlowHeatConduction
    variable = temp
    block = 'domain'
  []
  [heat_advection]
    type = PorousFlowFullySaturatedUpwindHeatAdvection
    variable = temp
    block = 'domain'
  []
  [solid_time_derivative]
    type = HeatConductionTimeDerivative
    variable = Tsolid
    block = 'g1'
  []
  [solid_heat_conduction]
    type = HeatConduction
    variable = Tsolid
    block = 'g1'
  []
  [heat_transfer_toFluid]
    type = PorousFlowHeatMassTransfer
    variable = temp
    v = Tsolid
    transfer_coefficient = ${hsf}
    block = 2
  []
  [heat_transfer_toSolid]
    type = PorousFlowHeatMassTransfer
    variable = Tsolid
    v = temp
    transfer_coefficient = ${hsf}
    block = 2
  []
[]

[Functions]
  [known_T_bc]
    type = PiecewiseLinear
    data_file = '../../data/bc_data/Exp6_20mm_BC_input_temp.csv'
    format = columns
  []
  [K_fcn]
    type = PiecewiseMulticonstant
    direction = 'left right'
    data_file = '../K_distribution/K_dist_0.data'
  []
[]

[BCs]
  [top_pp]
    type = DirichletBC
    variable = pp
    boundary = top
    value = ${pp_in}
  []
  [bottom_pp]
    type = DirichletBC
    variable = pp
    boundary = bottom
    value = ${pp_out}
  []
  [var_temp]
    type = FunctionDirichletBC
    variable = temp
    function = known_T_bc
    boundary = top
  []
  [temperature_bottom]
   type = DirichletBC
    variable = temp
    value = ${T_0}
    boundary = bottom
  []
[]

[AuxVariables]
  [hsf]
     family = MONOMIAL
     order = CONSTANT
  []
  [swater]
     family = MONOMIAL
     order = CONSTANT
  []
  [darcy_vel_x]
     family = MONOMIAL
     order = CONSTANT
     block='domain'
  []
  [darcy_vel_y]
     family = MONOMIAL
     order = CONSTANT
     block='domain'
  []
  [K]
     family = MONOMIAL
     order = CONSTANT
  []
[]

[AuxKernels]
  [swater]
     type = PorousFlowPropertyAux
     variable = swater
     property = saturation
     block='domain'
  []
  [darcy_vel_x]
     type = PorousFlowDarcyVelocityComponent
     variable = darcy_vel_x
     component = x
     gravity = '0 0 0'
  []
  [darcy_vel_y]
     type = PorousFlowDarcyVelocityComponent
     variable = darcy_vel_y
     component = y
     gravity = '0 0 0'
  []
  [K]
     type = FunctionAux
     function = K_fcn
     variable = K
     execute_on = initial
  []
[]

[FluidProperties]
  [simple_fluid]
    type = SimpleFluidProperties
    bulk_modulus = 2E9
    viscosity = ${mu}
    density0 = ${rho_f}
    thermal_expansion = 0
    cv = ${cf}
  []
[]

[Materials]
  [temperature]
    type = PorousFlowTemperature
    temperature=temp
    block = 'domain'
  []
  [ppss]
    type = PorousFlow1PhaseFullySaturated
    porepressure = pp
    block = 'domain'
  []
  [porosity]
    type = PorousFlowPorosityConst
    porosity = ${n}
    block = 'domain'
  []
  [permeability_aquifer]
    type = PorousFlowPermeabilityConstFromVar
    perm_xx = K
    perm_yy = K
    perm_zz = K
    block = 'domain'
  []
  [rock_heat]
    type = PorousFlowMatrixInternalEnergy
    specific_heat_capacity = ${cs}
    density = ${rho_s}
    block = 'domain'
  []
  [PF_lambda]
    type = PorousFlowThermalConductivityFromPorosity
    lambda_s = '1 0 0  0 1 0  0 0 1'
    lambda_f = '0.6 0 0  0 0.6 0  0 0 0.6'
    block = 'domain'
  []
  [simple_fluid]
    type = PorousFlowSingleComponentFluid
    fp = simple_fluid
    phase = 0
    block = 'domain'
  []
  [massfrac]
    type = PorousFlowMassFraction
    block = 'domain'
  []
  [relp]
    type = PorousFlowRelativePermeabilityConst
    phase = 0
    block = 'domain'
  []
  [solid_boundary_material]
    type = GenericConstantMaterial
    prop_names = 'thermal_conductivity'
    prop_values = '0.6'
    block = '2'
  []
  [grain_thermal_conductivity]
    type = HeatConductionMaterial
    thermal_conductivity = ${lambda_sol}
    specific_heat = ${cs}
    block = 'g1'
  []
  [grain_density]
    type = Density
    density = ${rho_s}
    block = 'g1'
  []
[]

# ==============================================================================
# EXECUTIONER AND TIME SETTING
# ==============================================================================
[Preconditioning]
  [smp]
    type = SMP
    full = true
    petsc_options_iname = '-pc_type -ksp_gmres_restart -sub_pc_type -sub_pc_factor_shift_type'
    petsc_options_value = 'asm      100                lu           NONZERO'
  []
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  start_time = 0
  dt = 1
  end_time = 6000
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
[]

# ==============================================================================
# POSTPROCESSORS DEBUG AND OUTPUTS
# ==============================================================================
[Postprocessors]
  [Ts]
    type = PointValue
    point = '0.145 0.2 0'
    variable = Tsolid
    execute_on = timestep_end
  []
  [Tf_1]
    type = PointValue
    point = '0.1330 0.2 0'
    variable = temp
    execute_on = timestep_end
  []
  [Tf_2]
    type = PointValue
    point = '0.1570 0.2 0'
    variable = temp
    execute_on = timestep_end
  []
  [v_1]
    type = PointValue
    point = '0.1330 0.2 0'
    variable = darcy_vel_y
    execute_on = timestep_end
  []
  [v_2]
    type = PointValue
    point = '0.1570 0.2 0'
    variable = darcy_vel_y
    execute_on = timestep_end
  []
[]
[Outputs]
#  exodus = true
  csv = true
[]
