from fastapi import FastAPI, HTTPException
import subprocess
from request import build_agent
import uvicorn
app = FastAPI()

@app.post("/run-script")
async def run_script():
    try:
        # Replace 'script.py' with your Python script filename
        # result = subprocess.run(
        #     ["python", "build_agent.py"],
        #     capture_output=True,
        #     text=True,
        #     check=True
        # )
        result=build_agent()
        return {"agent_id":result}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail={"stdout": e.stdout, "stderr": e.stderr})
if  __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)
# To run this FastAPI app, save this to main.py and use:
# uvicorn main:app --reload
