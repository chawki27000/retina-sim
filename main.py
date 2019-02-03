import logging
import sys
import getopt
import os

from architecture.noc import NoC
from engine.simulation import Simulation
from gen.generation import Generation
from gen.csv_writer import CSVWriter


def main():
    # parse input files
    input_files = os.popen("ls input").read().split('\n')
    del input_files[-1]

    # CLI Argument parsing
    level = 0
    try:
        options, args = getopt.getopt(sys.argv[1:], 'dimu:')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print("""usage: %s [-d|-i] [-u|-m|-]
                -d, -i: DEBUG / INFO """ % sys.argv[0])
        sys.exit()

    for opt, value in options:
        if opt in '-d':
            level = logging.DEBUG
        if opt in '-i':
            level = logging.INFO

    # file parsing loop
    for file in input_files:
        Simulation.CLOCK = 0

        # NoC Settings
        generation = Generation()
        generation.config('input/' + file + '/config.yml')

        square_size = generation.square_size()
        nbvc = generation.nbvc()
        vc_size = generation.vc_size()
        vc_quantum = generation.vc_quantum()
        arbitration = generation.arbitration()

        noc = NoC('Network-On-Chip', square_size, nbvc, vc_size, vc_quantum)

        generation.set_noc(noc)

        # Messages generation
        messages = generation.scenario('input/' + file + '/scenario.yml')

        # set logging level + log file
        logging.basicConfig(level=level,
                            handlers=[
                                logging.FileHandler('input/output.log'),
                                logging.StreamHandler()
                            ])

        logging.info('###################################################################')
        logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')
        logging.info('------ NoC Configuration ------')
        logging.info('\tDimension : %d x %d' % (square_size, square_size))
        logging.info('\tVC Number per Input : %d' % nbvc)
        logging.info('\tVC Buffer size : %d' % vc_size)
        logging.info('\tVC Quantum setting : %s' % vc_quantum)
        logging.info('\tArbitration Policy : %s' % arbitration)
        logging.info('-------------------------------')

        """
        Analysis : Begin
        """
        csv = CSVWriter(messages, 1)
        csv.generate_csv('input/' + file + '/result_analysis.csv',
                         arbitration=arbitration,
                         generation=generation)
        """
        Analysis : End
        """

        """
        Simulation : Begin
        """
        # Simulator Settings
        simulation = Simulation(noc, generation.hyperperiod())

        for message in messages:
            simulation.send_message(message)

        # Starting Simulation
        logging.info('### Simulation --> START - hyperperiod : %d ###' % generation.hyperperiod())
        simulation.simulate(arbitration)
        logging.info('### Simulation --> END ###')

        # printing
        messages_i = simulation.get_message_instance_tab()
        csv = CSVWriter(messages_i, 0)
        csv.generate_csv('input/' + file + '/result_sim.csv')

        simulation.reset_clock()

        """
        Simulation : End
        """


if __name__ == "__main__":
    main()
