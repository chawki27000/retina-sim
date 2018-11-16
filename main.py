import logging

# Simulation Setup
from architecture.noc import NoC
from communication.routing import Coordinate
from communication.structure import Message
from engine.simulation import Simulation
from input.generation import Generation

SIM_DURATION = 30


def main():
    # NoC Settings
    generation = Generation()
    generation.parse('input/config.yml')

    square_size = generation.square_size()
    nbvc = generation.nbvc()
    vc_size = generation.vc_size()
    vc_quantum = generation.vc_quantum()

    noc = NoC('Network-On-Chip', square_size, nbvc, vc_size, vc_quantum)

    # Log Configuration
    # logging.basicConfig(filename='output/log.txt', level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    # Simulator Settings
    simulation = Simulation(noc, SIM_DURATION)

    src = Coordinate(1, 1)
    dest = Coordinate(2, 2)
    message = Message(1, 40, 128, src, dest)

    src2 = Coordinate(0, 2)
    dest2 = Coordinate(2, 2)
    message2 = Message(2, 60, 128, src2, dest2)

    # Simulation START
    simulation.send_message(message)
    simulation.send_message(message2)

    simulation.simulate()


if __name__ == "__main__":
    main()
