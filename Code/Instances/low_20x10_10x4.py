import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.39903888948321997, 'demand': {1: 5.206, 2: 3.262, 3: 3.547, 4: 3.265, 5: 7.915, 6: 4.559, 7: 6.429, 8: 9.04, 9: 6.573, 10: 2.496, 11: 7.094, 12: 7.124, 13: 4.75, 14: 3.132, 15: 7.861, 16: 8.452, 17: 2.812, 18: 7.725, 19: 0.892, 20: 5.017}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.39903888948321997,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.39903888948322,complexity="low",params=params)
