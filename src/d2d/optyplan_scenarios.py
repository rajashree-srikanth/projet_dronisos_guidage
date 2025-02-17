#
# Scenarios for the single vehicle planner
#

import numpy as np, sympy as sym

import d2d.opty_utils as d2ou

class exp_0:
    ncases = 1
    tol, max_iter = 1e-5, 1500
    vref = 12.
    cost = d2ou.CostAirVel(vref)
    #cost = d2ou.CostBank()
    obj_scale = 1.
    wind = d2ou.WindField(w=[0.,0.])
    obstacles = ( )
    t0, p0 = 0.,  ( 0.,  0.,    0.,    0., 10.)    # initial position: t0, ( x0, y0, psi0, phi0, v0)
    t1, p1 = 10., ( 0., 30., np.pi,    0., 10.)    # final position
    x_constraint, y_constraint = None, None
    #x_constraint, y_constraint = (-5., 100.), (-50., 50.) 
    phi_constraint = (-np.deg2rad(30.), np.deg2rad(30.))
    v_constraint = (9., 14.)
    hz = 50.
    name = 'exp0'
    desc = 'Turn around - 12m/s objective'
    def set_case(idx): pass
    def label(idx): return f'{idx}'

class exp_0_1(exp_0):
    tol, max_iter = 1e-5, 5000
    #cost = d2ou.CostBank()
    #cost = d2ou.CostComposit(None, 11., kobs=0., kvel=0.1, kbank=10.)
    t1s = [7., 10., 15., 20, 30]
    ncases = len(t1s)
    #x_constraint, y_constraint = (-5., 50.), (-20., 70.)
    #wind = d2ou.WindField(w=[-3.,0.])
    def set_case(idx):
        exp_0.t1 = exp_0_1.t1s[idx]
    def label(idx): return f'{exp_0_1.t1s[idx]:.1f} s'
    name = 'exp0_1'
    desc = 'changing duration'

class exp_0_2(exp_0):
    name = 'exp0_2'
    desc = 'changing wind'
    tol, max_iter = 1e-5, 5000
    winds = [[0., 0.], [1., 0.], [2., 0.], [5., 0.]]
    #winds = [[0., 0.], [1., 0.], [2., 0.], [5., 0.], [7., 0.], [10., 0.], [12., 0.]]
    ncases = len(winds)
    def set_case(idx):
        exp_0.wind = d2ou.WindField(w=exp_0_2.winds[idx])
    def label(idx): return f'wind {exp_0_2.winds[idx]} m/s'


class exp_0_3(exp_0):
    name = 'exp0_3'
    desc = 'xy constraints'
    tol, max_iter = 1e-5, 5000
    cost = d2ou.CostBank()
    obj_scale = 1.e-1
    x_constraint, y_constraint = (-5., 45.), (-1., 51.)
    t1 = 20.
    
    
class exp_1(exp_0):   # input objectives
    name = 'exp_1'
    desc = 'combined phi/vel objective'
    t0, p0 = 0.,  ( 0.,   0., 0.,    0., 12.)    # initial position: t0, ( x0, y0, psi0, phi0, v0)
    t1, p1 = 10., ( 100., 0., 0.,    0., 12.)    # final position

    cost, obj_scale = d2ou.CostInput(vsp=12., kvel=1., kbank=50.), 1.
    
    
class exp_1_1(exp_1):   # varying weight for vel and bank
    name = 'exp_1_1'
    desc = 'combined phi/vel objective'
    Ks = [[1., 0.5], [1., 1.],[1., 10.],[1., 20.], [1., 30.], [1., 40.], [1., 50.]]
    ncases = len(Ks)
    def set_case(idx):
        exp_1_1.K = exp_1_1.Ks[idx]
        exp_1_1.cost = d2ou.CostInput(vsp=12., kvel=exp_1_1.K[0], kbank=exp_1_1.K[1])
        
    def label(idx): return f'kvel, kbank {exp_1_1.K}'
    
class exp_421(exp_0):
    cost = d2ou.CostBank()
    name = 'exp1'
    desc = 'min mean bank objective'

class exp_2(exp_0):
    cost = d2ou.CostComposit(None, 11., kobs=0., kvel=0.1, kbank=10.)
    name = 'exp2'
    desc = 'bank/vel obective'

class exp_2_1(exp_2):
    #cost = d2ou.CostBank()
    cost = d2ou.CostComposit(None, 12., kobs=0., kvel=0.5, kbank=1.)
    obj_scale = 1.
    x_constraint, y_constraint = (-5., 35.), (-5., 35.)
    t1 = 20. 
    name = 'exp3'
    desc = 'bank/vel obective, xy constraints'

class exp_3(exp_0):
    name = 'exp3'
    desc = 'input_cost'
    cost = d2ou.CostInput(vsp=15., kvel=1., kbank=1.)
    p0s = d2ou.pts_on_circle(c=(0,0), r=20, alpha0=-3*np.pi/4., dalpha=np.deg2rad(20), n=5)
    def p1s(idx): return ( 0., 30.+2*idx, np.pi,    0., 10.)
    ncases = len(p0s)
    t1, p1 = 10., ( 0., 30., np.pi,    0., 10.)    # final position
    def set_case(idx):
        exp_3.p0 = exp_3.p0s[idx]
        exp_3.p1 = exp_3.p1s(idx)
    def label(idx): return f'{idx}'
        
class exp_4(exp_0):  # Obstacles  - reference for multi aircraft version
    t0, p0 = 0., ( 0., 0., 0,    0., 10.)    # initial position
    t1, p1 = 6.5, ( 50., 0., 0,    0., 10.)  # final position
    obstacles = ((25, -20, 10), )
    cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=0.5, kbank=1.)
    obj_scale = 1.e-2
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    x_constraint, y_constraint = (-5., 105.), (-15., 35.)
    #v_constraint = (11.99, 12.01)
    v_constraint = (9., 15.)
    name = 'exp4'
    desc = 'obstacle - simple case'

class exp_4_1(exp_0):  # Obstacles  - reference for multi aircraft version
    t0, p0 = 0., ( 0., 0., 0,    0., 10.)    # final position
    t1, p1 = 8.5, ( 100., 0., 0,    0., 10.)    # final position
    obstacles = ((50, -10, 25), )
    #cost = d2ou.CostObstacle(obstacles[0][:2], obstacles[0][2], kind=0)
    #cost = d2ou.CostObstacle(obstacles[0][:2], obstacles[0][2], kind=1)
    cost = d2ou.CostInput(vsp=12., kvel=0.5, kbank=1.)
    #cost = d2ou.CostComposit(obstacles, vsp=12., kobs=0.5, kvel=0.5, kbank=1., obs_kind=1)
    obj_scale = 1.e-2
    x_constraint = (-5., 105.)
    y_constraint = (-10., 40.)
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    #v_constraint = (11.99, 12.01)
    v_constraint = (9., 15.)
    name = 'exp4_1'
    desc = 'obstacle - simple case'

class exp_4_2(exp_0):  # Testing obstacles in maze like configuration
    t1, p1 = 15., ( 100., 0., 0,    0., 10.)    # final position
    obstacles = ((25, 0, 15), (55, 7.5, 12), (80, -10, 12))
    cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=0.5, kbank=1.)
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    obj_scale = 1.e-2
    x_constraint = (-5., 105.)
    #y_constraint = (-10., 25.) # fails
    y_constraint = (-15., 35.) #(-20., 20.)
    v_constraint = (11.99, 12.01)
    v_constraint = (9., 15.)
    name = 'exp4'
    desc = 'obstacles - maze'

class exp_4_3(exp_0):  # Testing obstacles in maze like configuration
    t1, p1 = 15., ( 100., 0., 0,    0., 10.)    # final position
    obstacles = ((25, 0, 15), (55, 7.5, 12), (80, -10, 12))
    cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=0.5, kbank=1.)
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    obj_scale = 1.e-2
    x_constraint = (-5., 105.)
    #y_constraint = (-10., 25.) # fails
    y_constraint = (-15., 35.) #(-20., 20.)
    v_constraint = (11.99, 12.01)
    v_constraint = (9., 15.)
    name = 'exp4'
    desc = 'obstacles - maze'

class exp_5(exp_0):
    t0, p0 =  0., (   0., 40., 0,   0., 10.)    # start position 
    t1, p1 = 12., ( 100., 40., 0,   0., 10.)    # end position
    obstacles = []
    for i in range(5):
        for j in range(5):
            if (i+j)%2:
                obstacles.append((i*20., j*20., 10.))
    if 1:
        cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=10., kbank=1.)
    else:
        cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=10., kbank=1.)
        obj_scale = 1.e-4
        t1 = 15.
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    name = 'exp5'


#
# formation flight
#
class exp_6(exp_0):
    ncases = nac = 4
    vref = 12.
    exp_0.t1 = 15.
    #x_constraint, y_constraint = (-10., 105.), (0, 100)
    #x_constraint, y_constraint = (-50., 105.), (0, 100)
    x_constraint, y_constraint = None, None
    seed = 6789; rng = np.random.default_rng(seed)
    p0s = d2ou.random_states(rng, nac, xlim=(0, 50), ylim=(-50, 0), v=vref)
    p1s = d2ou.line_formation(nac, (50, 50), np.pi, dx=2.5, dy=2.5, v=vref)
    def set_case(idx): exp_0.p0 = exp_6.p0s[idx]; exp_0.p1 = exp_6.p1s[idx] 
    def label(idx): return f'{idx}'
    name = 'exp6'
    desc = '  Rendez-vous, random start, 15s, line formation arrival'

class exp_6_1(exp_6):
    name = 'exp6_1'
    desc = 'Rendez-vous, random start, 15s, arrow formation arrival'
    p1s = d2ou.arrow_formation(exp_6.nac, (50, 50), np.pi, dx=2.5, dy=2.5, v=12.)
    def set_case(idx): exp_0.p0 = exp_6_1.p0s[idx]; exp_0.p1 = exp_6_1.p1s[idx] 

class exp_6_2(exp_6):
    name = 'exp6_2'
    desc = 'Rendez-vous, random start, 15s, diamond formation arrival'
    p1s = d2ou.diamond_formation(exp_6.nac, (50, 50), np.pi, dx=2.5, dy=2.5, v=12.)
    def set_case(idx): exp_0.p0 = exp_6_2.p0s[idx]; exp_0.p1 = exp_6_2.p1s[idx]
    
class exp_6_3(exp_6):
    ncases = nac = 5
    name = 'exp6_3'
    desc = 'Rendez-vous circular start, 15s, arrow formation arrival'
    c, r, alpha0, dalpha = np.array([0, -25]), 25., -np.pi, np.deg2rad(30.)
    p0s = d2ou.circle_formation(nac, c, r, alpha0, dalpha, exp_6.vref)
    p1s = d2ou.arrow_formation(nac, (50, 50), np.pi, dx=2.5, dy=2.5, v=exp_6.vref)
    def set_case(idx): exp_0.p0 = exp_6_3.p0s[idx]; exp_0.p1 = exp_6_3.p1s[idx] 

class exp_6_4(exp_6_3):
    name = 'exp6_4'
    desc = 'Rendez-vous circular start, 20s, arrow formation arrival'
    t1 = 20.

    
class exp_6_5(exp_6_3):
    name = 'exp6_5'
    desc = 'Rendez-vous, circular start, 30s, arrow formation arrival'
    t1 = 30.
    
class exp_6_6(exp_6_3):
    name = 'exp6_6'
    desc = 'Rendez-vous, circular start, 40s, arrow formation arrival'
    t1 = 40.

class exp_6_7(exp_6_3):
    name = 'exp6_7'
    desc = 'Rendez-vous, circular start, alpha0=-pi/2, 20s, arrow formation arrival'
    t1 = 20.
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    v_constraint = (11., 13.)
    p0s = d2ou.circle_formation(exp_6_3.nac, exp_6_3.c, exp_6_3.r, -np.pi/2, exp_6_3.dalpha, exp_6.vref)
    def set_case(idx): exp_0.p0 = exp_6_7.p0s[idx]; exp_0.p1 = exp_6_7.p1s[idx] 

class exp_6_8(exp_6_2):
    name = 'exp6_8'
    desc = 'Rendez-vous, circular start, many aircraft, 20s, arrow formation arrival'
    ncases = nac = 12
    t1 = 20.
    p0s = d2ou.circle_formation(nac, exp_6_3.c, exp_6_3.r, -np.pi/2, exp_6_3.dalpha, exp_6.vref)
    #p1s = d2ou.arrow_formation(nac, (50, 50), np.pi, dx=2.5, dy=2.5, v=exp_6.vref)
    p1s = d2ou.diamond_formation(nac, (50, 50), np.pi, dx=7.5, dy=5., v=exp_6.vref)
    def set_case(idx): exp_0.p0 = exp_6_8.p0s[idx]; exp_0.p1 = exp_6_8.p1s[idx] 
    
scens = [exp_0, exp_0_1, exp_0_2, exp_0_3,
         exp_1, exp_1_1, exp_2, exp_3, exp_4, exp_4_1, exp_4_2, exp_5,
         exp_6, exp_6_1, exp_6_2, exp_6_3, exp_6_4, exp_6_5, exp_6_6, exp_6_7, exp_6_8]

def desc_all(): return '\n'.join([f'{i}: {s.name} {s.desc}' for i, s in enumerate(scens)])

def desc_one(idx):
    s = scens[idx]
    desc = f'{s.name} {s.desc}\n'
    desc += f'initial state {s.t0} {s.p0}\n'
    desc += f'final state {s.t1} {s.p1}\n'
    return desc
