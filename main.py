import logging
import sys
import getopt

from architecture.noc import NoC
from engine.simulation import Simulation
from gen.generation import Generation
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

    generation.set_noc(noc)

    # CLI Argument parsing
    level = 0
    messages = 0
    try:
        options, args = getopt.getopt(sys.argv[1:], 'dimu:')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print("""usage: %s [-d|-i] [-u|-m|-]
            -d, -i: DEBUG / INFO
            -u, -m : UUniFast val / Manual """ % sys.argv[0])
        sys.exit()

    for opt, value in options:
        if opt in '-d':
            level = logging.DEBUG
        if opt in '-i':
            level = logging.INFO
        if opt in '-m':
            messages = generation.scenario('input/scenario.yml')
        if opt in '-u':
            messages = generation.uunifast_generate(int(value))

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
