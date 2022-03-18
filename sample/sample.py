import sys

sys.path.append('D:\B\python-jsonpreprocessor')

from JsonPreprocessor import CJsonPreprocessor
from JsonPreprocessor import CSyntaxType

from pprint import pprint

prepro=CJsonPreprocessor(syntax=CSyntaxType.python)

data=prepro.jsonLoad(".\json\json_with_comment.json")

pprint(data)

