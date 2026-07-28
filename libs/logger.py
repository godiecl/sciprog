#  Copyright (c) 2026. Programacion Cientifica, DISC, Antofagasta, Chile.

import logging

import coloredlogs


def configure_logging(level: int = logging.DEBUG) -> None:
    """Configure the logging module."""
    coloredlogs.install(
        level=level,
        fmt="%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d (%(process)d/%(threadName)s) - %(message)s",
        level_styles={
            "DEBUG": {"color": "black", "bright": True},
            "INFO": {"color": "green"},
            "WARNING": {"color": "magenta"},
            "ERROR": {"color": "red"},
            "CRITICAL": {"color": "red", "bold": True},
        },
        field_styles={
            "asctime": {"color": "yellow"},
            "levelname": {"bold": True},
            "name": {"color": "blue", "bold": True},
            "lineno": {"color": "magenta"},
            "process": {"color": "blue", "bold": True},
            "threadName": {"color": "cyan"},
            "message": {"color": "white"},

        },
        milliseconds=True,
    )

    # decrease the level of logger in external libraries
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
    logging.getLogger("git.cmd").setLevel(logging.WARNING)
    logging.getLogger("git.util").setLevel(logging.WARNING)
    logging.getLogger("graphviz._tools").setLevel(logging.WARNING)
    logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
    logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("matplotlib.colorbar").setLevel(logging.WARNING)
    logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)
    logging.getLogger("matplotlib.pyplot").setLevel(logging.WARNING)
    logging.getLogger("mlflow.store.db.utils").setLevel(logging.WARNING)
    logging.getLogger("mlflow.tracking.fluent").setLevel(logging.WARNING)
    logging.getLogger("numba.core").setLevel(logging.WARNING)
    logging.getLogger("scrapling").setLevel(logging.WARNING)
    logging.getLogger("websockets.client").setLevel(logging.WARNING)
