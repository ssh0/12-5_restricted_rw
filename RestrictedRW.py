#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, June 2014.

import numpy as np
import matplotlib.pyplot as plt


class RestrictedRW:

    def __init__(self, walker=1000, alpha=0.5):

        self.walker = walker  # walker
        self.alpha = alpha

    def restricted_rw_erase(self, a=5, x0=2):

        self.a = a
        self.x0 = x0  # integer between (0,a)
        self.x = np.tile([self.x0], self.walker).reshape((self.walker, 1))
        x = self.x
        self.tau = np.zeros(self.walker, 'int32')

        while min(self.tau) == 0:
            # random walk
            x = np.insert(x, len(x[0]), 0, axis=1)

            for m in xrange(self.walker):
                if not x[m][-2] == 0:
                    p = np.random.rand()
                    if p < self.alpha:
                        x[m][-1] = x[m][-2] + 1
                    else:
                        x[m][-1] = x[m][-2] - 1

                    if x[m][-1] == 0 or x[m][-1] == self.a:
                        x[m][-1] = 0
                        self.tau[m] = len(x[m]) - 1
        else:
            # caluculate
            self.ave_tau = np.average(self.tau)
            self.std_tau = np.std(self.tau)

    def restricted_rw_reflect(self, N=10, a=5):

        self.a = a
        self.x0 = 0
        self.N = N
        self.x = np.tile([self.x0], self.walker).reshape((self.walker, 1))
        x = self.x

        for n in xrange(1, N):
            x = np.insert(x, len(x[0]), 0, axis=1)
            for m in xrange(self.walker):
                if x[m][-2] == -self.a:
                    x[m][-1] = -self.a + 1
                elif x[m][-2] == self.a:
                    x[m][-1] = self.a - 1
                else:
                    p = np.random.rand()
                    if p < self.alpha:
                        x[m][-1] = x[m][-2] + 1
                    else:
                        x[m][-1] = x[m][-2] - 1
        self.x = x

    def random_walk_d1(self, N=10):

        x = np.zeros([self.walker, N], 'i')

        # generate random number in [0,1)
        p = np.random.random([self.walker, N - 1])
        prob = self.alpha
        l = 1
        x0 = 0

        for n in xrange(self.walker):
            x[n][0] = x0
            for i in xrange(1, N):
                d = +l if p[n][i - 1] < prob else -l
                x[n][i] = x[n][i - 1] + d
        self.x = x
        self.N = N
        self.a = N

    def caluculate_prob(self, _n=6):

        x = self.x

        count_box = np.zeros([self.N, 2 * self.a + 1], 'f')
        for n in xrange(self.N):
            for m in xrange(self.walker):
                count_box[n][self.a + x[m][n]] += 1
        prob = count_box / self.walker

        def show_for_n(_n):

            xmin = -self.a
            xmax = self.a

            for _x in xrange(2 * self.a + 1):
                if prob[_n][_x] != 0:
                    xmin, xmax = _x - self.a, self.a - _x
                    break

            xmargin = xmax * 0.1
            ymax = np.amax(prob[_n])
            ymargin = ymax * 0.1

            fig = plt.figure('probability')
            ax = fig.add_subplot(111)
            ax.grid()
            ax.set_xlim(xmin - xmargin, xmax + xmargin)
            ax.set_ylim(0, ymax + ymargin)
            ax.plot(xrange(-self.a, self.a + 1), prob[_n])
            ax.set_xlabel(r'$x$', fontsize=16)
            ax.set_ylabel(r'$P(x,N)$', fontsize=16)
            plt.show()

        show_for_n(_n)

if __name__ == '__main__':

    def test(target):
        rw = RestrictedRW(walker=1000)
        if target == 'erase':
            from math import sqrt
            rw.restricted_rw_erase(a=5, x0=2)
            print rw.ave_tau, '+-', rw.std_tau / sqrt(rw.walker)
        elif target == 'reflect':
            rw.restricted_rw_reflect(N=1000, a=100)
            rw.caluculate_prob(_n=900)
        else:
            pass

    test('erase')
