import logging
import sys

from architecture.noc import NoC
from engine.simulation import Simulation
from input.generation import Generation

SIM_DURATION = 30


def main():
    # NoC Settings
    generation = Generation()
    generation.config('input/config.yml')

    square_size = generation.square_size()
    nbvc = generation.nbvc()
    vc_size = generation.vc_size()
    vc_quantum = generation.vc_quantum()

    noc = NoC('Network-On-Chip', square_size, nbvc, vc_size, vc_quantum)

    # Log Configuration
    print('Please enter the simulation monitoring mode')
    print('1 - DEBUG')
    print('2 - INFO')
    mode = int(input('--> '))

    if mode == 1:
        level = logging.DEBUG
    elif mode == 2:
        level = logging.INFO
    else:
        print('wrong parameters')
        sys.exit()

    logging.basicConfig(level=level)

    logging.info('###################################################################')
    logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')
    logging.info('------ NoC Configuration ------')
    logging.info('\tDimension : %d x %d' % (square_size, square_size))
    logging.info('\tVC Number per Input : %d' % nbvc)
    logging.info('\tVC Buffer size : %d' % vc_size)
    logging.info('\tVC Quantum setting : %s' % vc_quantum)
    logging.info('-------------------------------')

    # Simulator Settings
    simulation = Simulation(noc, SIM_DURATION)

    # Messages
    messages = generation.scenario('input/scenario.yml')
    for message in messages:
        simulation.send_message(message)

    # Starting Simulation
    logging.info('### Simulation --> START ###')
    simulation.simulate()
    logging.info('### Simulation --> END ###')


if __name__ == "__main__":
    main()
