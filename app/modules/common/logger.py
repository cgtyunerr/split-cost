"""Logger functions for all modules."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format=("%(asctime)s::%(levelname)s::%(message)s"),
    datefmt="%y-%m-%d-%H:%M:%S",
    handlers=[logging.StreamHandler()],
)
