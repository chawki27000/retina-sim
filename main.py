import simpy
import logging

from architecture.noc import NoC

# Simulation Setup
SIM_DURATION = 30


def main():
    # Log Configuration
    logging.basicConfig(level=logging.DEBUG)

    logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    # Simulation Environment Initialization
    env = simpy.Environment()

    # NoC Initialization
    noc = NoC(env, 'Network-On-Chip', 4, 6, 12)
    noc.process()

    # Simulation START
    env.run(until=SIM_DURATION)


if __name__ == "__main__":
    main()
