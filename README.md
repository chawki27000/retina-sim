# ReTiNAS
Real-Time Network-on-chip Analysis and Simulation

### Introduction

ReTiNAS is a discrete event-based simulator with cycle-accurate time
handling. The purpose of ReTiNAS is to simulate real-time tasks
executing on Manycore on-chip Networks, and communicating with each
other.

## Installation
The following packages are required to execute the program :
- Python 3
- Pip (python package manager)
- PyYaml
- Simpy

To install the requirements, you must apply the following instructions (on Ubuntu) :
```
$ sudo apt-get install python-pip python-dev  
$ pip install -r requirement.txt
```

## Configuration
#### Simulator scenario

A scenario is needed to make a simulation. some parameters must be written to build a communicating task. These parameters are the same of for each task contained in the taskset, and they are enumerated as follows (in order) :
- Router source coordinate
- Router destination coordinate
- Message size
- Task offset
- Task deadline
- Task period

There is a choice in the way to write a scenario, either in a manual
or automatic way. The first is simply performed through editing the
**scenario.yml** file (included in the _input_ package).

Each YAML element describe a communication between two routers. An example of two tasks is given below.
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
    
    ...
    # Task n
```
	  
The second way is to generate a taskset by using
[UUniFast-Discard](https://pdfs.semanticscholar.org/24a9/c3297bf08caeceb15777e85f0c3da5c07e26.pdf)
Algorithm. The number of tasks must be given by the user in the
simulator CLI, like the following scenario file : 
```yaml
task: 7 # Task number 
method: 'UuniFast' # The unique method (until now)
load: 0.7 # Load rate (specified in UUnifast documentation)
```

#### Network-on-Chip settings

To perform a simulation, you must describe the NoC architecture in
**config.yml** (also included in _input_ package) as described in the
below.

```yaml
noc:
  dimension: 4 # NoC dimension : 4x4
  numberOfVC: 4 # Number of VC in each InPort
  VCBufferSize: 4 # the VC buffer size
  arbitration: 'RR' # Either in :: RR (TDMA) / PRIORITY_PREEMPT 

quantum: # VCs Quantum configuration (TDM Slot)
  1: 1
  2: 2
  3: 1
  4: 4
```

Other parameters are the packet and flit default size in
**structure.py**. They can be changed by modifying the two constants
_FLIT_DEFAULT_SIZE_ and _PACKET_DEFAULT_SIZE_.


## Execution

To run the simulation, go to the project root and execute :

```
$ python main.py [-i][-d]
```

The main program needs a parameter to lunch the simulation, as follows :  
- DEBUG (-d) : Print all NoC actions (PE sending, Router sending, VC allocation and releasing) and alternative cases (full buffer, no idle VC)
- INFO (-i) : Print only router-to-router sending and Flit arriving


## Example

The picture bellowed shows Flit sending and buffering into NoC under
_wormhole-switching_ flow control. The simulator can reproduce the
same schema.

![Alt Text](https://upload.wikimedia.org/wikipedia/en/a/ae/Wormhole-Three-Flows-Interfering.gif)

The following example is composed of 2 tasks that contain 2 communications :
- Task 1 : Router (1, 1) -> Router (2, 2)
- Task 2 : Router (0, 2) -> Router (2, 2)

Into NoC with : 4x4 2D-Mesh topology, 4 VC per InPort, 4 Flit buffer
and unified Quantum = 1. We suppose the communication between PE and
its router is instantaneous (No time taken into account).


The following results are the INFO output

```
INFO: :(0) : FlitType.head 0-0-1 - Router (0,2) -> VC (0)(North)  -> Router (1,2)
INFO: :(0) : FlitType.head 0-0-0 - Router (1,1) -> VC (0)(West)  -> Router (1,2)
INFO: :(1) : FlitType.body 1-0-0 - Router (1,1) -> VC (0)(West)  -> Router (1,2)
INFO: :(1) : FlitType.head 0-0-1 - Router (1,2) -> VC (0)(North)  -> Router (2,2)
INFO: :(1) : FlitType.body 1-0-1 - Router (0,2) -> VC (0)(North)  -> Router (1,2)
INFO: :(2) : FlitType.body 2-0-1 - Router (0,2) -> VC (0)(North)  -> Router (1,2)
INFO: :(2) : FlitType.body 1-0-1 - Router (1,2) -> VC (0)(North)  -> Router (2,2)
INFO: :(2) : FlitType.head 0-0-1 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(2) : FlitType.body 2-0-0 - Router (1,1) -> VC (0)(West)  -> Router (1,2)
INFO: :(3) : FlitType.tail 3-0-0 - Router (1,1) -> VC (0)(West)  -> Router (1,2)
INFO: :(3) : FlitType.head 0-0-0 - Router (1,2) -> VC (1)(North)  -> Router (2,2)
INFO: :(3) : FlitType.body 1-0-1 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(3) : FlitType.tail 3-0-1 - Router (0,2) -> VC (0)(North)  -> Router (1,2)
INFO: :(4) : FlitType.body 2-0-1 - Router (1,2) -> VC (0)(North)  -> Router (2,2)
INFO: :(4) : FlitType.head 0-0-0 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(5) : FlitType.body 1-0-0 - Router (1,2) -> VC (1)(North)  -> Router (2,2)
INFO: :(5) : FlitType.body 2-0-1 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(6) : FlitType.tail 3-0-1 - Router (1,2) -> VC (0)(North)  -> Router (2,2)
INFO: :(6) : FlitType.body 1-0-0 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(7) : FlitType.body 2-0-0 - Router (1,2) -> VC (1)(North)  -> Router (2,2)
INFO: :(7) : FlitType.tail 3-0-1 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(8) : FlitType.tail 3-0-0 - Router (1,2) -> VC (1)(North)  -> Router (2,2)
INFO: :(8) : FlitType.body 2-0-0 - Router (2,2) -> ProcessingEngine (2,2)
INFO: :(9) : FlitType.tail 3-0-0 - Router (2,2) -> ProcessingEngine (2,2)
```

The simulation generates Two result files structured like CSV format, named **result_analysis.csv** (contains the analysis part)  and **result_sim.csv**, where it contains the simulation results which express the task latency (computed by the last packet arriving time
minus the first packet sending time). In the result analysis file, the latency's computed by formulation detailed in the paper. 
The **result_analysis.csv** is structured like follows :

| i | L_1 | L_2 | L_3 | L_4 |
| --- | --- | --- | --- | --- |
| task index | inst 1 latency | inst 2 latency | inst 3 latency | inst 4 latency |

On the other hand, The **result_analysis.csv** is stuctured, like :

| i | WCLA |
| --- | --- |
| task index  | analysis latency |

Our work is based, on the generation of conflictual tasks through an algorithm detailed in the paper. The latter, takes the conflict rate interval, specified on _generation.py_ in _gen_ package through **scenario** function.
You can edit the conflict rate by modifying the followings function:
```python
# The first paramters is our communication task
# The two following parameters specify the interval (upper, lower) ([50%, 60%])
# The last, is the rate error (+/-)  
self.conflict_task_by_axe(message, 60, 50, 0) 
```

## Authors

* **Chawki BENCHEHIDA** - [LAPECI Lab](http://lapeci.org/) - Université d'Oran 1
* **Mohammed Kamel BENHAOUA** - [LAPECI Lab](http://lapeci.org/) - Université d'Oran 1
* **Houssam Eddine ZAHAF** - [CRIStAL](https://www.cristal.univ-lille.fr) - Université de Lille
* **Giuseppe LIPARI** - [CRIStAL](https://www.cristal.univ-lille.fr) - Université de Lille

## Licence
[GPL](http://www.gnu.org/licenses/gpl-3.0.html)
