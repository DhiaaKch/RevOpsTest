import subprocess

from flask import Flask, request

app = Flask(__name__)

@app.get("/ping")
def ping_host() -> str:
  host = request.args.get("host", "localhost")
  result = subprocess.run(
    f"ping -c 1 {host}",
    shell=True,
    capture_output=True,
    text=True,
    timeout=5,
  )
  return result.stdout
