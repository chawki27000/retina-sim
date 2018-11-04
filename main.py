from architecture.noc import NoC
import simpy

# Simulation Setup
SIM_DURATION = 100

if __name__ == "__main__":
    print('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    # Simulation Environment Initialization
    env = simpy.Environment()

    # NoC Initialization
    noc = NoC(env, 'Network-On-Chip', 4)
    noc.process()

    # Simulation START
    env.run(until=SIM_DURATION)
