import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.47790834219506517, 'demand': {1: 5.464, 2: 6.424, 3: 4.697, 4: 0.398, 5: 7.327, 6: 4.807, 7: 1.874, 8: 6.744, 9: 2.857, 10: 1.101, 11: 9.622, 12: 1.974, 13: 3.78, 14: 9.192, 15: 6.979, 16: 2.694, 17: 2.275, 18: 3.619, 19: 2.484, 20: 7.873}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.47790834219506517,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.4779083421950652,complexity="high",params=params)
