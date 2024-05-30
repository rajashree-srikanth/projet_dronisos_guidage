

import numpy as np, sympy as sym

import d2d.opty_utils as d2ou

class exp_0:
    ncases = 1
    tol, max_iter = 1e-5, 1500
    cost = d2ou.CostAirVel(12.)
    #cost = d2ou.CostBank()
    obj_scale = 1.
    wind = d2ou.WindField(w=[0.,0.])
    obstacles = ( )
    t0, p0 = 0.,  ( 0.,  0.,    0.,    0., 10.)    # initial position: t0, ( x0, y0, psi0, phi0, v0)
    t1, p1 = 10., ( 0., 30., np.pi,    0., 10.)    # final position
    x_constraint, y_constraint = None, None
    phi_constraint = (-np.deg2rad(30.), np.deg2rad(30.))
    v_constraint = (9., 12.)
    hz = 50.
    name = 'exp0'
    desc = 'Turn around - 12m/s objective'
    def set_case(idx): pass
    def label(idx): return ''

class exp_0_1(exp_0):
    tol, max_iter = 1e-5, 5000
    cost = d2ou.CostBank()
    t1s = [7., 10., 15., 20]
    ncases = len(t1s)
    def set_case(idx):
        exp_0.t1 = exp_0_1.t1s[idx]
    def label(idx): return f'{exp_0_1.t1s[idx]:.1f} s'
    name = 'exp0_1'
    desc = 'changing duration'

class exp_0_2(exp_0):
    tol, max_iter = 1e-5, 5000
    winds = [[0., 0.], [1., 0.], [2., 0.], [5., 0.]]
    ncases = len(winds)
    def set_case(idx):
        exp_0.wind = d2ou.WindField(w=exp_0_2.winds[idx])
    def label(idx): return f'wind {exp_0_2.winds[idx]} m/s'
    name = 'exp0_2'
    desc = 'changing wind'


class exp_1(exp_0):
    tol, max_iter = 1e-5, 5000
    cost = d2ou.CostBank()
    obj_scale = 1.e-1
    name = 'exp1'
    desc = 'xy constraints'
    x_constraint, y_constraint = (-5., 45.), (-1., 51.)
    t1 = 20.
    
    
    
    
class exp_421(exp_0):
    cost = d2ou.CostBank()
    name = 'exp1'
    desc = 'min mean bank objective'

class exp_2(exp_0):
    cost = d2ou.CostComposit(None, 11., kobs=0., kvel=0.1, kbank=10.)
    name = 'exp2'
    desc = 'bank/vel obective'

class exp_3(exp_2):
    #cost = d2ou.CostBank()
    cost = d2ou.CostComposit(None, 12., kobs=0., kvel=0.5, kbank=1.)
    obj_scale = 1.
    x_constraint, y_constraint = (-5., 35.), (-5., 35.)
    t1 = 20. 
    name = 'exp3'
    desc = 'bank/vel obective, xy constraints'

class exp_4(exp_0):
    t1, p1 = 10., ( 100., 0., 0,    0., 10.)    # final position
    obstacles = ((25, 0, 15), (55, 7.5, 12), (80, -10, 12))
    cost = d2ou.CostComposit(obstacles, vsp=15., kobs=0.5, kvel=0.5, kbank=1.)
    phi_constraint = (-np.deg2rad(40.), np.deg2rad(40.))
    obj_scale = 1.e-2
    x_constraint = (-5., 105.)
    y_constraint = (-15., 25.) #(-20., 20.)
    name = 'exp4'

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
    
scens = [exp_0, exp_0_1, exp_0_2, exp_1, exp_2, exp_3, exp_4, exp_5]

def desc_all():
    return '\n'.join([f'{i}: {s.name} {s.desc}' for i, s in enumerate(scens)])

def desc_one(idx):
    s = scens[idx]
    desc = f'{s.name} {s.desc}\n'
    desc += f'initial state {s.t0} {s.p0}\n'
    desc += f'final state {s.t1} {s.p1}\n'
    return desc
