import logging
import sys

from architecture.noc import NoC
from engine.simulation import Simulation
from input.generation import Generation
from output.csv_writer import CSVWriter


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

    # Generation mode
    print('Please enter the messages generation mode')
    print('1 - UUniFast')
    print('2 - Manuel')
    generating = int(input('--> '))

    if generating == 1:
        messages = generation.uunifast_generate(30)
    elif generating == 2:
        messages = generation.scenario('input/scenario.yml')
    else:
        print('wrong parameters')
        sys.exit()

    # Simulator Settings
    simulation = Simulation(noc, generation.hyperperiod())

    for message in messages:
        simulation.send_message(message)

    # Starting Simulation
    logging.info('### Simulation --> START - hyperperiod : %d ###' % generation.hyperperiod())
    simulation.simulate()
    logging.info('### Simulation --> END ###')

    # printing
    messages_i = simulation.get_message_instance_tab()
    csv = CSVWriter(messages_i)
    csv.generate_csv('output/result.csv')


if __name__ == "__main__":
    main()
