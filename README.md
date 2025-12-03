🛰️ Live Network Monitor

A lightweight Python-based real-time network monitoring tool that tracks latency, packet loss, and bandwidth usage while displaying everything on a live updating graph. The system also provides instant alerts when any network metric crosses the defined threshold.

🚀 Features

📡 Live Latency Monitoring (via ping)

❌ Packet Loss Detection

📊 Real-time Bandwidth Usage (upload & download)

📈 Live Graph Visualization using Matplotlib

⚠️ Automatic Alerts for high latency or high bandwidth usage

⏱️ Runs in background using scheduler + threading

🖥️ Tech Stack

Python

psutil

ping3

schedule

matplotlib

📦 Installation
pip install psutil ping3 schedule matplotlib

▶️ How to Run
python network_monitor.py


The live graph will open and update automatically every 5 seconds.

⚙️ Configuration

You can modify thresholds inside the script:

LATENCY_THRESHOLD = 100      # ms
PACKET_LOSS_THRESHOLD = 0.1  # 10%
BANDWIDTH_THRESHOLD = 1e6    # bytes/sec

📌 Screenshot (Optional)

Add a screenshot of your graph here if you want.

📝 Description

A simple real-time system performance tool that logs network metrics, visualizes trends live, and alerts users to abnormal activity.

🧑‍💻 Author

Vivek Rao
https://github.com/vivekkrao07
