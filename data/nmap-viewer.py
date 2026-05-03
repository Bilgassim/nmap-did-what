import sqlite3
import argparse
from datetime import datetime

def format_timestamp(ts_ms):
    if ts_ms is None: return "N/A"
    return datetime.fromtimestamp(ts_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

def view_results(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        print("\n=== NMAP SCANS SUMMARY ===")
        c.execute("SELECT id, nmap_version, start_time, total_hosts, total_open_ports FROM scans")
        scans = c.fetchall()
        for s in scans:
            print(f"ID: {s[0]} | Ver: {s[1]} | Date: {format_timestamp(s[2])} | Hosts: {s[3]} | Open Ports: {s[4]}")

        print("\n=== OPEN PORTS DETAIL ===")
        query = """
        SELECT h.ip, h.hostname, p.port, p.protocol, p.service_name, p.service_info
        FROM ports p
        JOIN hosts h ON p.host_id = h.id
        WHERE p.state = 'open'
        """
        c.execute(query)
        ports = c.fetchall()
        print(f"{'IP Address':<15} | {'Hostname':<20} | {'Port':<6} | {'Service':<12} | {'Version Info'}")
        print("-" * 80)
        for p in ports:
            print(f"{p[0]:<15} | {p[1]:<20} | {p[2]:<6} | {p[4]:<12} | {p[5]}")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error reading database: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="View nmap results from SQLite database.")
    parser.add_argument("--db", default='nmap_results.db', help="Path to the SQLite database file")
    args = parser.parse_args()
    view_results(args.db)
