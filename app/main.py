"""
    main.py 
    This file is part of FastAPI.
"""
import asyncio
import signal
import sys
import time

# Use the fastAPI framework
from fastapi import FastAPI, Request, Response
from app import health, sys_config_info
from app import memory_max_use

# incl logging func
import logging

from app.sys_config_info import hostname

logging.basicConfig(level=logging.INFO, force=True,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

# use async context manager for lifespan
from contextlib import asynccontextmanager

# include health endpoints as health_router
from app.health import router as health_router

# include dynamic memory check and related functions
#from app.memory_max_use import is_memory_safe


# create lifespan object decorated with asynccontextmanager
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
           Lifespan object is yielded
           📌 yield is the divider: before → startup  // after → shutdown

    :param fastapi_app: FastAPI object
    :param health.is_ready checked
    :yield
    """
    start_time = time.time()
    logging.info("Application :: startup (lifespan) event")
    sys_config_info.is_ready = True
    sys_config_info.startup_complete= True

    for route in app.routes:
        logging.info(f"Route Loaded: {route}")

    yield
    
    logging.info("Application Startup Time:: %.2f seconds",
                 time.time() - start_time)
    sys_config_info.is_ready = False
    sys_config_info.startup_complete = False
    
    logging.info("Application :: shutdown (lifespan) event")

    sys.stdout.flush()
    sys.stderr.flush()


# instantiate an object for FastAPI     -- deprecated old way
# app = FastAPI()

# instantiate an object for FastAPI using lifespan object passed in as param
app = FastAPI(lifespan=lifespan)


# function handling SIGTERM
def handle_sigterm(sig,frame):
    """
          function handling SIGTERM
    :param sig:
    :param frame:
    :return:
    """
    print("Inside handle_sigterm()")
    logging.info(
        "SIGTERM Received ::  Shutting down in Progress Gracefully ... ")
    sys_config_info.shutdown = True
signal.signal(signal.SIGTERM, handle_sigterm)


# create a root endpoint ("/")

@app.get("/")
def root():
    """
    route /
    :return:
    """
    return {"message":"FastAPI :: Hello World :: SERVICE Running ",
            "version":"v1", "pod":hostname}


# /work to simulate close down tasks like store to DB, write to file, flush,
# etc.

@app.get("/work")
async def do_work():
    """
      /work to simulate close down tasks like store to DB, write to file,
      flush, etc.
    :return:
    """
    print("Processing Request ... ")
    logging.info("Work endpoint called")
    await asyncio.sleep(25)
    return {"status":"Work Completed", "version":"v1", "pod":hostname}

# Check memory management at this place

@app.middleware("http")
async def memory_guard_middleware(request: Request, call_next):
    """

    :param request:
    :param call_next:
    :return:
    """
    if not memory_max_use.is_memory_safe():
        return Response(status_code=503,
                        content="Service Overloaded, "
                                "Applied Memory Protection",
                        )
    return await call_next(request)


# register health_router with main app
"""
    http://127.0.0.1:8000/health/liveliness
    http://127.0.0.1:8000/health/readiness
"""
app.include_router(health_router)
app.include_router(memory_max_use.router)
