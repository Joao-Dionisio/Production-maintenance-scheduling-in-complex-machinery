import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'time_limit': 7200, 'global_seed': 0.32383276483316237, 'demand': {1: 4.844, 2: 7.307, 3: 8.048, 4: 2.871, 5: 6.472, 6: 4.249, 7: 4.944, 8: 0.257, 9: 9.019, 10: 7.851, 11: 4.455, 12: 2.955, 13: 3.15, 14: 3.396, 15: 4.829, 16: 3.616, 17: 4.57, 18: 9.56, 19: 5.623, 20: 8.903}, 'machines_per_group': [20], 'n_groups': 1, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

params[0] = get_random_machine(seed = 0.32383276483316237,complexity="high",params=params)
