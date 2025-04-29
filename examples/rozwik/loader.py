import importlib.util
import os

from typing import Any
from types import ModuleType, LambdaType


def loadExtension(path: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

def getModuleAttr(module: ModuleType, name: str) -> Any:
    if name in dir(module): return getattr(module, name)
    else: return None

getParsers = lambda extension: getModuleAttr(extension, 'PARSERS')
getMaps    = lambda extension: getModuleAttr(extension, 'MAPS'   )

def importExtension(path: str) -> tuple[dict, dict]:
    mod = loadExtension(path, os.path.basename(path))

    p = getParsers(mod)
    m = getMaps(mod)

    return p, m


if __name__ == '__main__':

    mod = importExtension('./examples/rozwik/ext/01.py')
    print(f'{mod=}')