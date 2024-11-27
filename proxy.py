import http.server
import socketserver
import socket
import threading
import re
import os
import subprocess


def kill_process_on_port(port):
    try:
        # Use netstat to check which process is using the port
        cmd = f"netstat -ano | findstr :{port}"
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

        # Parse the PID
        lines = output.strip().split("\n")
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                # Kill the process using the port
                print(f"Killing process with PID: {pid} on port {port}")
                os.system(f"taskkill /PID {pid} /F")
    except subprocess.CalledProcessError:
        print(f"No process is using port {port}.")


# Stop any process using port 8888


# Path to the local rule file
RULES_FILE = "anti-ad-adguard.txt"

def adguard_to_regex(rule):
    # Ignore whitelisted rules
    if rule.startswith('@@'):
        rule = rule[2:]
    # Replace || to match domain names
    if rule.startswith('||'):
        rule = rule[2:]
        rule = r'(?:^|\.)' + rule
    # Handle the ending '^' for URL boundaries
    rule = rule.replace('^', r'(?:$|[/?#])')
    # Replace wildcard * with regex .*
    rule = rule.replace('*', '.*')
    # Return the compiled regex without unnecessary escaping
    return re.compile(rule)

# Load rules from the local file
def load_rules_from_file(file_path):
    ad_block_patterns = []
    counter = 0
    max_lines = 10
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Uncomment the following lines to limit the number of rules for testing
            # counter += 1
            # if counter > max_lines:
            #     break
            # print('line:', line)
            line = line.strip()
            # Ignore comments and invalid lines
            if line and not line.startswith('!') and not line.startswith('['):
                pattern = adguard_to_regex(line)
                # print('pattern:', pattern)
                ad_block_patterns.append(pattern)
    return ad_block_patterns

# Load ad-blocking rules
ad_block_patterns = load_rules_from_file(RULES_FILE)
print(f"Loaded {len(ad_block_patterns)} ad block patterns.")
test_url = "pagead2.googlesyndication.com"
if any(pattern.search(test_url) for pattern in ad_block_patterns):
    print("Matched!")

# Define ad-blocking rules for testing
AD_BLOCK_PATTERNS = [
    r"ads\.example\.com",   # Example ad domain
    r".*\.doubleclick\.net", # Common ad platform
    r".*\.adservice\.google\.com",  # Google Ads
]

PORT = 8888  # Local proxy server port

class AdBlockProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_CONNECT(self):
        print(f"Establishing tunnel for {self.path}")
        try:

            # Check if the request is for an ad
            requested_url = self.path.split(":")[0]
            print('requested_url:', requested_url)
            print('pattern match:', any(pattern.search(requested_url) for pattern in ad_block_patterns))
            if any(pattern.search(requested_url) for pattern in ad_block_patterns):
                print(f"Blocked connect URL: {requested_url}")
                raise Exception("Blocked URL")


            # Parse the target host and port
            target_host, target_port = self.path.split(":")
            target_port = int(target_port)
            
            # Establish a connection with the target server
            target_socket = socket.create_connection((target_host, target_port))
            self.send_response(200, "Connection Established")
            self.end_headers()

            # Start bi-directional traffic forwarding
            client_socket = self.connection
            t1 = threading.Thread(target=self.forward_data, args=(client_socket, target_socket))
            t2 = threading.Thread(target=self.forward_data, args=(target_socket, client_socket))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception as e:
            self.send_error(500, f"Failed to establish connection: {e}")

    def forward_data(self, source, destination):
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)
        except (socket.error, OSError) as e:
            print(f"Connection closed: {e}")
        finally:
            try:
                source.close()
            except Exception:
                pass
            try:
                destination.close()
            except Exception:
                pass

    def do_GET(self):
        # Handle normal HTTP requests
        requested_url = self.path.split(":")[0]
        print(requested_url)
        if any(pattern.search(requested_url) for pattern in ad_block_patterns):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"This request is blocked by AdBlock Proxy.")
            print(f"Blocked URL: {requested_url}")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Request allowed.")
            print(f"Allowed URL: {requested_url}")

def run_proxy():
    with socketserver.ThreadingTCPServer(("", PORT), AdBlockProxyHandler) as httpd:
        print(f"AdBlock Proxy running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # kill_process_on_port(8888)
    run_proxy()
    pass
