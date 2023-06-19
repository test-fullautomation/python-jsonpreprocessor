#  Copyright 2020-2023 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#################################################################################

## This example also shows how to import json files
## into json files.

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../"))

from JsonPreprocessor import CJsonPreprocessor

from pprint import pprint

prepro=CJsonPreprocessor()

# you can load the base json file with
# - relative path to your python program
# - absolute path
# - paths containting environment variables by means of
#   %envvariable% syntax
data=prepro.jsonLoad(os.path.dirname(__file__) + "/json/json_with_import.json")

pprint(data)

