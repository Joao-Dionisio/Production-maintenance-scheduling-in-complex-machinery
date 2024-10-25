import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7425956013079879, 'demand': {1: 2.637, 2: 9.767, 3: 9.531, 4: 6.878, 5: 5.773, 6: 1.403, 7: 2.322, 8: 6.898, 9: 7.229, 10: 9.134}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.7425956013079879,complexity="high",params=params)
