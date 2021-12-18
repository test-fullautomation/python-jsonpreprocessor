#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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
'''
The script for running jsonpreprocessor's acceptance tests with Robot Framework
testsuites management.

'''

import os
import sys
import robot
import argparse

from os.path import abspath, dirname

if __name__ == '__main__':
    os.chdir(dirname(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='The testsuite file or testsuite directory',
                        default = './jsonpreprocessor')
    parser.add_argument('-o', '--outputdir', help='The output directory which stores test logs',
                        default = './logs')
    
    args = parser.parse_args()
    
    status = robot.run(args.source, outputdir = args.outputdir)
    
    sys.exit(status)