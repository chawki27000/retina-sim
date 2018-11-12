import logging

# Simulation Setup
from communication.routing import Coordinate
from communication.structure import Message
from engine.global_obj import EVENT_LIST
from engine.simulation import Simulation

SIM_DURATION = 30


def main():
    # Log Configuration
    logging.basicConfig(level=logging.DEBUG)

    logging.info('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    # Simulator Settings
    simulation = Simulation()

    src = Coordinate(0, 0)
    dest = Coordinate(2, 2)
    message = Message(1, 40, 256, src, dest)

    # Simulation START
    simulation.send_message(message)
    simulation.simulate()


if __name__ == "__main__":
    main()
