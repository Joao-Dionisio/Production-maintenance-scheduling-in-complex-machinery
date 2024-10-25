import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.9560342718892494, 'demand': {1: 3.592, 2: 6.393, 3: 3.193, 4: 1.613, 5: 3.498, 6: 1.195, 7: 5.777, 8: 3.574, 9: 5.673, 10: 5.253}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.9560342718892494,complexity="low",params=params)

params[1] = get_random_machine(seed = 1.9560342718892494,complexity="low",params=params)
