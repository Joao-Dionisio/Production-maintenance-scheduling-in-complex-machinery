import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.13291567842612995, 'demand': {1: 8.353, 2: 7.113, 3: 1.554, 4: 2.418, 5: 5.963, 6: 1.745, 7: 9.647, 8: 1.133, 9: 3.095, 10: 6.856}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.13291567842612995,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.13291567842613,complexity="low",params=params)
