import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.8389025795813567, 'demand': {1: 1.838, 2: 6.009, 3: 9.939, 4: 0.893, 5: 8.767, 6: 8.117, 7: 8.271, 8: 4.672, 9: 3.837, 10: 4.291, 11: 2.098, 12: 3.237, 13: 5.557, 14: 3.208, 15: 0.94, 16: 5.605, 17: 9.89, 18: 6.249, 19: 9.935, 20: 3.081}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.8389025795813567,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.8389025795813567,complexity="high",params=params)
