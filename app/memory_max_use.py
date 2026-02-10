"""
    demo app for memory usage
"""

import psutil
import os
import logging

from fastapi import APIRouter

router = APIRouter()

data = []

MAX_MEMORY_MB = int(os.getenv("MAX_MEMORY_MB", "450"))

def is_memory_safe() -> bool:
    """
       Checks if memory used breached threshold
    :return:
    """
    process = psutil.Process(os.getpid())
    used_memory = process.memory_info().rss / (1024 * 1024)

    logging.info(f"Memory used:  {used_memory:.2f} MB")

    if used_memory > MAX_MEMORY_MB:
        logging.error(f"Memory exceeded {MAX_MEMORY_MB} MB, rejecting "
                      f"traffic.")
        return False
    return True




@router.get("/eat-memory")
def eat_memory():
    """
        demo func for eating memory TEST

    """
    while True:
        data.append("X" * 10_000_000)  # ~10MB per iteration

