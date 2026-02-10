"""
    main.py 
    This file is part of FastAPI.
"""
import sys

# Use the fastAPI framework
from fastapi import FastAPI, Request, Response
from app import health
from app import memory_max_use

# incl logging func
import logging
logging.basicConfig(level=logging.INFO, force=True,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

# use async context manager for lifespan
from contextlib import asynccontextmanager

# include health endpoints as health_router
from app.health import router as health_router

# include dynamic memory check and related functions
from app.memory_max_use import is_memory_safe

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
    logging.info("Application :: startup (lifespan) event")
    health.is_ready = True
    yield
    health.is_ready = False
    logging.info("Application :: shutdown (lifespan) event")
    sys.stdout.flush()
    sys.stderr.flush()

    

# instantiate an object for FastAPI     -- deprecated old way
# app = FastAPI()

# instantiate an object for FastAPI using lifespan object passed in as param
app = FastAPI(lifespan=lifespan)


# create a root endpoint ("/")

@app.get("/")
def root():
    """
    route /
    :return:
    """
    return {"message":"FastAPI :: Hello World"}



# Check memory management at this place

@app.middleware("http")
async def memory_guard_middleware(request: Request, call_next):
    """

    :param request:
    :param call_next:
    :return:
    """
    if not is_memory_safe():
        # # from starlette import status
        # # return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        #                 content={"message":
        #                              "FastAPI :: Hello World  -- "
        #                                    "Service Overloaded, Applied "
        #                                    "Memory Protection"}
        #                 )

        return Response(status_code=503, content="Service Overloaded, Applied Memory Protection",
                        )
    return await call_next(request)



# register health_router with main app
"""
    http://127.0.0.1:8000/health/liveliness
    http://127.0.0.1:8000/health/readiness
"""
app.include_router(health_router)
app.include_router(memory_max_use.router)
