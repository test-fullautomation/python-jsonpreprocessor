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

# Executes JsonPreprocessor acceptance test.
#!/bin/sh

bash_file_path=`readlink -f "${BASH_SOURCE:-$0}"`
atest_dir=`dirname $bash_file_path`
cd $atest_dir/jsonpreprocessor
export PYTHONPATH="$atest_dir/../"
echo $PYTHONPATH
   $RobotPythonPath/python3 -m pytest jsonpreprocessor_unittest.py --junit-xml=../logs/linux_jsonpreprocessor_unittest.xml && (
   echo "Run JsonPreprocessor acceptance test successful!"
 ) || (
   echo "Run JsonPreprocessor acceptance test failed!"
 )