import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7629455103243709, 'demand': {1: 1.259, 2: 0.266, 3: 0.396, 4: 7.4, 5: 0.958, 6: 0.647, 7: 2.858, 8: 3.716, 9: 0.51, 10: 7.589}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.7629455103243709,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.762945510324371,complexity="high",params=params)
