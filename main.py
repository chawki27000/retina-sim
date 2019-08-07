import getopt
import logging
import os
import sys
import time

import simpy

from architecture.noc import NoC
from gen.csv_writer import CSVWriter
from gen.generation import Generation


def main1():
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
        csv = CSVWriter(messages, arbitration, noc)
        csv.analysis_trace_csv('input/' + file + '/result_analysis.csv', messages)
        """
        Analysis : End
        """

        """
        Simulation : Begin
        """
        # Simulator Settings
        noc.messages = messages
        noc.arbitration = arbitration

        for msg in messages:
            print(msg)
        # Starting Simulation
        logging.info('### Simulation --> START - hyperperiod : %d ###' % generation.hyperperiod())
        env.run(until=generation.hyperperiod())
        # env.run(until=20)
        logging.info('### Simulation --> END ###')

        # printing
        messages_i = noc.messages_instance
        csv = CSVWriter(messages_i, 0, noc)

        """
        Simulation : End
        """

        # Trace generation : Latency
        # for msgi in messages_i:
        #     print("%s ---> Sched :: %s" % (msgi, msgi.is_deadline_met()))

        csv.simulation_trace_csv('input/' + file + '/result_sim.csv')


def main_resource_augmentation():
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
        nbvc = generation.nbvc() - 1
        vc_size = generation.vc_size()
        vc_quantum = generation.vc_quantum()
        arbitration = generation.arbitration()

        # Messages generation
        # messages = generation.scenario('input/' + file + '/scenario.yml')
        # print("Taskset : %d" % len(messages))
        # print("HP : %d" % generation.hyperperiod())
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

        # Starting Simulation
        tab = []
        for count in range(5):
            messages = None
            nbvc = generation.nbvc() - 1
            vc_quantum = generation.vc_quantum()
            vc_quantum.pop()
            while True:
                # Create the SimPy environment. This is the thing that runs the simulation.
                env = simpy.Environment()

                nbvc += 1
                vc_quantum.append(1)
                noc = NoC(env, 'Network-On-Chip', square_size, nbvc, vc_size, vc_quantum)
                generation.set_noc(noc)

                # Messages generation
                if messages is None:
                    print("GENERATION ----------------------------------")
                    messages = generation.scenario('input/' + file + '/scenario.yml')
                # Simulator Settings
                noc.messages = messages

                ##################  1 - RR  ##################
                noc.arbitration = arbitration

                logging.info('### Simulation --> START - hyperperiod : %d ###' % generation.hyperperiod())
                env.run(until=generation.hyperperiod())
                # env.run(until=20)
                logging.info('### Simulation --> END ###')

                # printing
                messages_i = noc.messages_instance
                csv = CSVWriter(messages_i, 0, noc)

                """
                Simulation : End
                """
                if is_taskset_deadline_meeting(messages_i):
                    print(">>>>>>>>>>>>>>>>> FINAL :: NUMBER OF VCS : %d" % len(noc.router_matrix[0][0].inNorth.vcs))
                    tab.append(len(noc.router_matrix[0][0].inNorth.vcs))
                    break
                else:
                    # TODO : RA
                    print(">>>>>>>>>>>>>>>>> NUMBER OF VCS : %d" % len(noc.router_matrix[0][0].inNorth.vcs))
                    continue

        CSVWriter.resource_augmentation_trace_csv('input/' + file + '/resource_augmentation.csv', tab)


def is_taskset_deadline_meeting(messages):
    for msg in messages:
        # if msg.is_deadline_met() is None:
        #     continue
        if not msg.is_deadline_met():
            print("%s ---> Sched :: %s" % (msg, msg.is_deadline_met()))
            return False
    return True


if __name__ == "__main__":
    main1()
