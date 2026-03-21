"""
    FastAPI MVP
"""

from fastapi import FastAPI, Query
import os

app = FastAPI()
DATA_FILE = "/data/data.txt"
print(os.getcwd())
@app.get("/write_data")
async def write_data():
    """
          write data to file
    :return:
    """
    try:
        with open(DATA_FILE, "a") as f:
            f.write("Hello World from FastAPI \n")
        return {"message": "Data Written: Hello World from FastAPI \n"}
    except FileNotFoundError:
        return {"File Not Found"}
    except PermissionError:
        return {"Permission Denied"}
    except Exception as e:
        return {"Error": str(e)}
    


@app.get("/read_data")
async def read_data():
    """
        Read Data from file
    :return:
    """
    try:
        if not os.path.exists(DATA_FILE):
            return {"data": []}
    except FileNotFoundError:
        return {"File Not Found"}
    except OSError:
        return {"Permission Denied"}
    except Exception as e:
        return {"Error": str(e)}
    
    try:
        with open(DATA_FILE, "r") as f:
            content = f.readlines()
        return {"data":content}
    except FileNotFoundError:
        return {"File Not Found"}
    except PermissionError:
        return {"Permission Denied"}
    except Exception as e:
        return {"Error":str(e)}


@app.get("/write_live_data")
async def write_live_data(message:str = Query(...)):
    """
        Write Live Data to file
    :param message:
    :return:
    """
    try:
        with open(DATA_FILE, "a") as f:
            f.write(message + "\n")
        return {"message":"Data Written: " + message + "\n"}

    except FileNotFoundError:
        return {"File Not Found"}
    except PermissionError:
        return {"Permission Denied"}
    except Exception as e:
        return {"Error":str(e)}




