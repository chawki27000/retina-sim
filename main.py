from architecture.noc import NoC

if __name__ == "__main__":
    print('### ReTiNAS - Real-Time Network-on-chip Analysis and Simulation ###')

    noc = NoC('Network-On-Chip', 4)
    print(noc)
