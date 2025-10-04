from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.post("/run-script")
async def run_script():
    try:
        # Replace 'script.py' with your Python script filename
        result = subprocess.run(
            ["python", "build_agent.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail={"stdout": e.stdout, "stderr": e.stderr})

# To run this FastAPI app, save this to main.py and use:
# uvicorn main:app --reload
