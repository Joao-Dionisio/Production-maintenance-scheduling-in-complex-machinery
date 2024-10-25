import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.05190743589748703, 'demand': {1: 1.359, 2: 9.499, 3: 0.776, 4: 9.683, 5: 7.523, 6: 9.867, 7: 9.307, 8: 3.801, 9: 5.36, 10: 5.777}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.05190743589748703,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.051907435897487,complexity="low",params=params)
