import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.8021704088294962, 'demand': {1: 5.102, 2: 9.652, 3: 0.524, 4: 7.063, 5: 5.624, 6: 9.553, 7: 9.126, 8: 2.808, 9: 3.849, 10: 7.983}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.8021704088294962,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.8021704088294963,complexity="high",params=params)
