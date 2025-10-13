import numpy as np 
import matplotlib.pyplot as plt
import csv

distances = [2,5,10,15]
num_runs = 5
tcp_throughput = []
udp_throughput = []
tcp_runs = np.full((len(distances), num_runs), np.nan, dtype=float)
udp_runs= np.full((len(distances), num_runs), np.nan, dtype=float)

def get_cell(filepath, target_row, target_col):
    try:
        with open(filepath,'r', newline = '') as file:
            reader = csv.reader(file)
            for current_row, row in enumerate(reader):
                if current_row == target_row:
                    if target_col < len(row):
                        return row[target_col]
                    else:
                        # print("error, col index out of range")
                        return None
    except FileNotFoundError:
        print(f"Error: file not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

for index, i in enumerate(distances):
    tcp_file_name = f"iperf_tcp_{i}m.csv"
    udp_file_name = f"iperf_udp_{i}m.csv"
    tcp_val = get_cell(tcp_file_name,1,6)
    tcp_throughput.append(tcp_val)
    udp_throughput.append(get_cell(udp_file_name,1,6))
    for r in range(num_runs):
    
        #store row 1 columns 1 through 5 of tcp in respective row in 2d array tcp_throughput_all
        tcp_runs[index, r] = get_cell(tcp_file_name, 1, 1 + r)
        udp_runs[index, r] = get_cell(udp_file_name, 1, 1 + r)


tcp = np.array(tcp_throughput, dtype=float)
udp = np.array(udp_throughput, dtype=float)
plt.figure(figsize=(8, 5))
plt.plot(distances, tcp, 'o-', label='TCP Throughput (Mbps)')
plt.plot(distances, udp, 's-', label='UDP Throughput (Mbps)')

plt.xlabel('Distance (m)')
plt.ylabel('Throughput (Mbps)')
plt.title('Throughput vs Distance')
plt.legend()
plt.grid(True)

plt.xlim(0, 16)
plt.savefig("throughput_vs_distance.png", dpi=300, bbox_inches='tight')
plt.show()

tcp_runs_float = np.array(tcp_runs, dtype = float)
udp_runs_float = np.array(udp_runs, dtype = float)
runs = [1,2,3,4,5]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))


axes[0,0].plot(runs, tcp_runs_float[0], 'o-', label = "TCP Throughput")
axes[0,0].plot(runs, udp_runs_float[0], 's-', label = "UDP Throughput")
axes[0,0].set_title('2m Runs')
axes[0,0].legend()
axes[0,0].grid(True)

axes[0,1].plot(runs, tcp_runs_float[1], 'o-', label = "TCP Throughput")
axes[0,1].plot(runs, udp_runs_float[1], 's-', label = "UDP Throughput")
axes[0,1].set_title('5m Runs')
axes[0,1].legend()
axes[0,1].grid(True)

axes[1,0].plot(runs, tcp_runs_float[2], 'o-', label = "TCP Throughput")
axes[1,0].plot(runs, udp_runs_float[2], 's-', label = "UDP Throughput")
axes[1,0].set_title('10m Runs')
axes[1,0].legend()
axes[1,0].grid(True)

axes[1,1].plot(runs, tcp_runs_float[3], 'o-', label = "TCP Throughput")
axes[1,1].plot(runs, udp_runs_float[3], 's-', label = "UDP Throughput")
axes[1,1].set_title('15m Runs')
axes[1,1].legend()
axes[1,1].grid(True)
plt.savefig("runs.png", dpi=300, bbox_inches='tight')
plt.show()



