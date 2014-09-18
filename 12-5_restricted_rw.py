#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, June 2014.

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from RestrictedRW import RestrictedRW as RRW


def plot3d_a_x_tau(amin=0, amax=10):

    list_a = np.repeat(
        np.array(range(amin, amax + 1))[:, np.newaxis], amax + 1, axis=1)
    list_x = np.repeat(np.array([range(0, amax + 1)]), amax + 1, axis=0)
    list_tau = np.zeros([amax + 1, amax + 1], 'f')

    from mpl_toolkits.mplot3d import Axes3D
    for _a in range(amin + 2, amax + 1):
        for _x in range(amin + 1, _a - 1):
            rw.restricted_rw_erase(a=_a, x0=_x)
            list_tau[_a][_x] = rw.ave_tau

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(list_a, list_x, list_tau, rstride=1, cstride=1)
    ax.set_xlabel(r'$a$', fontsize=16)
    ax.set_ylabel(r'$x_{0}$', fontsize=16)
    ax.set_zlabel(r'$\tau$', fontsize=16)
    plt.show()

if __name__ == '__main__':

    rw = RRW(walker=1000)
# comment out to use
#
#    rw.restricted_rw_erase(a=5, x0=2)
#    print rw.ave_tau, '+-', rw.std_tau/sqrt(rw.walker)
#
    plot3d_a_x_tau(amax=15)
#
#    rw.restricted_rw_reflect(N=1000, a=100)
#    rw.caluculate_prob(_n=900)
#
#    rw.random_walk_d1(N=1000)
#    rw.caluculate_prob(_n=900)
#
