import Parameter
from ground_structure import init_constraint_params, init_idm_params
#from userInterfaceDrawer import noise_mode

### INITIALIZE PARAMETER ###
Parameter._init()
Parameter.set_value('visible', True)

Parameter.set_value('step_number', 0)
Parameter.set_value('init_speed', 15)
Parameter.set_value('init_acc', 0)

Parameter.set_value('show_road_ID', True)
Parameter.set_value('barnumberlimit', 5)
Parameter.set_value('show_bar', True)
Parameter.set_value('control_value', False)
Parameter.set_value('Canvas_width', 1280)
Parameter.set_value('Window_Height', 850)
Parameter.set_value('userInterfaceFrame_width', 400)

Parameter.set_value('SCALE', 4)                             # Scale factor from pixel to meter. 1m = SCALE pixel
scale = Parameter.get_value('SCALE')
Parameter.set_value('LANEWIDTH', 5.0*scale)                 # Lane width in pixel
Parameter.set_value('CAR_Dimension', [7*scale, 5*scale])    # Car width in pixel

Parameter.set_value('slow_motion', 0.5)
Parameter.set_value('delta_t', 0.1)                         # Sampling time
Parameter.set_value('spawnNewCarCounter', 0)                # Parameters used to control car generation
Parameter.set_value('spawnNewCarLimit', 36)


### INITIALIZE ALL AGENTS PARAMS ###
constraint_params = init_constraint_params(v_max=50, v_min=0.0, a_max=10, b_max=-16.0, t_react=0.5,
                                                         d_max=200, car_length=7,
                                                         a_duration=1.0)
idm_params = []
for i in range(15):
    idm_params.append(init_idm_params(v_0=16+0.4*i, b_comf=-4.0-0.4*i, d_0=2.0, T_idm=1.5-0.1*i,
                                      v_exp=4.0, d_exp=2.0, advance_mode='idm', noise_mode=0))
# before select the drive mode,the car will drive in idm mode without noise


Parameter.set_value('constraint_params', constraint_params)
Parameter.set_value('idm_params', idm_params)







