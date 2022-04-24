import math


######### xva means position x, speed v & acceleration a##############
## return predicted xva state which is delta_t in the future
def calc_next_xva_state(x, v, a, delta_t, v_min=None, v_max=None, const_acc=False):

    if const_acc:  ## do CA prediction
        next_a = a
    else:  ## do CV prediction
        next_a = 0.0
    next_v = v + a * delta_t  # prediction of v completed

    # check if next_v would violate speed limits
    if v_min is not None and next_v <= v_min:  # if v_min is defined and is not reached
        a = (v_min - v) * delta_t
        next_a = 0.0  ## Wechsel zu CV
        next_v = v_min
    if v_max is not None and next_v >= v_max:  # if v_max is defined and exceeded
        a = (v_max - v) * delta_t
        next_a = 0.0  ## Wechsel zu CV
        next_v = v_max

    next_x = x + v * delta_t + 0.5 * a * delta_t * delta_t   # next_x = x + v*dt + 1/2*a*(dt)^2
    return next_x, next_v, next_a



## Es folgen 4 Hilfsfunktionen:

## return braking distance with reaction time t_react and CA
def calc_distance_to_stop_CA_braking(v, a, t_react=0.0):
    if ((v >= 0) and (a < 0)):  # deceleration from foreward drive
        return (v * t_react + v ** 2 / (-2.0 * a))
    else:
        return None


## return sicherheitsabstand zum Vordermann (Annahme: beide bremsen CA (Hintermann verzoegert mit t_react)) und ich will einen Minimalabstand d_min nie unterschreiten)
## result is scalar
def safe_distance_CA_braking(v, a, t_react, v_other, a_other, d_min):
    # It is assumed that x_other >= x
    d = calc_distance_to_stop_CA_braking(v, a, t_react)
    d_other = calc_distance_to_stop_CA_braking(v_other, a_other)
    result = d_min + max(d - d_other, 0.0)
    return result


## return the Sollabstand d* of the last term of idm, which ensures enough distance to the front
## v, v_other, a_max, t_react, b, d_0 : my car speed, the front car speed, max. acceleration, reaction time=Folgezeit=safety time gap, comfort deceleration b, minimum/ traffic jam distance d_0,
def safe_distance_idm(v, v_other, d_0, T_idm, a_max, b=None):
    if b is None:
        b = a_max
    a_max = abs(a_max)
    b = abs(b)
    result = d_0 + abs(v) * T_idm + v * (v - v_other) / (2.0 * math.sqrt(a_max * b))
    result = max(0.1, result)
    return result


## return (general) IDM gradient
def dvdt_idm(v, v_other, distance, d_0, T_idm, a_max, b_comf, b_max, t_react=0.5, v_target=33.3, v_exp=1.0, d_exp=1.0, ext=False, limited=False, idm_mode=None):
    # d = distance
    d = max(distance, 0.001)

    if ext:
        # use const.acc. to calculate sollabstabd d*  = d_0 + (Bremsweg ego [CA with a=b] - Bremsweg other [CA with a_other=b])
        d_target = safe_distance_CA_braking(v=v, a=b_comf, t_react=t_react, v_other=v_other, a_other=b_comf, d_min=d_0)
    else:
        # use IDM to calculate Sollabstand d* from (IDM(2))=(FDM(2))
        d_target = safe_distance_idm(v=v, v_other=v_other, d_0=d_0, T_idm=T_idm, a_max=a_max, b=b_comf)

    if idm_mode in [None, 'idm', 'ext_idm', 'lim_idm']:  # IDM (original formula)
        ## general version of IDM(1)=FDM(1) dvdt= a*( 1 - (v/v_soll)^v_exp - ( s*/s)^d_exp
        dvdt = a_max * (1.0 - (v / v_target) ** v_exp - (d_target / d) ** d_exp)
    elif idm_mode in ['lim_idm+']:  # IDM+
        dvdt = a_max * min((1.0 - (v / v_target) ** v_exp), (1 - (d_target / d) ** d_exp))
    else:  # IDM alternative
        dvdt = a_max * (1.0 - (v / v_target) ** v_exp) * (1.0 - (d_target / d) ** d_exp)  # alternative calculation

    if limited:  # ensure that the allowable limit value is not exceeded
       real_break_max = abs(b_max)
       if dvdt < 0:     # breaking
           return max(-real_break_max, dvdt)
       elif dvdt >= 0:  # acceleration
           return min(a_max, dvdt)
    else:
        return dvdt


####################################Parameter######################################

def init_constraint_params(v_max, v_min, a_max, b_max, t_react=0.0, d_max=200, car_length=5.0, a_duration=1.0):  ## used for LongTraj1D and Agent constructor
        constraint_params = {
            'v_max': v_max,  # m/s, e.g. 50 m/s = 180 km/h
            'v_min': v_min,  # m/s
            'a_max': a_max,  # m/s^2                ## maximale Beschleunigung, d.h. Bodenblech
            'b_max': b_max,  # m/s^2                ## maximale Verzoegerung, d.h. Vollbremsung, emergency break
            't_react': t_react,  # s                ## reaction time of the agent
            'd_max': d_max,                         ## car with a distance bigger than d_max aren't considered in risk evaluation
            'car_length': car_length,               ## Car length
            'a_duration': a_duration,               ## s, duration of acceleration period (of e.g. IDM or FDM)
        }
        return constraint_params


def init_idm_params(b_comf, v_0, d_0, T_idm, v_exp, d_exp, advance_mode,noise_mode):
        idm_params = {
            'b_comf': b_comf,    ## komfortable Bremsbeschleunigung <0 (b bei safe distance idm)  m/s^2
            'd_0': d_0,          ## minimal distance (in traffic jam), bumper to bumper
            'v_0': v_0,          ## desired cruise velocity IDM m/s
            'T_idm': T_idm,      ## idm safety time gap
            'v_exp': v_exp,      ## exponent (sigma) of the speed fractional term in the idm calculation, by default v_exp=4
            'd_exp': d_exp,      ## exponent of the distance fractional term in the idm calculation, by default d_exp=2
            'advance_mode': advance_mode,
            'noise_mode':noise_mode,
        }
        return idm_params

#######################################################################################################################
####################################################################################################

## Env for Enviroment (Umgebung), defines all recognized traffic participants and obstacles
def Env(long_agents=None, paral_agents=None, merge_agents=None, intersect_agents=None):
    # long_agents = List of other cars on the same path as current car
    if long_agents is None: ##define empty long_agents to prevent compilation error
        long_agents = []
    # merge_agents: the cars, which on the different lanes, in next time will drive on the same lane
    if merge_agents is None:
        merge_agents = []
    # other cars parallel to current car (for multilane driving)
    if paral_agents is None:
        paral_agents = []

    if intersect_agents is None:
        intersect_agents = []

    # other cars that intersect the current car's path (for crossings, intersections, etc.))
    env = {
        'long_agents': long_agents,             # agents in their own lane, always take into account
        'merge_agents': merge_agents,           # agents that are about to enter a merge scenario with the respective agent
        'paral_agents': paral_agents,           # no consideration during normal driving (only interesting when changing lanes on 2 lane road)
        'intersect_agents': intersect_agents,   # agents in lanes about to intersect with other lanes
    }

    return env




