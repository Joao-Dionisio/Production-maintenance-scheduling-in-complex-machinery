import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from testing import get_random_machine


params = {'eps': 1e-09, 'decimal_places': 9, 'linear_relaxation': False, 'T_prime': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'time_limit': 7200, 'global_seed': 0.7590351673877891, 'demand': {1: 2.476, 2: 9.359, 3: 3.076, 4: 8.42, 5: 4.736, 6: 3.906, 7: 8.594, 8: 5.803, 9: 8.879, 10: 0.007}, 'machines_per_group': [10, 10], 'n_groups': 2, 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 'T': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

params[0] = get_random_machine(seed = 0.7590351673877891,complexity="high",params=params)

params[1] = get_random_machine(seed = 1.759035167387789,complexity="high",params=params)
