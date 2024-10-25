import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9337824900741977, 'demand': {1: 9.238, 2: 1.121, 3: 8.799, 4: 5.953, 5: 1.398, 6: 4.514, 7: 8.995, 8: 1.611, 9: 0.483, 10: 0.74, 11: 9.915, 12: 7.238, 13: 9.637, 14: 2.553, 15: 4.923, 16: 5.8, 17: 1.696, 18: 7.444, 19: 6.911, 20: 4.186}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.9337824900741977,complexity="high",params=params)
