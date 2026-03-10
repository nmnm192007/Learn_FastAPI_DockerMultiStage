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

# import APIrouter
from fastapi import APIRouter, Response

# implement memory management
import memory_max_use
import sys_config_info

# instantiate object for APIRouter
router = APIRouter()


# handle endpoint liveliness
@router.get("/health/liveliness")
def health_liveliness():
    """
        handles liveliness endpoint
                  http://127.0.0.1:8000/health/liveliness
    :return:
    """
    # return {"status":"alive"}
    # if random.randint(1,10) < 7:
    if sys_config_info.is_ready:
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
    if not sys_config_info.is_ready:
        return Response(status_code=503)

    if not memory_max_use.is_memory_safe():
        return Response(status_code=503)

    return Response(status_code=200)


@router.post("/health/toggle")
def toggle_readiness():
    """
        Temporary Function to check is_ready behaviour
    :return:
    """
    sys_config_info.is_ready = not sys_config_info.is_ready
    tmp_str =  "is_ready:"+ str(sys_config_info.is_ready)
    return Response(status_code=200, content=tmp_str)


@router.get("/health/simulate_fluctuations")
async def simulate_fluctuations():
    """
       simulate fluctuations endpoint
    :return:
    """
    await asyncio.sleep(2)
    sys_config_info.is_ready = not sys_config_info.is_ready
    tmp_str = "is_ready:" + str(sys_config_info.is_ready)
    return Response(status_code=200, content=tmp_str)


# /startup - the code supporting startup probe
@router.get("/health/startup")
async def startup():
    """
      /startup - the code supporting startup probe
    :return:  JSON  {status,version,pod,httpCode}
    """
    if sys_config_info.startup_complete:
        tmp_str = ("Startup Completed"+ "v1" + sys_config_info.hostname +
                   "httpCode:"+ "200")
        return Response(status_code=200, content= tmp_str)
    tmp_str = ("Startup In Progress" + "v1" + sys_config_info.hostname +
               "httpCode:" + "503")
    return Response(status_code=503, content= tmp_str)
