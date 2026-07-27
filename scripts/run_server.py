import logging
import time
from datetime import datetime
from enum import Enum
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

from benchmarking import benchmark
from logger import configure_logging

log = logging.getLogger(__name__)


class Action(str, Enum):
    upload = "upload"
    download = "download"


class Experiment(BaseModel):
    name: str
    description: str | None = None
    temperature: float | None = None
    timestamp: datetime | None = None


def main() -> None:
    # the fastapi server
    app = FastAPI()

    @app.middleware("http")
    async def add_timing(req: Request, call_next):
        start = time.perf_counter()
        response = await call_next(req)
        elapsed = time.perf_counter() - start
        response.headers["X-Time"] = str(elapsed)
        return response

    # Hola mundo!
    @app.get("/")
    def root():
        return {"message": "Hello, World!"}

    # the analysis
    @app.get("/analysis/{action}")
    def analysis(action: Action):
        return {"action": action}

    # query parameters
    @app.get("/experiments/")
    def experiments(skip: int = 0, limit: int = 100):
        return {"skip": skip, "limit": limit}

    # the experiments
    @app.post("/experiments/")
    def create_experiment(experiment: Experiment):
        return {"id": 1, **experiment.model_dump()}

    # run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)


# call the main function
if __name__ == '__main__':
    configure_logging(logging.DEBUG)

    root_dir = Path(__file__).resolve().parent.parent
    log.debug(f"root_dir: {root_dir}")

    output_dir = root_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    log.debug(f"output_dir: {output_dir}")

    with benchmark("main", log):
        log.info("️🏎️ starting ..")
        main()
        log.info("️🏁 done.")
