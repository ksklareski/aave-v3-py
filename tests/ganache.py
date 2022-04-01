import os
import signal
import socket
import subprocess
import time

from dotenv import load_dotenv

p = None
admin_user = None


def start_ganache():
    global p
    global admin_user

    load_dotenv(override=True)
    poly_url = os.environ["POLY_URL"]
    admin_user = os.environ["ADMIN_USER"]

    # Start ganache cli
    p = subprocess.Popen(
        [
            "ganache",
            "-f",
            poly_url,
            "-i",
            "999",
            "-e",
            "1000000",
            "-p",
            "8545",
            "-l",
            "8000000",
            "-u",
            admin_user,
        ]
    )
    wait_for_port(port="8545", timeout=10)


def wait_for_port(port, host="localhost", timeout=5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    "Waited too long for the port {} on host {} to start accepting "
                    "connections.".format(port, host)
                ) from ex


def stop_ganache():
    global p
    os.kill(p.pid, signal.SIGTERM)
    time.sleep(5)
