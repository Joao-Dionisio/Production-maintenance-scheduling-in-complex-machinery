# Branch and price for nonlinear production-maintenance scheduling in complex machinery

This repository contains the implementation of the *Branch and price for nonlinear production-maintenance scheduling in complex machinery* paper.
The problem concerns deciding how much each machine should produce, so that demand is satisfied, given that more production incurs more degradation. This will require costly maintenance, and the problem's objective is the minimization of the maintenance cost.

The paper is saved in [Manuscript.pdf](https://github.com/Joao-Dionisio/Production-maintenance-scheduling-in-complex-machinery/blob/master/Manuscript.pdf).

<p align=center>
<img width="864" height="365" alt="image" src="https://github.com/user-attachments/assets/ee35ebca-1216-4db7-972c-2c062c8ca0d6" />
  
  <p align=center>
    Fig. 1: Visualization of the production-maintenance scheduling problem. Bad decisions early lead to infeasibility in later periods.
  </p>
</p>

It should be adaptable to other Branch-and-Price applications without much effort.

Note: This repository is still in the process of being cleaned up. Some files may contain code or comments that are not relevant to this specific project. Namely, mentions of alternative master problems and different formulations. Make sure that when running, either use `model=0` or `model=1` for the extended or the compact formulations, respectively.

---

## **Contents**

The code 

### **1. Key Files**
- **`sequential_pricer.py`**: Implements the column generation code mentioned in the paper, along with the acceleration techniques.
- **`pricing_branching.py`**: Contains branching rules and event handlers for managing branching decisions in the master problem, as well as the repairing of fractional solutions. The default branching rule is branching on original variable bounds, with a repair step for the mixed-integer case.
- **`testing.py`**: Provides tools for testing feasibility, generating random instances, and running experiments.
- **`create_model.py`**: Constructs the compact formulation and the pricing problems.
- **`parameters.py`**: Defines the parameters and components used in the models.


<p align=center>
<img width="733" height="564" alt="image" src="https://github.com/user-attachments/assets/122796fe-754b-4e78-a063-fa9031947986" />

  <p align=center>
    Fig. 2: Visualization of branching on original variable bounds.
  </p>
</p>

---

### **2. Installation**

#### **Dependencies**
- Python 3.9+
- Required Python libraries:
  ```bash
  pip install pyscipopt numpy matplotlib
  ```

Optional: networkx for a simple tree visualization.
Note: At the time of submission, it's possible that the PySCIPOpt version on PyPI is not recent enough to run the code. In that case, please install it from source as per the instructions on the [PySCIPOpt GitHub page](https://github.com/scipopt/PySCIPOpt).

### **3. Usage**

_Run an Instance_
To run a specific instance:

Modify the kwargs dictionary at the end of `testing.py` to configure the instance parameters.

_Run experiments_
Run `run_instance_set()` in `testing.py` to execute a given set of instances with the specified parameters.

### **4. Example Workflow**
- Generate Instances: Use `create_instance_set()` in `testing.py` to create problem instances.
- Run code: Execute `run_instance()` with the desired parameters.
- Get statistics: Call `generate_stats_report()` to obtain a report on the generated instances.

### **5. Contributing**
Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a feature branch.
- Submit a pull request with a detailed description.

### **6. License**
This project is licensed under the MIT License. See the LICENSE file for details.

### **7. Contact**
For questions or feedback, feel free to open an issue or contact me directly!
