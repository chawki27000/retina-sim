import logging

# Simulation Setup
from communication.routing import Coordinate
from communication.structure import Message
from engine.simulation import Simulation

SIM_DURATION = 30


def main():
    # Log Configuration
    # logging.basicConfig(filename='sim.txt', level=logging.INFO)
    logging.basicConfig(level=logging.INFO)

    logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    # Simulator Settings
    simulation = Simulation(SIM_DURATION)

    src = Coordinate(1, 1)
    dest = Coordinate(2, 2)
    message = Message(1, 40, 128, src, dest)

    src2 = Coordinate(0, 2)
    dest2 = Coordinate(2, 2)
    message2 = Message(2, 40, 128, src2, dest2)

    # Simulation START
    simulation.send_message(message)
    simulation.send_message(message2)

    simulation.simulate()


if __name__ == "__main__":
    main()
