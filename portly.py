#!/usr/bin/python3
# Portly
# A python port scanner.
# Eric Hedstrom

# We need sys to pass cli arguments to the port scanner.
try:
    import sys
except ImportError as error:
    print(error)

# The real meat of this operation.
try:
    import socket
except ImportError as error:
    print(error)

# Local variables
wait = float(0.5)    # Seconds to wait for a response.
low_port = 1         # Low port range.
high_port = 65535    # High port range.
multi_port = False   # Toggle between single and multiple ports.

# Exit if port and IP are not passed via arg
if not len(sys.argv) == 3:
    print(f"Usage: portly.py [PORT] [IP]")
    sys.exit()

# Use port passed via argument.
if sys.argv[1].count("-") > 0:
    # Possibly two ports were passed.
    multi_port = True

    # Split the two numbers into low and high.
    low_port = int(sys.argv[1].split("-")[0])
    high_port = int(sys.argv[1].split("-")[1])

    # Verify low value is a viable port.
    if not 1 <= low_port <= 65535:
        print(f"{low_port} is not between 1 and 65535.")
        sys.exit()

    # Verify the high value is a viable port.
    if not 1 <= high_port <= 65535:
        print(f"{high_port} is not between 1 and 65535.")
        sys.exit()
    # Calculate how many ports we're going to scan.
    possible_ports = high_port - low_port + 1


else:
    # Single port passed.
    multi_port = False

    # Get port number.
    port = int(sys.argv[1])

    # Verify as a viable port.
    if not 1 <= port <= 65535:
        print(f"{port} is not between 1 and 65535.")
        sys.exit()

    possible_ports = 1

# Estimate minimum running time to complete the scan.
min_run_time = round(possible_ports * wait, 2)

# Verify an IP was passed.
if len(sys.argv[2]) > 1:
    ip = str(sys.argv[2])
else:
    print("Google selected because a viable IP was not passed via argument.")
    ip = "8.8.8.8"

# Total Ports Scanned
scan_total = 0


def scan_ports(ip, low_port, high_port, wait):

    scan_total = 0

    print(f"Scan started - scanning ports {low_port}-{high_port}")

    for port in range(low_port, high_port + 1):
        protocol = "TCP"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(wait)
        result = s.connect_ex((ip, port))

        if result == 0:
            status = "OPEN"
            print(f"Port:{protocol} {port}-{status}")
        else:
            status = "CLOSED"

        s.close()
        scan_total += 1

    print(f"SCAN COMPLETE: {scan_total} of {high_port - low_port + 1}")


wait_time = 0.5

scan_ports(ip, low_port, high_port, wait_time)

