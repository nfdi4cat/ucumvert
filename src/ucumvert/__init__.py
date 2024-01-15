from __future__ import annotations

import logging
import os
from pathlib import Path

from ucumvert.parser import (
    get_ucum_parser,
    make_parse_tree_png,
    update_lark_ucum_grammar_file,
)
from ucumvert.ucum_pint import (
    UcumToPintStrTransformer,
    UcumToPintTransformer,
    get_pint_registry,
    ucum_preprocessor,
)

try:
    from ucumvert._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

__all__ = [
    "get_ucum_parser",
    "get_pint_registry",
    "make_parse_tree_png",
    "ucum_preprocessor",
    "update_lark_ucum_grammar_file",
    "UcumToPintTransformer",
    "UcumToPintStrTransformer",
]

# Note that nothing is passed to getLogger to set the "root" logger
logger = logging.getLogger()


def setup_logging(loglevel: int = logging.INFO, logfile: Path | None = None) -> None:
    """
    Setup logging to console and optionally a file.

    The default loglevel is INFO.
    """
    loglevel_name = os.getenv("LOGLEVEL", "").strip().upper()
    if loglevel_name in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        loglevel = getattr(logging, loglevel_name, logging.INFO)

    # Apply constraints. CRITICAL=FATAL=50 is the maximum, NOTSET=0 the minimum.
    loglevel = min(logging.FATAL, max(loglevel, logging.NOTSET))

    # Setup handler for logging to console
    logging.basicConfig(level=loglevel, format="%(levelname)-8s|%(message)s")

    if logfile is not None:
        # Setup handler for logging to file
        fh = logging.handlers.RotatingFileHandler(
            logfile, maxBytes=100000, backupCount=5
        )
        fh.setLevel(loglevel)
        fh_formatter = logging.Formatter(
            fmt="%(asctime)s|%(name)-20s|%(levelname)-8s|%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)
