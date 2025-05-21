# server.py
from mcp.server.fastmcp import FastMCP
import pandas as pd
import logging
import signal
import sys
import threading
# Import tools so they get registered via decorators
from utils.file_reader import read_parquet_summary
from utils.file_reader import read_csv_summary

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
shutdown_event = threading.Event()

mcp = FastMCP("product_mcp_server")


@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    return read_parquet_summary(filename)

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    return read_csv_summary(filename)

def handle_shutdown(signum, frame):
    if not shutdown_event.is_set():
        logging.info("Shutdown signal received.")
        shutdown_event.set()
        # Optional: restore default signal behavior
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    logging.info("Server is starting up")

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        mcp.run()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received.")
    finally:
        logging.info("Server shutdown complete.")