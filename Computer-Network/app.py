import psutil
from ping3 import ping
import time
import schedule
import matplotlib.pyplot as plt
from datetime import datetime
from threading import Thread

# ---------------- CONFIG ----------------
LATENCY_THRESHOLD = 100      # ms
PACKET_LOSS_THRESHOLD = 0.1  # 10%
BANDWIDTH_THRESHOLD = 1e6    # bytes
MAX_POINTS = 50              # max points shown on graph

# Data storage
network_data = {
    "time": [],
    "latency": [],
    "packet_loss": [],
    "bandwidth_sent": [],
    "bandwidth_received": []
}

prev_io = psutil.net_io_counters()
prev_time = time.time()
running = True

# ---------------- MONITORING ----------------
def monitor_latency(host="8.8.8.8"):
    """Ping the host and measure latency."""
    try:
        latency = ping(host, timeout=2)
        if latency is None:
            print(f"[ALERT] Host {host} unreachable!")
            packet_loss = 100
            latency_ms = 0
        else:
            latency_ms = latency * 1000
            packet_loss = 0
            if latency_ms > LATENCY_THRESHOLD:
                print(f"[ALERT] High latency: {latency_ms:.2f} ms")

        network_data["latency"].append(latency_ms)
        network_data["packet_loss"].append(packet_loss)
    except Exception as e:
        print(f"[ERROR] Ping failed: {e}")
        network_data["packet_loss"].append(100)
        network_data["latency"].append(0)

def monitor_bandwidth():
    """Calculate bandwidth since last check."""
    global prev_io, prev_time
    current_io = psutil.net_io_counters()
    current_time = time.time()
    interval = current_time - prev_time

    sent_bps = (current_io.bytes_sent - prev_io.bytes_sent) / interval
    recv_bps = (current_io.bytes_recv - prev_io.bytes_recv) / interval

    if sent_bps > BANDWIDTH_THRESHOLD:
        print(f"[ALERT] High upload speed: {sent_bps/1e6:.2f} MB/s")
    if recv_bps > BANDWIDTH_THRESHOLD:
        print(f"[ALERT] High download speed: {recv_bps/1e6:.2f} MB/s")

    prev_io = current_io
    prev_time = current_time

    network_data["bandwidth_sent"].append(sent_bps)
    network_data["bandwidth_received"].append(recv_bps)

    print(f"Upload: {sent_bps/1e6:.2f} MB/s | Download: {recv_bps/1e6:.2f} MB/s")

def monitor_network():
    """Run latency and bandwidth checks."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    network_data["time"].append(timestamp)

    print(f"\n--- Network Check @ {timestamp} ---")
    monitor_latency()
    monitor_bandwidth()

    # Keep only recent data
    for key in network_data:
        network_data[key] = network_data[key][-MAX_POINTS:]

# ---------------- PLOTTING ----------------
plt.ion()  # Interactive mode ON
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle("Live Network Monitor")

latency_line, = axs[0].plot([], [], label="Latency (ms)", color="orange")
packet_line, = axs[1].plot([], [], label="Packet Loss (%)", color="red")
upload_line, = axs[2].plot([], [], label="Upload (MB/s)", color="blue")
download_line, = axs[2].plot([], [], label="Download (MB/s)", color="green")

for ax in axs:
    ax.legend()
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)

axs[0].set_ylabel("Latency (ms)")
axs[1].set_ylabel("Packet Loss (%)")
axs[2].set_ylabel("Speed (MB/s)")

def update_plot():
    """Force refresh of the live graph."""
    if not network_data["time"]:
        return

    x = range(len(network_data["time"]))  # use numeric X for better performance

    latency_line.set_data(x, network_data["latency"])
    packet_line.set_data(x, network_data["packet_loss"])
    upload_line.set_data(x, [s/1e6 for s in network_data["bandwidth_sent"]])
    download_line.set_data(x, [r/1e6 for r in network_data["bandwidth_received"]])

    for ax in axs:
        ax.relim()
        ax.autoscale_view()

    # Redraw immediately
    fig.canvas.draw()
    fig.canvas.flush_events()

# ---------------- SCHEDULER ----------------
def run_scheduler():
    schedule.every(2).seconds.do(lambda: (monitor_network(), update_plot()))
    while running:
        schedule.run_pending()
        time.sleep(0.1)

# Start scheduler in background
thread = Thread(target=run_scheduler, daemon=True)
thread.start()

print("✅ Live network monitor started — close the graph window to stop.")
plt.show(block=True)
running = False