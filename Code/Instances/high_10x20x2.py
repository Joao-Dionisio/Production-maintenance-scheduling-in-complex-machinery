import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7848223833146682, 'demand': {1: 7.921, 2: 4.993, 3: 8.505, 4: 7.848, 5: 7.04, 6: 4.826, 7: 7.524, 8: 2.451, 9: 7.054, 10: 6.889}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.7848223833146682,complexity="high",params=params)
