import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9501913698990805, 'demand': {1: 4.152, 2: 7.488, 3: 9.348, 4: 6.225, 5: 6.341, 6: 7.367, 7: 9.778, 8: 4.271, 9: 3.478, 10: 0.139, 11: 5.152, 12: 2.777, 13: 4.46, 14: 7.864, 15: 8.357, 16: 4.045, 17: 5.753, 18: 6.899, 19: 1.869, 20: 4.755}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.9501913698990805,complexity="low",params=params)
