# ReTiNAS
Real-Time Network-on-chip Analysis and Simulation

## Installation
The following packages are required to execute the program :
- Python 3
- Pip (python package manager)
- PyYaml

To install the requirements, you must apply the following instructions (on Ubuntu) :
```
sudo apt-get install python-pip python-dev  
pip install -r requirement.txt
```

## Configuration
#### Simulator scenario
To execute the simulator, it needs a scenario. The latter is a Task Set of several routers communication that's contain :
- Router source coordinate 
- Router destination coordinate
- Message size
- Task offset
- Task deadline
- Task period

There is a choice in the way to write a scenario, either in a manuel or automatic way. The first is simply performed through editing **scenario.yml** file (included in the input package).

Each YAML element describe a communication between two routers. An example of two tasks is given in bellow.
```yaml
scenario:
    # Task 1
    - src: # source router
          i: 1 # row
          j: 1 # column
      dest: # destination router
          i: 2
          j: 2
      size: 128 # message size
      offset: 0 # task offset 
      deadline: 20 # task deadline
      period: 40 # task period
      
    # Task 2
    - src: 
          i: 0
          j: 2
      dest:
          i: 2
          j: 2
      size: 128
      offset: 30
      deadline: 60
      period: 100
```
The second way is to generate tasks by using [UUniFast-Discard](https://pdfs.semanticscholar.org/24a9/c3297bf08caeceb15777e85f0c3da5c07e26.pdf) Algorithm. The number of tasks must be given by the user in the simulator CLI.

#### Network-on-Chip settings
To perform a simulator, it required to set the NoC architecture in **config.yml** (also included in input package) as described in the bellow.
```yaml
noc:
  dimension: 4 # NoC dimension : 4x4
  numberOfVC: 4 # Number of VC in each InPort
  VCBufferSize: 4 # the VC buffer size

quantum: # VCs Quantum configuration (according to numberOfVC)
  1: 1
  2: 2
  3: 1
  4: 4
```