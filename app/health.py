"""
    FastAPI.health.py
    health endpoints feed needed information to Kubernetes K8s liveliness
    and readiness probe
    Kubernetes asks:
    Liveliness: Should I restart the container?
    Readiness: Should I send traffic to it ?
    Startup: Should I start up?
"""

# import asyncio for fluctuation simulations
import asyncio
import random

# import APIrouter
from fastapi import APIRouter, Response


# implement memory management
from .memory_max_use import is_memory_safe
from .sys_config_info import hostname, startup_complete

# instantiate object for APIRouter
router = APIRouter()

# check if health app is ready
is_ready = False


# handle endpoint liveliness
@router.get("/health/liveliness")
def health_liveliness():
    """
        handles liveliness endpoint
                  http://127.0.0.1:8000/health/liveliness
    :return:
    """
    # return {"status":"alive"}
    if random.randint(1,10) < 7:
    # if is_ready:
         return Response(status_code=200)
    else:
        return Response(status_code=503)


@router.get("/health/readiness")
def health_readiness():
    """
          handles readiness endpoint     --
          http://127.0.0.1:8000/health/readiness
    :return:  status
    """
    if not is_ready:
        return Response(status_code=503)

    if not is_memory_safe():
        return Response(status_code=503)
    
    return Response(status_code=200)


@router.post("/health/toggle")
def toggle_readiness():
    """
        Temporary Function to check is_ready behaviour
    :return:
    """
    global is_ready
    is_ready = not is_ready
    return {"is_ready":is_ready}


@router.get("/health/simulate_fluctuations")
async def simulate_fluctuations():
    """
       simulate fluctuations endpoint
    :return:
    """
    global is_ready
    await asyncio.sleep(2)
    # if not is_ready:
    #     is_ready = True
    # else:
    #     is_ready = False
    is_ready = not is_ready
    return {"is_ready":is_ready}


# /startup - the code supporting startup probe
@router.get("/health/startup")
async def startup():
    """
      /startup - the code supporting startup probe
    :return:  JSON  {status,version,pod}
    """
    if startup_complete:
        return {"status":"Startup Completed", "version":"v1", "pod":hostname,
                "httpCode": "200"}
    return {"status":"Startup In Progress", "version":"v1", "pod":hostname,
            "httpCode":"503"}

