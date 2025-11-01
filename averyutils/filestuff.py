from averyutils import avery_logger
from pathlib import Path
from typing import *

def load_file(filepath: Path | str, defaults: Any) -> Any:
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            filepath.touch()
        with open(file=filepath, mode="r", encoding="utf-8") as file:
            data = file.read()
            if not data:
                return defaults
            else:
                return data
    except Exception as e:
        avery_logger.warn(f"couldn't load file {e}")
        return None

def save_file(filepath: Path | str, data: Any):
    try:
        filepath = Path(filepath)
        with open(file=filepath, mode="w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        avery_logger.warn(f"couldn't save file {e}")

def encode_data(data: Any, encoder: Callable, **encodekwargs) -> Any:
    try:
        pdata = encoder(data, **encodekwargs)
        return pdata
    except Exception as e:
        avery_logger.warn(f"couldn't encode data {e}")
        return None

def decode_data(data: Any, decoder: Callable, **decodekwargs) -> Any:
    try:
        pdata = decoder(data, **decodekwargs)
        return pdata
    except Exception as e:
        avery_logger.warn(f"couldn't decode data {e}")
        return data