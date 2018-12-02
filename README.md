# ReTiNAS
Real-Time Network-on-chip Analysis and Simulation

### Introduction
The purpose of ReTiNAS is to simulate real-time communicating tasks into On-chip Networks with a specific configuration.It's a discrete event-based simulation with cycle-accurate time handling.

## Installation
The following packages are required to execute the program :
- Python 3
- Pip (python package manager)
- PyYaml

To install the requirements, you must apply the following instructions (on Ubuntu) :
```
$ sudo apt-get install python-pip python-dev  
$ pip install -r requirement.txt
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

There is a choice in the way to write a scenario, either in a manuel or automatic way. The first is simply performed through editing **scenario.yml** file (included in the _input_ package).

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
To perform a simulator, it required to set the NoC architecture in **config.yml** (also included in _input_ package) as described in the bellow.
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

## Execution
To run the simulation, go to the project root and execute :
```
$ python main.py
```
After that, a CLI appears and ask 2 parameters : Task assigning mode (Manuel/UUniFast) and Simulation output mode, that's separated as follow :
- DEBUG : Print all NoC actions (PE sending, Router sending, VC allocation and releasing) and alternative cases (full buffer, no idle VC)
- INFO : Print only router-to-router sending and Flit arriving

## Example
The picture bellowed shows Flit sending and buffering into NoC under _wormhole-switching flow control. The simulator can reproduce the same schema.

![Alt Text](https://upload.wikimedia.org/wikipedia/en/a/ae/Wormhole-Three-Flows-Interfering.gif)

The following example is composed of 2 tasks that contain 2 communications :
- Task 1 : Router (1, 1) -> Router (2, 2)
- Task 2 : Router (0, 2) -> Router (2, 2)

Into NoC with : 4x4 2D-Mesh topology, 4 VC per InPort, 4 Flit buffer and unified Quantum = 1. We suppose the communication between PE and its router is instantaneous (No time taken into account). 


The following results are the INFO output
```
INFO:Router (1,1):Time : (0) - Flit(0-FlitType.head) from Packet(0) from Message(0) -> sent through VC (0)(West)  to Router (1,2)
INFO:Router (0,2):Time : (0) - Flit(0-FlitType.head) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (1,2)
INFO:Router (1,2):Time : (1) - Flit(0-FlitType.head) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (2,2)
INFO:Router (1,1):Time : (1) - Flit(1-FlitType.body) from Packet(0) from Message(0) -> sent through VC (0)(West)  to Router (1,2)
INFO:Router (0,2):Time : (1) - Flit(1-FlitType.body) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (1,2)
INFO:Router (2,2):Time : (2) - Flit(0-FlitType.head) from Packet(0) from Message(1) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (2) - Flit(1-FlitType.body) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (2,2)
INFO:Router (1,1):Time : (2) - Flit(2-FlitType.body) from Packet(0) from Message(0) -> sent through VC (0)(West)  to Router (1,2)
INFO:Router (0,2):Time : (2) - Flit(2-FlitType.body) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (1,2)
INFO:Router (2,2):Time : (3) - Flit(1-FlitType.body) from Packet(0) from Message(1) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (3) - Flit(0-FlitType.head) from Packet(0) from Message(0) -> sent through VC (1)(North)  to Router (2,2)
INFO:Router (1,1):Time : (3) - Flit(3-FlitType.tail) from Packet(0) from Message(0) -> sent through VC (0)(West)  to Router (1,2)
INFO:Router (0,2):Time : (3) - Flit(3-FlitType.tail) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (1,2)
INFO:Router (2,2):Time : (4) - Flit(0-FlitType.head) from Packet(0) from Message(0) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (4) - Flit(2-FlitType.body) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (2,2)
INFO:Router (2,2):Time : (5) - Flit(2-FlitType.body) from Packet(0) from Message(1) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (5) - Flit(1-FlitType.body) from Packet(0) from Message(0) -> sent through VC (1)(North)  to Router (2,2)
INFO:Router (2,2):Time : (6) - Flit(1-FlitType.body) from Packet(0) from Message(0) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (6) - Flit(3-FlitType.tail) from Packet(0) from Message(1) -> sent through VC (0)(North)  to Router (2,2)
INFO:Router (2,2):Time : (7) - Flit(3-FlitType.tail) from Packet(0) from Message(1) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (7) - Flit(2-FlitType.body) from Packet(0) from Message(0) -> sent through VC (1)(North)  to Router (2,2)
INFO:Router (2,2):Time : (8) - Flit(2-FlitType.body) from Packet(0) from Message(0) arrived to ProcessingEngine (2,2)
INFO:Router (1,2):Time : (8) - Flit(3-FlitType.tail) from Packet(0) from Message(0) -> sent through VC (1)(North)  to Router (2,2)
INFO:Router (2,2):Time : (9) - Flit(3-FlitType.tail) from Packet(0) from Message(0) arrived to ProcessingEngine (2,2)
```

A CSV file named **result.csv** (under _output_ package) contains the task instances latency (computed by the last packet arriving time minus the first packet sending time) and the analysis WCLA. the CSV file in structured as : 

| i | WCLA | L_1 | L_2 | L_3 | L_4 |
| --- | --- | --- | --- | --- | --- |
| task index  | analysis  | inst 1 latency | inst 2 latency | inst 3 latency | inst 4 latency |

## Authors

* **Chawki BENCHEHIDA** - [LAPECI Lab](http://lapeci.org/) - Université d'Oran 1
* **Mohammed Kamel BENHAOUA** - [LAPECI Lab](http://lapeci.org/) - Université d'Oran 1
* **Houssam Eddine ZAHAF** - [CRIStAL](https://www.cristal.univ-lille.fr) - Université de Lille
* **Giuseppe LIPARI** - [CRIStAL](https://www.cristal.univ-lille.fr) - Université de Lille

## Licence
[GPL](http://www.gnu.org/licenses/gpl-3.0.html)