import getopt
import logging
import os
import sys

import simpy

from architecture.noc import NoC
from gen.generation import Generation


def main():
    # Create the SimPy environment. This is the thing that runs the simulation.
    env = simpy.Environment()

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
        # NoC Settings
        generation = Generation()
        generation.config('input/' + file + '/config.yml')

        square_size = generation.square_size()
        nbvc = generation.nbvc()
        vc_size = generation.vc_size()
        vc_quantum = generation.vc_quantum()
        arbitration = generation.arbitration()

        noc = NoC(env, 'Network-On-Chip', square_size, nbvc, vc_size, vc_quantum)

        generation.set_noc(noc)

        # Messages generation
        messages = generation.scenario('input/' + file + '/scenario.yml')
        print("Taskset : %d" % len(messages))
        print("HP : %d" % generation.hyperperiod())
        # set logging level + log file
        logging.basicConfig(level=level,
                            handlers=[
                                # logging.FileHandler('input/' + file + '/output.log'),
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
        # csv = CSVWriter(messages, arbitration, noc)
        # csv.analysis_trace_csv('input/' + file + '/result_analysis.csv', messages)
        """
        Analysis : End
        """

        """
        Simulation : Begin
        """
        # Simulator Settings
        noc.messages = messages

        # Starting Simulation
        logging.info('### Simulation --> START - hyperperiod : %d ###' % generation.hyperperiod())
        env.run(until=100)
        logging.info('### Simulation --> END ###')

        # printing
        # messages_i = simulation.get_message_instance_tab()
        # csv = CSVWriter(messages_i, 0)

        #
        # """
        # Simulation : End
        # """
        #
        # # Trace generation : Latency
        # for message in simulation.get_message_instance_tab():
        #     print("%s --> latency : %d" % (message, message.get_latency()))
        #
        # csv.simulation_trace_csv('input/' + file + '/result_sim.csv')


if __name__ == "__main__":
    main()
