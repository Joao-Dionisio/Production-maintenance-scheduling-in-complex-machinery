import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.9372383891087552, 'demand': {1: 8.39, 2: 2.152, 3: 5.631, 4: 9.24, 5: 0.743, 6: 1.643, 7: 6.216, 8: 6.407, 9: 8.686, 10: 3.068, 11: 1.074, 12: 6.795, 13: 2.7, 14: 4.459, 15: 6.057, 16: 7.161, 17: 7.513, 18: 8.788, 19: 2.796, 20: 0.904}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.9372383891087552,complexity="high",params=params)
