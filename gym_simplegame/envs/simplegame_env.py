import sys
from contextlib import closing

import numpy as np
from six import StringIO, b

from gym import utils
from gym.envs.toy_text import discrete

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3



class SimplegameEnv(discrete.DiscreteEnv):
    """
    walls variable is an array of multiple wall objects
    wall format: [[position of wall], 0 for bottom or 1 for right]
    example: walls = [[[1,1],0],[[1,1],1]] # put a wall to the right and bottom
    of position [1,1]
    """

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, nrow=4, ncol=4, walls=[]):
        desc = np.full((2*nrow+1, 2*ncol+1), ' ')
        
        for i in range(nrow):
          desc[2*i+1][0] = '|'
          desc[2*i+1][-1] = '|'
        for j in range(ncol):
          desc[0][2*j+1] = '-'
          desc[-1][2*j+1] = '-'
        for i in range(nrow+1):
          for j in range(ncol+1):
            desc[2*i][2*j] = '+'
        for wall in walls:
          if wall[1] == 0:
            desc[2*wall[0][0]+2][2*wall[0][1]+1] = '-'
          else:
            desc[2*wall[0][0]+1][2*wall[0][1]+2] = '|'
            
            
        self.desc = desc = np.asarray(desc,dtype='c')
        self.nrow, self.ncol = nrow, ncol
        self.reward_range = (0, 1)

        nA = 4
        nS = nrow * ncol
                        
        isd = np.full(nS,0.)
        isd[0] = 1.

        P = {s : {a : [] for a in range(nA)} for s in range(nS)}

        def to_s(row, col):
            return row*ncol + col

        def inc(row, col, a):
            if a == LEFT:
              if desc[2*row+1][2*col] == b' ':
                col = col-1
            elif a == DOWN:
              if desc[2*row+2][2*col+1] == b' ':
                row = row+1
            elif a == RIGHT:
              if desc[2*row+1][2*col+2] == b' ':
                col = col+1
            elif a == UP:
              if desc[2*row][2*col+1] == b' ':
                row = row-1
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a]
                    done = row == nrow-1 and col == ncol-1
                    if done:
                        li.append((1.0, s, 0, True))
                    else:
                        newrow, newcol = inc(row, col, a)
                        newstate = to_s(newrow, newcol)
                        done = newrow == nrow-1 and newcol == ncol-1
                        rew = float(done)*2001 - float(row == newrow and col == newcol)*79 - 1.
                        li.append((1.0, newstate, rew, done))
                                                

        super(SimplegameEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
                
        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[2*row+1][2*col+1] = 'X'
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left","Down","Right","Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()