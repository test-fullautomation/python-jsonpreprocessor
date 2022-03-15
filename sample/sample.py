import sys
sys.path.append('D:\B\python-jsonpreprocessor')

import JsonPreprocessor
from pprint import pprint

prepro=JsonPreprocessor.CJsonPreprocessor()

data=prepro.jsonLoad(".\json\json_with_comment.json")

pprint(data)

