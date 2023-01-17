import os
import sys
import pytest
from JsonPreprocessor import CJsonPreprocessor

os.chdir(os.path.realpath(os.path.dirname(__file__)))
sys.path.append("../testdata")
from templates import *

class TestJsonFormat:

    def test_json_config_format_01(self):
        '''
        Test with json config file has standard format without commnent.
        '''
        sJsonfile = os.path.abspath("../testdata/config/07_json_format/json_format_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == JSONFORMAT

    def test_json_config_format_02(self):
        '''
        Test with the standard json config file has commnents.
        '''
        sJsonfile = os.path.abspath("../testdata/config/07_json_format/json_format_02.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == JSONFORMAT

    def test_json_config_format_03(self):
        '''
        Test with the json config file has commnents.
        The elements and values contain //
        '''
        sJsonfile = os.path.abspath("../testdata/config/07_json_format/json_format_03.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == JSONFORMAT

    def test_json_config_format_04(self):
        '''
        Test with the json config file has commnents.
        The elements and values contain //
        Some unusual new lines in json config file.
        '''
        sJsonfile = os.path.abspath("../testdata/config/07_json_format/json_format_04.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == JSONFORMAT

    def test_json_config_format_05(self):
        '''
        Test with the json config file has only 1 line with //
        '''
        sJsonfile = os.path.abspath("../testdata/config/07_json_format/json_format_05.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == JSONFORMAT

class TestLoadJsonFiles:

    def test_load_proper_file(self):
        sJsonfile = os.path.abspath("../testdata/config/01_proper_json/proper_file_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == PROPERCONFIGFILE

    def test_import_one_file_01(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_one_file01_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILE01

    def test_import_one_file_02(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_one_file02_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILE02

    def test_import_one_file_03(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_one_file03_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILE03

    def test_import_one_file_04(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_one_file04_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILE04

    def test_import_files_05(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_files01_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILES01

    def test_import_files_06(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_files02_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILES02

    def test_import_files_07(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_files03_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILES03

    def test_import_files_08(self):
        sJsonfile = os.path.abspath("../testdata/config/02_import_json/import_files04_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILES04

class TestNestedImport:

    def test_nested_import_one_file_01(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import01_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT01

    def test_nested_import_one_file_02(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import02_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT02

    def test_nested_import_one_file_03(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import03_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT03

    def test_nested_import_one_file_04(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import04_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT04

    def test_nested_import_one_file_05(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import05_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT05

    def test_nested_import_one_file_06(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import06_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT06

    def test_nested_import_one_file_07(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import07_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT07

    def test_nested_import_one_file_08(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import08_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT08

    def test_nested_import_one_file_09(self):
        sJsonfile = os.path.abspath("../testdata/config/03_nested_import/nested_import09_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == NESTEDIMPORT09

class TestReimport:

    def test_re_import_01(self):
        sJsonfile = os.path.abspath("../testdata/config/04_re_import/re_import_file01_config.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData == IMPORTEDFILE01

class TestOverrideParameters:

    def test_override_parameter_01(self):
        '''
        The parameters are overrided in the same configuration file.
        '''
        sJsonfile = os.path.abspath("../testdata/config/06_override_params/project_config_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData['params']['global']['dSUT']['audio']['volume']['bSupported'] == PARAMOVERRIDE['testcase_01a']
        assert oJsonData['version']['patchversion'] == PARAMOVERRIDE['testcase_01b']
        assert oJsonData['params']['global']['dSUT']['system']['sDetails'] == PARAMOVERRIDE['testcase_01c']

    def test_override_parameter_02(self):
        '''
        The parameters in imported json file are overrided.
        '''
        sJsonfile = os.path.abspath("../testdata/config/06_override_params/project_config_02.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData['gPreproString'] == PARAMOVERRIDE['testcase_02a']
        assert oJsonData['gPreproStructure']['test01'] == PARAMOVERRIDE['testcase_02b']
        assert oJsonData['gPreproFloatParam'] == PARAMOVERRIDE['testcase_02c']

    def test_override_parameter_03(self):
        '''
        The parameters in imported json file are overrided in other imported file, overrided json object, added new json object, ...
        '''
        sJsonfile = os.path.abspath("../testdata/config/06_override_params/project_config_03.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData['params']['global']['dSUT']['audio']['volume']['bSupported'] == PARAMOVERRIDE['testcase_03a']
        assert oJsonData['params']['global']['dSUT']['abc'] == PARAMOVERRIDE['testcase_03b']
        assert oJsonData['params']['global']['dSUT']['tuner']['fm']['frequency']['bSupported'] == PARAMOVERRIDE['testcase_03c']
        assert oJsonData['params']['global']['newStruct'] == PARAMOVERRIDE['testcase_03d']
        assert oJsonData['params']['global']['TestLogfileName'] == PARAMOVERRIDE['testcase_03e']
        assert oJsonData['params']['global']['dSUT']['system']['hardware'] == PARAMOVERRIDE['testcase_03f']
        assert oJsonData['params']['global']['Testparms']['Testglobal'] == PARAMOVERRIDE['testcase_03g']

class TestSubDataStructure:

    def test_sub_data_structure_01(self):
        '''
        Updated 1 parameter without nested variable.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_01.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['preprocessor']['definitions']['preproFloatParam'] == SUBDATASTRUCTURE['testcase_01']

    def test_sub_data_structure_02(self):
        '''
        Updated more than 1 parameter without nested variable.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_02.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['params']['glo']['globalString'] == SUBDATASTRUCTURE['testcase_02a']
        assert oJsonData['preprocessor']['definitions']['preproStructure']['variable_01'] == SUBDATASTRUCTURE['testcase_02b']
        assert oJsonData['Project'] == SUBDATASTRUCTURE['testcase_02c']

    def test_sub_data_structure_03(self):
        '''
        Updated 1 parameter with nested variable in element name.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_03.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['preprocessor']['definitions']['preproStructure']['general'] == SUBDATASTRUCTURE['testcase_03']

    def test_sub_data_structure_04(self):
        '''
        Updated 1 parameter with nested variable in element value.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_04.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['params']['glo']['globalString'] == SUBDATASTRUCTURE['testcase_04']

    def test_sub_data_structure_05(self):
        '''
        Updated 1 parameter with nested variable in both element name and value.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_05.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['preprocessor']['definitions']['preproTest']['checkParam'] == SUBDATASTRUCTURE['testcase_05']

    def test_sub_data_structure_06(self):
        '''
        Updated more than 1 parameter with nested variable.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_01.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        sUpdateJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/json_update_06.json")
        oUpdateJsonData = oJsonPreprocessor.jsonLoad(sUpdateJsonfile)
        oJsonData.update(oUpdateJsonData)

        assert oJsonData['sWelcome'] == SUBDATASTRUCTURE['testcase_06a']
        assert oJsonData['params']['glo'] == SUBDATASTRUCTURE['testcase_06b']
        assert oJsonData['params']['Test01'] == SUBDATASTRUCTURE['testcase_06c']
        assert oJsonData['preprocessor']['definitions'] == SUBDATASTRUCTURE['testcase_06d']

    def test_sub_data_structure_07(self):
        '''
        The value is list contained dictionary element.
        '''
        sJsonfile = os.path.abspath("../testdata/config/05_sub_datastructure/sub_data_structure_02.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)

        assert oJsonData['arrayTest01'][2]['test1'] == SUBDATASTRUCTURE['testcase_07a']
        assert oJsonData['preprocessor']['definitions']['preproStructure']['arrayTest02'][1]['check1'] == SUBDATASTRUCTURE['testcase_07b']

class TestNoneTrueFalseDatatype:

    def test_none_true_false_datatype(self):
        '''
        Test python data types and syntax to json. ``True``, ``False`` and ``None`` will be a accepted as json syntax elements.
        '''
        sJsonfile = os.path.abspath("../testdata/config/06_override_params/project_config_04.json")
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        oJsonData = oJsonPreprocessor.jsonLoad(sJsonfile)
        assert oJsonData['string_null'] == "null"
        assert oJsonData['string_none'] == '"None"'
        assert oJsonData['string_true'] == '"True"'
        assert oJsonData['string_false'] == '"False"'
        assert oJsonData['convert_null_to_string'] == '"None"'
        assert oJsonData['convert_none_to_string'] == '"None"'
        assert oJsonData['convert_float_to_string'] == "1.332"
        assert oJsonData['convert_true_to_string'] == '"True"'
        assert oJsonData['convert_false_to_string'] == '"False"'
        assert oJsonData['params']['global'] == JSONFORMAT_NONE_TRUE_FALSE['params']['global']
        assert oJsonData['preprocessor']['definitions'] == JSONFORMAT_NONE_TRUE_FALSE['preprocessor']['definitions']