# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# from pathlib import Path
# import importlib

# # automatically import any Python files in the criterions/ directory
# for file in sorted(Path(__file__).parent.glob("*.py")):
#     if not file.name.startswith("_"):
#         importlib.import_module("graphormer.criterions." + file.name[:-3])


import os
import importlib
from . import rmse

# Automatically import all .py files in this directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("_"):
        module_name = file[:-3]
        importlib.import_module(f"graphormer.criterions.{module_name}")