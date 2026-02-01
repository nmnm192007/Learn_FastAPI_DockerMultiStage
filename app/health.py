"""
    FastAPI.health.py
    health endpoints feed needed information to Kubernetes K8s liveliness
    and readiness probe
    Kubernetes asks:
    Liveliness: Should I restart the container?
    Readiness: Should I send traffic to it ?
"""

# import asyncio for fluctuation simulations
import asyncio

# import APIrouter
from fastapi import APIRouter

# instantiate object for APIRouter
router = APIRouter()

# check if health app is ready
is_ready = False


# handle endpoint liveliness
@router.get("/health/liveliness")
def health_liveliness():
    """
        handles liveliness endpoint
    :return:
    """
    return {"status":"alive"}


@router.get("/health/readiness")
def health_readiness():
    """
          handles readiness endpoint     --
          http://127.0.0.1:8000/health/liveliness
          http://127.0.0.1:8000/health/readiness
    :return:  status -> dict
    """
    if not is_ready:
        return {"status":"not ready"}
    return {"status":"ready"}


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
