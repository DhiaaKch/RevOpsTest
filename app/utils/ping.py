import os

def ping_host(host: str) -> str:
    # BAD: user input passed straight to the shell
    output = os.popen(f"ping -c 1 {host}").read()
    return output
