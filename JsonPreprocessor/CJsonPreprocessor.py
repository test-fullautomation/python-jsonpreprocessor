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
#
# File: JsonPreprocessor.py
#
# This module uses to handle connfiguration file in json format (import another
# json file to the json file).
# Allows user adds comment into json config file
#
# History:
#
# 2021-01:
#    - Initially created by Mai Dinh Nam Son (RBVH/ECM11)
#
# 2021-02-08:
#   - Use object_pairs_hook of json.load() to process [import] node(s).
#     Allow to use multiple [import] node(s) at same level.
#   - Avoid cyclic import
#
# 2021-02-17:
#   - Replace method to load json data json.load() by json.loads()
#     to load string data after removing comment(s)
#
# 2021-02-18:
#   - Add parameter syntax to support Python types if required:
#     None  => null
#     True  => true
#     False => false
#
# 2021-03-29:
#   - Adds update configuration using json file
#   - Handles nested parameter in json config file
#################################################################################


import os
import json
import regex
import sys
import copy
import shlex
import hashlib
import unicodedata
import ast

from PythonExtensionsCollection.String.CString import CString
from enum import Enum
from JsonPreprocessor.version import VERSION, VERSION_DATE
from pydotdict import DotDict

class CSyntaxType():
    python = "python"
    json = "json"

class CNameMangling(Enum):
    AVOIDDATATYPE    = "JPavoidDataType_"
    COLONS           = "__handleColonsInLine__"
    NESTEDPARAM      = "__handleNestedParamInLine__"
    DUPLICATEDKEY_00 = "__handleDuplicatedKey__00"
    DUPLICATEDKEY_01 = "__handleDuplicatedKey__"
    STRINGCONVERT    = "__ConvertParameterToString__"
    LISTINDEX        = "__IndexOfList__"
    SLICEINDEX       = "__SlicingIndex__"
    STRINGVALUE      = "__StringValueMake-up__"
    HANDLEIMPORTED   = "__CheckImportedHandling__"
    DYNAMICIMPORTED  = "__DynamicImportedHandling__"
    PYTHONBUILTIN    = "__PythonBuiltInFunction__"
    PYBUILTINSTR     = "__StrInPythonInlineCode__"
    BYTEVALUE        = "__HandleByteValue__"

class CPythonJSONDecoder(json.JSONDecoder):
    """
Extends the JSON syntax by the Python keywords ``True``, ``False`` and ``None``.

**Arguments:**

* ``json.JSONDecoder``

  / *Type*: object /

  Decoder object provided by ``json.loads``
    """

    NUMBER_RE = regex.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (regex.VERBOSE | regex.MULTILINE | regex.DOTALL))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan_once = self.custom_scan_once

    def _custom_scan_once(self, string :str, idx: int) -> any:
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx) from None

        if nextchar == '"':
            return self.parse_string(string, idx + 1, self.strict)
        elif nextchar == '{':
            return self.parse_object((string, idx + 1), self.strict,
                self._custom_scan_once, self.object_hook, self.object_pairs_hook, self.memo)
        elif nextchar == '[':
            return self.parse_array((string, idx + 1), self._custom_scan_once)
        elif nextchar == 'n' and string[idx:idx + 4] == 'null':
            return None, idx + 4
        elif nextchar == 't' and string[idx:idx + 4] == 'true':
            return True, idx + 4
        elif nextchar == 'f' and string[idx:idx + 5] == 'false':
            return False, idx + 5
        elif nextchar == 'N' and string[idx:idx + 4] == 'None':
            return None, idx + 4
        elif nextchar == 'T' and string[idx:idx + 4] == 'True':
            return True, idx + 4
        elif nextchar == 'F' and string[idx:idx + 5] == 'False':
            return False, idx + 5

        m = CPythonJSONDecoder.NUMBER_RE.match(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = self.parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = self.parse_int(integer)
            return res, m.end()
        elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
            return self.parse_constant('NaN'), idx + 3
        elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
            return self.parse_constant('Infinity'), idx + 8
        elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
            return self.parse_constant('-Infinity'), idx + 9
        else:
            raise StopIteration(idx)

    def custom_scan_once(self, string : str, idx : int) -> any:
        try:
            return self._custom_scan_once(string, idx)
        finally:
            self.memo.clear()

class CKeyChecker():
    """
CkeyChecker checks key names format based on a rule defined by user.
    """
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern
        self.error_msg   = ''

    def key_name_checker(self, key_name: str):
        if key_name=='' or regex.match(r'^\s+$', key_name):
            self.error_msg = "Empty key name detected. Please enter a valid name."
            return False
        if regex.match(self.key_pattern, key_name):
            return True
        else:
            self.error_msg = f"Error: Key name '{key_name}' is invalid. Expected format: '{self.key_pattern}'"
            return False

class CTreeNode():
    """
The CTreeNode class is a custom tree data structure that allows to create and manage hierarchical data.
    """

    def __init__(self, value, parent=None):
        self.value    = value
        self.parent   = parent
        self.children = {}    # Dictionary to store children

    def add_child(self, value):
        """
Add a child node to the current node.

**Arguments:**

* ``value``

  / *Condition*: required / *Type*: str /

  The value for the new child node.

**Returns:**

  The new or existing child node.
        """
        if value in self.children:
            return self.children[value]
        child_node = CTreeNode(value, parent=self)
        self.children[value] = child_node
        return child_node

    def get_path_to_root(self):
        """
Retrieve the path from this node to the root.
        """
        path = []
        current = self
        while current:
            path.append(current.value)
            current = current.parent
        return path[::-1]

    # def display(self, level=0):
    #     if self is None:
    #         pass
    #     print("  " * level + str(self.value))
    #     for child in self.children.values():
    #         child.display(level + 1)

class CTextProcessor():
    @staticmethod
    def load_and_remove_comments(jsonP : str, is_file = True) -> str:
        """
Loads a given json file or json content and filters all C/C++ style comments.

**Arguments:**

* ``jsonP``

  / *Condition*: required / *Type*: str /

  Path of file to be processed or a JSONP content.

* ``is_file``

  / *Condition*: required / *Type*: bool /

  Indicates the jsonP is a path of file or a JSONP content, default value is True.

**Returns:**

* ``sContentCleaned``

  / *Type*: str /

  String version of JSON file after removing all comments.
        """
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return ""
            else:
                return s

        if is_file:
            file=open(jsonP, mode='r', encoding='utf-8')
            content=file.read()
            file.close()
        else:
            content = jsonP

        pattern = regex.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', regex.DOTALL | regex.MULTILINE)
        content_cleaned=regex.sub(pattern, replacer, content)
        return content_cleaned

    @staticmethod
    def multiple_replace(input : str, replacements : dict) -> str:
        """
    Replaces multiple parts in a string.

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``output``

  / *Type*: str /

        """
        pattern = regex.compile('|'.join(regex.escape(key) for key in replacements.keys()))
        output = pattern.sub(lambda x: replacements[x.group()], input)
        return output

    @staticmethod
    def normalize_digits(input : str) -> str:
        """
Convert/Replace all Unicode digits inside square brackets like [<digits>] to [<ASCII digits>].

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

  The string which need to find and convert Unicode digits to ASCII digits.

**Returns:**

* ``result``

  / *Type*: str /

  The string contains only ASCII digits within brackets.

**Raises:**

 * ``TypeError``: If input is not a string.
        """
        # Validate input type
        if not isinstance(input, str):
            error_msg = f'Invalid input type: {type(input)}. Expected str.'
            raise Exception(error_msg)
        
        # Define regex pattern to match Unicode digits within brackets
        pattern = r'\[\s*(\p{Nd}+)\s*\]'

        # Replace using the ASCII equivalent
        def replacer(match):
            digits = match.group(1)
            try:
                ascii_digits = ''.join(str(unicodedata.decimal(item)) for item in digits)
                return f'[{ascii_digits}]'
            except ValueError as e:
                # retain original match if conversion fails without further message
                return match.group(0)
        
        try:
            # Perform the replacement
            result = regex.sub(pattern, replacer, input)
        except regex.error as e:
            error_msg = f'Could not replace Unicode digits with their ASCII equivalents. Regex error occurred: {e}'
            raise Exception(error_msg)
        return result

class CJsonPreprocessor():
    """
CJsonPreprocessor extends the JSON syntax by the following features:

* Allow c/c++-style comments within JSON files
* Allow to import JSON files into JSON files
* Allow to define and use parameters within JSON files
* Allow Python keywords ``True``, ``False`` and ``None``
    """

    def getVersion(self):
        """
Returns the version of JsonPreprocessor as string.
        """
        return VERSION
    
    def getVersionDate(self):
        """
Returns the version date of JsonPreprocessor as string.
        """
        return VERSION_DATE

    def __init__(self, syntax: CSyntaxType = CSyntaxType.python , current_cfg : dict = {}, key_pattern = r'.+') -> None:
        """
Constructor

**Arguments:**

* ``syntax`` (*CSyntaxType*) optional

  / *Condition*: optional / *Type*: CSyntaxType / *Default*: python /

  If set to ``python``, then Python data types are allowed as part of JSON file.

* ``current_cfg`` (*dict*) optional

  / *Condition*: optional / *Type*: dict / *Default*: {} /

  Used to update parameters from jsonp file to current JSON object.
        """
        import builtins
        import keyword
        if not isinstance(key_pattern, str):
            key_pattern_type = regex.search(r"('.+')>\s*$", str(type(key_pattern)))[1]
            raise Exception(f"The key pattern must be 'str' but received {key_pattern_type}!")
        elif key_pattern=='' or key_pattern=='.*':
            raise Exception(f"The key pattern '{key_pattern}' allows key names that are empty or contains only whitespace!")
        elif regex.match(r'^\s+$', key_pattern):
            raise Exception(f"The key pattern '{key_pattern}' just allows a key name that contains only whitespace!")
        else:
            self.key_pattern = key_pattern
        self.list_datatypes      = [name for name, value in vars(builtins).items() if isinstance(value, type)]
        self.special_characters  = r"!#$%^&()=[]{}|;',?`~"
        self.py_call_pattern     = r'<<\s*(?:(?!<<\s*|>>).)*>>' # The pattern of call Python builtin function in JSONP
        self.list_datatypes.append(keyword.kwlist)
        self.json_path           = None
        self.import_tree         = None
        self.current_node        = None
        self.master_file         = None
        self.handling_file       = []
        self.import_check        = []
        self.recursive_level     = 0
        self.is_dynamic_import    = False
        self.i_dynamic_import    = 0
        self.l_dynamic_imports   = []
        self.syntax              = syntax
        self.current_cfg         = current_cfg
        self.dUpdatedParams      = {}
        self.dot_in_param_name   = []
        self.json_pre_check      = False
        self.json_check          = {}
        self.jp_globals          = {}
        self.key_ddict_coverted  = {}
        self.byte_value_index    = 0
        self.byte_value          = {}
        self.python_type_error   = ["object is not subscriptable",
                                    "string indices must be integers",
                                    "list indices must be integers",
                                    "index out of range"]

    def __get_failed_json_doc(self, json_decode_error=None, area_before_position=50, area_after_position=20, one_line=True):
        failed_json_doc = None
        if json_decode_error is None:
            return failed_json_doc
        try:
            json_doc = json_decode_error.doc
        except:
            # 'json_decode_error' seems not to be a JSON exception object ('doc' not available)
            return failed_json_doc
        json_doc_size     = len(json_doc)
        position_of_error = json_decode_error.pos
        if area_before_position > position_of_error:
            area_before_position = position_of_error
        if area_after_position > (json_doc_size - position_of_error):
            area_after_position = json_doc_size - position_of_error
        failed_json_doc = json_doc[position_of_error-area_before_position:position_of_error+area_after_position]
        failed_json_doc = f"... {failed_json_doc} ..."
        if one_line is True:
            failed_json_doc = failed_json_doc.replace("\n", r"\n")
        return failed_json_doc

    def __reset(self) -> None:
        """
Reset initial variables which are set in constructor method after master JSON file is loaded.
        """
        self.json_path          = None
        self.import_tree        = None
        self.current_node       = None
        self.master_file        = None
        self.handling_file      = []
        self.import_check       = []
        self.recursive_level    = 0
        self.is_dynamic_import   = False
        self.i_dynamic_import   = 0
        self.l_dynamic_imports  = []
        self.dUpdatedParams     = {}
        self.dot_in_param_name  = []
        self.json_pre_check     = False
        self.json_check         = {}
        self.jp_globals         = {}
        self.key_ddict_coverted = {}
        self.byte_value_index   = 0
        self.byte_value         = {}

    def __process_import_files(self, input_data : dict) -> dict:
        """
This is a custom decoder of ``json.loads object_pairs_hook`` function.

This method helps to import JSON files which are provided in ``"[import]"`` keyword into the current json file.

**Arguments:**

* ``input_data``

  / *Condition*: required / *Type*: (* /

  Dictionary from JSON file as input

**Returns:**

* ``out_dict``

  / *Type*: dict /

  Dictionary with resolved content from imported JSON file
        """
        out_dict = {}
        i=1
        check_element = CNameMangling.DUPLICATEDKEY_01.value
        for key, value in input_data:
            if '${' in key:
                self.__check_nested_param(key, is_key=True)
            # Check and convert dotdict in key name
            if regex.match(r'^\s*\${[^\.}]+\.[^\.]+.+$', key) and not self.json_pre_check:
                key_in_dot_format = key
                key = self.__handle_dot_in_nested_param(key_in_dot_format)
                self.key_ddict_coverted.update({key : key_in_dot_format})
            if regex.match(r'^\s*\[\s*import\s*\](\s|_\d+)*$', key.lower()):
                if not isinstance(value, str):
                    type_value = regex.search(r"^<class\s*('.+')>$", str(type(value)))
                    type_value = type_value[1] if type_value is not None else type(value)
                    error_msg = f"The [import] key requires a value of type 'str', but the type is {type_value}"
                    self.__reset()
                    raise Exception(error_msg)
                if '${' in value:
                    if not self.json_pre_check: # self.json_pre_check is set True when handling pre-check JSON files by __pre_check_json_file()
                        for item in self.l_dynamic_imports:
                            if value == next(iter(item)):
                                value = item[value]
                                break
                        if '${' in value:
                            dynamic_imported = regex.search(rf'^(.*){CNameMangling.DYNAMICIMPORTED.value}(.*)$', value)
                            value = self.__remove_token_str(dynamic_imported[2])
                            nested_params = regex.findall(rf'(\${{[^{regex.escape(self.special_characters)}]+}}(\[.*\])*)', value)
                            str_params = ''
                            for item in nested_params:
                                str_params += f"{item[0]} "
                            error_msg = f"Could not load the import file '{value}'. The parameter '{str_params}' is not available!"
                            self.__reset()
                            raise Exception(error_msg)
                    else:
                        if regex.match(r'^\[\s*import\s*\]$', key.strip()):
                            self.i_dynamic_import +=1
                            tmp_value = value
                            value = self.json_path + CNameMangling.DYNAMICIMPORTED.value + value
                            out_dict[f"{key.strip()}_{self.i_dynamic_import}"] = value
                            self.l_dynamic_imports.append({tmp_value:value})
                        else:
                            out_dict[key] = value
                if '${' not in value:
                    if regex.match(r'^\[\s*import\s*\]_\d+$', key):
                        dynamic_ipmport_index = regex.search(r'_(\d+)$', key)[1]
                        tmp_value = next(iter(self.l_dynamic_imports[int(dynamic_ipmport_index)-1]))
                        self.l_dynamic_imports[int(dynamic_ipmport_index)-1][tmp_value] = value
                    currjson_path = self.json_path
                    abs_path_file = CString.NormalizePath(value, sReferencePathAbs = currjson_path)
                    self.recursive_level = self.recursive_level + 1     # increase recursive level
                    if not self.is_dynamic_import or not self.json_pre_check or self.current_node.value==abs_path_file:
                        import_path = self.current_node.get_path_to_root() # Get the import path from import_tree to check Cyclic import
                        if abs_path_file in import_path:
                            previous_import_1 = import_path[0]
                            previous_import_2 = import_path[-1]
                            for path in import_path:
                                if path == abs_path_file:
                                    break
                                previous_import_1 = path
                            if previous_import_1 == abs_path_file or previous_import_2 == abs_path_file:
                                error_msg = f"Cyclic import detection: The file '{abs_path_file}' imports itself."
                            else:
                                error_msg = f"Cyclic import detection: The file '{abs_path_file}' is imported by '{previous_import_1}' and by file '{previous_import_2}'."
                            raise Exception(error_msg)
                    json_obj_import = self.json_load(abs_path_file)
                    if not self.json_pre_check and self.current_node.parent is not None:
                        self.current_node = self.current_node.parent
                    for k, v in json_obj_import.items():
                        if regex.match(r'^\s*\[\s*import\s*\]\s*', k) and '${' in v:
                            self.is_dynamic_import = True
                            break
                    self.json_path = currjson_path
                    tmp_out_dict = copy.deepcopy(out_dict)
                    for k1, v1 in tmp_out_dict.items():
                        for k2, v2 in json_obj_import.items():
                            if k2 == k1:
                                del out_dict[k1]
                    del tmp_out_dict
                    out_dict.update(json_obj_import)
                    self.recursive_level = self.recursive_level - 1     # descrease recursive level
                    if len(self.handling_file) > 1:
                        self.handling_file.pop(-1)
            else:
                if not self.json_pre_check:
                    special_characters = r'$[]{}\''
                    tmp_out_dict = copy.deepcopy(out_dict)
                    for k1, v1 in tmp_out_dict.items():
                        check_dup_key = '' # Uses to track an absolute path of overwritten parameter in case it's duplicate to others.
                        key_pattern = regex.escape(k1)
                        pattern_2 = rf'\${{\s*[^{regex.escape(special_characters)}]*\.*{key_pattern}\s*}}$|\[\s*\'{key_pattern}\'\s*\]$'
                        check = False
                        if regex.search(pattern_2, key, regex.UNICODE):
                            dot_format_key = None
                            for check_key in self.key_ddict_coverted.keys():
                                if key == check_key:
                                    dot_format_key = self.key_ddict_coverted[key]
                            if dot_format_key==None:
                                dot_format_key = key
                            # Check and ignore duplicated keys handling at the top level of JSONP
                            if  not (k1 in self.json_check.keys() and dot_format_key in self.json_check.keys()) \
                                or CTextProcessor.multiple_replace(key, {"${":"", "}":""}) == CTextProcessor.multiple_replace(k1, {"${":"", "}":""}):
                                check = True
                                tmp_key = CTextProcessor.multiple_replace(key, {"${":"", "}":""})
                                items = []
                                if regex.search(rf'\[\'*[^{regex.escape(special_characters)}]+\'*\]', tmp_key, regex.UNICODE):
                                    try:
                                        root_key = regex.search(rf'^\s*([^{regex.escape(special_characters)}]+)\[\'*.+', tmp_key, regex.UNICODE)[1]
                                        items = regex.findall(rf'\[(\'*[^{regex.escape(special_characters)}]+\'*)\]', tmp_key, regex.UNICODE)
                                        items.insert(0, f"'{root_key}'")
                                    except:
                                        pass
                                str_exec = "self.json_check"
                                for item in items:
                                    str_exec = f"{str_exec}[{item}]"
                                    check_dup_key = f"{check_dup_key}[{item}]"
                                try:
                                    exec(f"dump_data = {str_exec}")
                                except:
                                    check = False
                                    pass
                                if check:
                                    key = k1
                        if k1 == key:
                            list_keys = list(out_dict.keys())
                            index = list_keys.index(key)
                            new_key = f"{key}{CNameMangling.DUPLICATEDKEY_01.value}{i}"
                            list_keys.insert(index, new_key)
                            tmp_dict = {}
                            for k in list_keys:
                                tmp_dict[k] = index if k==new_key else out_dict[k]
                            out_dict = tmp_dict
                            if check_dup_key!='':
                                check_element = f"{check_element}({check_dup_key})"    # Adds absolute path to the check element while
                            elif check:                                               # handling duplicate keys later
                                check_element = f"{check_element}(None)"    # Adds "(None)" in case no absolute path is detected in
                            if isinstance(out_dict[key], list):              # a duplicated key.
                                if CNameMangling.DUPLICATEDKEY_01.value not in str(out_dict[key][0]):
                                    tmp_value = [check_element, out_dict[key], value]
                                    del out_dict[key]
                                else:
                                    tmp_value = out_dict[key]
                                    tmp_value.append(value)
                                    del out_dict[key]
                            else:
                                tmp_value = [check_element, out_dict[key], value]
                                del out_dict[key]
                            if check_element!=tmp_value[0]:
                                tmp_value[0] = check_element
                            value = tmp_value
                            out_dict[key] = value
                    del tmp_out_dict
                out_dict[key] = value
            i+=1
        return out_dict

    def __check_param_name(self, input: str) -> str:
        """
Checks a parameter name, in case the name is conflict with Python keywords, the temporary prefix
will be added to avoid any potential issues. This temporary prefix is removed when updating returned
Json object.

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``input``

  / *Type*: str /
        """
        pattern = r'\${\s*([^\[]+)\s*}'
        list_params = regex.findall(pattern, input, regex.UNICODE)
        for param in list_params:
            if "." not in param and param in self.list_datatypes:
                input = regex.sub(param, CNameMangling.AVOIDDATATYPE.value + param, input, count=1)
            if "." in param and CNameMangling.AVOIDDATATYPE.value + param.split('.')[0] in self.jp_globals.keys():
                input = regex.sub(param, CNameMangling.AVOIDDATATYPE.value + param, input, count=1)
        return input
    
    def __parse_dict_path(self, input : str) -> list:
        """
Parse a dictionary path string into a list of its components.

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

  The dictionary path string in the format "dictobj['element1']['element2']['element3']".

**Returns:**

* ``output``

  / *Type*: list /

  A list containing the dictionary object and its successive elements.
        """
        output = []
        special_characters = r'$[]{}'
        if not regex.search(r"\[.+\]", input):
            output.append(input)
        elif regex.match(r"^\[[^\[]+\]$", input):
            output.append(regex.sub(r"^\[\s*([^\[]+)\s*\]", "\\1", input))
        else:
            if not regex.match(r'^\s*\[.+$', input):
                index = input.index("[")
                output.append(input[:index])
            elements = regex.findall(rf"\[\s*('*[^{regex.escape(special_characters)}]+'*)\s*\]", input)
            for element in elements:
                output.append(element)
        return output

    def __nested_param_handler(self, input_str : str, is_key = False, convert_to_str = False):
        """
This method handles nested variables in parameter names or values. Variable syntax is ${Variable_Name}.

**Arguments:**

* ``input_str``

  / *Condition*: required / *Type*: str /

  Parameter name or value which contains a nested variable.

**Returns:**

  List of resolved variables which contains in the ``input_str``.
        """
        def __get_nested_value(nested_param : str):
            parameter = CTextProcessor.multiple_replace(nested_param, {"$${":"", "}":""})
            list_elements = self.__parse_dict_path(parameter)
            str_exec = "value = self.jp_globals"
            tmp_obj = self.jp_globals
            i=0
            for element in list_elements:
                is_list = False
                if regex.match(r"^[\s\-\+:]*\d+$", element):
                    is_list = True
                    tmp_exec = str_exec
                    str_exec = f"{tmp_exec}[{element}]"
                    try:
                        exec(str_exec)
                    except:
                        if i==0: # Handle cases one digit key name
                            str_exec = f"{tmp_exec}['{element}']"
                        pass
                elif regex.match(r"^'[^']+'$", element.strip()):
                    element = element.strip("'")
                if not is_list:
                    if isinstance(tmp_obj, dict) and element not in tmp_obj.keys():
                        duplicated_check = element + CNameMangling.DUPLICATEDKEY_01.value
                        for key in tmp_obj.keys():
                            if duplicated_check in key and CNameMangling.DUPLICATEDKEY_00.value not in key:
                                element = key                            
                    str_exec = f"{str_exec}['{element}']"
                if not is_list and isinstance(tmp_obj, dict):
                    if element in tmp_obj and (isinstance(tmp_obj[element], dict) or \
                                               isinstance(tmp_obj[element], list)):
                        tmp_obj = tmp_obj[element]
                elif is_list and isinstance(tmp_obj, list) and regex.match(r'^[\s\d]+$', element):
                    if int(element)<len(tmp_obj) and (isinstance(tmp_obj[int(element)], dict) or \
                                                      isinstance(tmp_obj[int(element)], list)):
                        tmp_obj = tmp_obj[int(element)]
                i+=1
            try:
                ldict = {}
                exec(str_exec, locals(), ldict)
                if py_builtIn:
                    tmp_value = str_exec.replace('value = ', '')
                else:
                    tmp_value = ldict['value']
            except Exception as error:
                if self.json_pre_check:
                    nested_param = self.__remove_token_str(nested_param)
                    tmp_value = nested_param.replace('$${', '${')
                    pass
                else:
                    self.__reset()
                    nested_param = self.__remove_token_str(nested_param)
                    error_msg = ''
                    for error_type in self.python_type_error:
                        if error_type in str(error):
                            error_msg = f"Could not resolve expression '{nested_param.replace('$${', '${')}'."
                    if error_msg != '':
                        error_msg = f"{error_msg} Reason: {error}" if ' or slices' not in str(error) else \
                                    f"{error_msg} Reason: {str(error).replace(' or slices', '')}"
                    else:
                        if isinstance(error, KeyError) and regex.search(r"\[\s*" + str(error) + r"\s*\]", nested_param):
                            error_msg = f"Could not resolve expression '{nested_param.replace('$${', '${')}'. \
Reason: Key error {error}"
                        else:
                            error_msg = f"The parameter '{nested_param.replace('$${', '${')}' is not available!"
                    raise Exception(error_msg)
            return tmp_value
        
        py_builtIn = False
        if regex.search(self.py_call_pattern, input_str):
            py_builtIn = True
        special_characters = r'[]{}'
        pattern = rf'\$\${{\s*[^{regex.escape(special_characters)}]+\s*}}'
        refer_vars = regex.findall(f"({pattern})", input_str, regex.UNICODE)
        # Resolve dotdict in input_str
        for var in refer_vars:
            if var not in input_str:
                continue
            if regex.search(r'\${.+\..+}', var):
                str_var = self.__handle_dot_in_nested_param(var)
                input_str = input_str.replace(var, str_var)
        tmp_pattern = rf'{pattern}(\[\s*\d+\s*\]|\[\s*\'[^{regex.escape(special_characters)}]+\'\s*\])*'
        nested_param = self.__remove_token_str(input_str.replace("$${", "${"))
        for key in self.key_ddict_coverted.keys():
            if nested_param == key:
                nested_param = self.key_ddict_coverted[key]
                break
        if regex.search(r'\${.+\..+}', input_str) and not convert_to_str:
            input_str = self.__handle_dot_in_nested_param(input_str)
        while regex.search(tmp_pattern, input_str, regex.UNICODE) and input_str.count("$${")>1:
            loop_check = input_str
            refer_vars = regex.findall(rf'({tmp_pattern})[^\[]', input_str, regex.UNICODE)
            if len(refer_vars)==0:
                refer_vars = regex.findall(rf'({tmp_pattern})$', input_str, regex.UNICODE)
            for var in refer_vars:
                str_var = self.__handle_dot_in_nested_param(var[0]) if regex.search(r'\${.+\..+}', var[0]) else var[0]
                tmp_value = __get_nested_value(str_var)
                if self.json_pre_check:
                    if "${" in tmp_value and convert_to_str:
                        tmp_value = tmp_value + CNameMangling.STRINGCONVERT.value
                if (isinstance(tmp_value, list) or isinstance(tmp_value, dict)) and convert_to_str and not py_builtIn:
                    self.__reset()
                    str_var = self.__remove_token_str(str_var)
                    raise Exception(f"The substitution of parameter '{str_var.replace('$${', '${')}' inside the string \
value '{nested_param}' is not allowed! Composite data types like lists and dictionaries cannot be substituted inside strings.")
                while var[0] in input_str:
                    loop_check_1 = input_str
                    var_pattern = regex.escape(var[0])
                    if regex.search(rf"\[['\s]*{var_pattern}['\s]*\]", input_str):
                        if regex.search(rf"\[\s*'\s*{var_pattern}\s*'\s*\]", input_str):
                            if (isinstance(tmp_value, list) or isinstance(tmp_value, dict)):
                                self.__reset()
                                str_var = self.__remove_token_str(str_var)
                                raise Exception(f"The substitution of parameter '{str_var.replace('$${', '${')}' inside \
the expression '{nested_param}' is not allowed! Composite data types like lists and dictionaries cannot be substituted as strings.")
                            input_str = regex.sub(rf"\[\s*'\s*{var_pattern}\s*'\s*\]", f"['{tmp_value}']", input_str)
                        elif isinstance(tmp_value, str):
                            input_str = regex.sub(rf"\[['\s]*{var_pattern}['\s]*\]", f"['{tmp_value}']", input_str)
                        elif isinstance(tmp_value, int):
                            input_str = regex.sub(rf"\[['\s]*{var_pattern}['\s]*\]", f"[{tmp_value}]", input_str)
                        else:
                            var = var[0].replace("$${", "${")
                            parent_param = regex.search(rf'^\s*(.+)\[[\s\']*{var_pattern}.*$', input_str)[1]
                            parent_value = None
                            var = self.__remove_token_str(var)
                            try:
                                parent_value = __get_nested_value(parent_param)
                            except Exception as error:
                                error_msg = f"{error} Could not resolve expression '{nested_param}'."
                                pass
                            if parent_value is not None:
                                if isinstance(parent_value, list):
                                    error_msg = f"Invalid list index in expression '{nested_param}'. The datatype of parameter \
'{var}' has to be 'int'."
                                elif isinstance(parent_value, dict):
                                    error_msg = f"Invalid dictionary key in expression '{nested_param}'. The datatype of parameter \
'{var}' has to be 'str'."
                                else:
                                    try:
                                        dummy_value = __get_nested_value(input_str)
                                    except Exception as error:
                                        error_msg = str(error)
                                        pass
                            self.__reset()
                            raise Exception(error_msg)
                    else:
                        if convert_to_str or input_str.count("$${")>1:
                            input_str = input_str.replace(var[0], str(tmp_value))
                        elif "$${" not in input_str:
                            return tmp_value
                    if input_str==loop_check_1:
                        if input_str.count("$${")==1:
                            break
                        self.__reset()
                        raise Exception(f"Invalid expression found: '{nested_param}'.")
                    elif regex.search(r"\[\s*\+*\-+\+*\d+\s*\]", input_str):
                        error_msg = f"Slicing is not supported (expression: '{nested_param}')."
                        self.__reset()
                        raise Exception(error_msg)
            if input_str==loop_check:
                self.__check_nested_param(input_str)
                self.__reset()
                raise Exception(f"Invalid expression found: '{nested_param}'.")
        if input_str.count("$${")==1:
            tmp_pattern = pattern + rf'(\[\s*\-*\d+\s*\]|\[[\s\']*[^{regex.escape(special_characters)}]+[\'\s]*\])*'
            if regex.match(f"^{tmp_pattern}$", input_str.strip(), regex.UNICODE) and is_key and not convert_to_str:
                root_var = regex.search(pattern, input_str, regex.UNICODE)[0]
                str_root_var = self.__handle_dot_in_nested_param(root_var) if regex.search(r'\${.+\..+}', root_var) else root_var
                input_str = input_str.replace(root_var, str_root_var)
                return CTextProcessor.multiple_replace(input_str, {"$${":"", "}":""})
            var = regex.search(tmp_pattern, input_str, regex.UNICODE)
            if var==None:
                str_var = self.__handle_dot_in_nested_param(input_str) if regex.search(r'\${.+\..+}', input_str) else input_str
                str_var = regex.sub(r'^\s*\$\${\s*([^}]+)}', "['\\1']", str_var)
                str_exec = "value = self.jp_globals" + str_var
                try:
                    ldict = {}
                    exec(str_exec, locals(), ldict)
                    tmp_value = ldict['value']
                except Exception as error:
                    if self.json_pre_check:
                        nested_param = self.__remove_token_str(nested_param)
                        tmp_value = nested_param.replace('$${', '${')
                        pass
                    else:
                        self.__reset()
                        error_msg = ''
                        for error_type in self.python_type_error:
                            if error_type in str(error):
                                error_msg = f"Could not resolve expression '{nested_param.replace('$${', '${')}'."
                        if error_msg != '':
                            error_msg = f"{error_msg} Reason: {error}"
                        else:
                            error_msg = f"The parameter '{nested_param.replace('$${', '${')}' is not available!"
                        raise Exception(error_msg)
                return tmp_value
            else:
                root_var = regex.search(pattern, var[0], regex.UNICODE)[0]
                str_root_var = self.__handle_dot_in_nested_param(root_var) if regex.search(r'\${.+\..+}', root_var) else root_var
                str_var = var[0].replace(root_var, str_root_var)
            tmp_value = __get_nested_value(str_var)
            if convert_to_str and (isinstance(tmp_value, list) or isinstance(tmp_value, dict)):
                datatype = regex.sub(r"^.+'([\p{L}]+)'.*$", "\\1", str(type(tmp_value)))
                self.__reset()
                str_var = self.__remove_token_str(str_var)
                raise Exception(f"The substitution of parameter '{str_var.replace('$${', '${')}' inside the string \
value '{nested_param}' is not allowed! Composite data types like lists and dictionaries cannot be substituted inside strings.")
            if regex.match(rf"^\s*{tmp_pattern}\s*$", input_str, regex.UNICODE) and not is_key:
                return tmp_value
            else:
                input_str = input_str.replace(var[0], str(tmp_value))
        return input_str.replace("$${", "${") if "$${" in input_str else input_str

    def __handle_dotdict_format(self, input_list_params : list, list_params: list = []) -> list:
        """
This method checks the availability of param names contained "." in dotdict format element in JSON config file.

**Arguments:**

* ``input_list_params``

  / *Condition*: required / *Type*: list /

  List of items separated by "." of dotdict format.

* ``list_params``

  / *Type*: list /

  List of parameter names in dotdict format.

**Returns:**

* ``list_params``

  / *Type*: list /
        """
        check_param = input_list_params[0]
        i = 0
        dotdict_param = False
        for item in input_list_params:
            if i > 0:
                check_param = f"{check_param}.{item}"
                if check_param in self.dot_in_param_name:
                    list_params.append(check_param)
                    dotdict_param = True
                    input_list_params = input_list_params[i+1:]
                    break
            i+=1
        if not dotdict_param:
            list_params.append(input_list_params[0])
            input_list_params.pop(0)
        if input_list_params == []:
            return list_params
        else:
            return self.__handle_dotdict_format(input_list_params, list_params)
        
    def __handle_dot_in_nested_param(self, nested_param : str) -> str:
        '''
This method handles the dot format in the parameter, then returns the traditional format with square brackets.

**Arguments:**

* ``nested_param``

  / *Condition*: required / *Type*: str /

  The parameter is formatted by "." of dotdict format.

**Returns:**

* ``str_var``

  / *Type*: str /

  The parameter is in traditional format with square brackets.
        '''
        is_modified = True
        if '$${' not in nested_param:
            is_modified = False
            nested_param = nested_param.replace('${', '$${')
        while nested_param.count('.$${') > 1:
            tmp_param = regex.search(r'\$\${[^\$]+\.\$\${[^\.\$}]*}(\[.*\])*}(\[.*\])*', nested_param)
            if tmp_param is None or tmp_param[0]==nested_param :
                break
            tmp_param = tmp_param[0]
            handle_tmp_param = self.__handle_dot_in_nested_param(tmp_param)
            nested_param = nested_param.replace(tmp_param, handle_tmp_param)
        root_param = ''
        str_index = ''
        if regex.search(r'\[.*\]\s*$', nested_param):
            root_param = regex.search(r'(^[^\[]+)', nested_param)[0]
            str_index = nested_param.replace(root_param, '')
        if root_param == '':
            root_param = nested_param
        dd_var = regex.sub(r'^\s*\$\${\s*(.*?)\s*}\s*$', '\\1', root_param, regex.UNICODE)
        ldd_var = dd_var.split(".")
        list_elements = self.__handle_dotdict_format(ldd_var, [])
        str_var = f'$${{{list_elements[0]}}}'
        str_exec = f"dummy_data = self.jp_globals['{list_elements.pop(0)}']"
        for item in list_elements:
            if regex.match(r'^\d+$', item):
                str_exec = f"{str_exec}[{item}]"
                if not self.json_pre_check:
                    try:
                        exec(str_exec)
                        str_var = f"{str_var}[{item}]"
                    except:
                        str_exec = regex.sub(r'^.+\[(\d+)\]$', "'\\1'", str_exec)
                        str_var = f"{str_var}['{item}']"
                else:
                    str_var = f"{str_var}[{item}]"
            elif (regex.search(r'[{}\[\]\(\)]+', item) and "${" not in item) or \
                regex.match(r'^\s*\$\${.+}(\[[^\[]*\])*\s*$', item):
                str_exec = f"{str_exec}[{item}]"
                str_var = f"{str_var}[{item}]"
            else:
                str_exec = f"{str_exec}['{item}']"
                str_var = f"{str_var}['{item}']"
        if str_index != '':
            str_var = str_var + str_index
        return str_var if is_modified else str_var.replace('$${', '${')

    def __check_and_create_new_element(self, str_key: str, value, json_obj=None, check=False, key_nested=None):
        """
This method checks and creates new elements if they are not already existing.
        """
        list_elements = self.__parse_dict_path(str_key)
        if len(list_elements) == 1:
            return True
        else:
            str_exec_1 = "dummy_data = self.jp_globals"
            if json_obj is not None:
                str_exec_2 = "dummy_data = json_obj"
            for element in list_elements:
                if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                    if json_obj is not None:
                        if '[' in str_exec_2:
                            str_exec_2 = f"{str_exec_2}[{element}]"
                        elif element.strip("'") in list(json_obj.keys()):
                            str_exec_2 = f"{str_exec_2}[{element}]"
                    str_exec_1 = f"{str_exec_1}[{element}]"
                else:
                    if json_obj is not None:
                        if '[' in str_exec_2:
                            str_exec_2 = f"{str_exec_2}['{element}']"
                        elif element.strip("'") in list(json_obj.keys()):
                            str_exec_2 = f"{str_exec_2}['{element}']"
                    str_exec_1 = f"{str_exec_1}['{element}']"
                try:
                    exec(str_exec_1)
                    if json_obj is not None:
                        exec(str_exec_2)
                except Exception as error:
                    if key_nested is not None:
                        tmp_nested_key = None
                        for key in self.key_ddict_coverted.keys():
                            if key == self.__remove_token_str(key_nested):
                                tmp_nested_key = self.key_ddict_coverted[key]
                        if tmp_nested_key == None:
                            tmp_nested_key = self.__remove_token_str(key_nested)
                    if isinstance(error, TypeError): # If Python's type errors occur when executing an expression
                        for eType in self.python_type_error:
                            if eType in str(error):
                                if key_nested is not None:
                                    error_msg = f"Could not set parameter '{tmp_nested_key}' with value '{value}'! \
Reason: {str(error).replace(' or slices', '')}"
                                else:
                                    error_msg = f"Could not set parameter '{self.__remove_token_str(str_key)}' with value '{value}'! \
Reason: {str(error).replace(' or slices', '')}"
                                self.__reset()
                                raise Exception(error_msg)
                    if check:
                        return False
                    else: # if check flag is False, this function will create a new data structure with default value is empty dict.
                        if json_obj is not None:
                            index = str_exec_2.index("=")
                            str_exec_21 = str_exec_2[index+1:].strip() + " = {}"
                        index = str_exec_1.index("=")
                        str_exec_11 = str_exec_1[index+1:].strip() + " = {}"
                        try:
                            exec(str_exec_11)
                            if json_obj is not None:
                                exec(str_exec_21)
                        except Exception as error:
                            self.__reset()
                            if key_nested is not None:
                                str_key = tmp_nested_key if tmp_nested_key is not None else self.__remove_token_str(key_nested)
                            error_msg = f"Could not set parameter '{str_key}' with value '{value}'! Reason: {error}"
                            raise Exception(error_msg)
            return True

    def __update_and_replace_nested_param(self, json_obj : dict, is_nested : bool = False, recursive : bool = False, \
                                      parent_params : str = '', dict_in_list : bool = False):
        """
This method replaces all nested parameters in key and value of a JSON object .

**Arguments:**

* ``json_obj``

  / *Condition*: required / *Type*: dict /

  Input JSON object as dictionary. This dictionary will be searched for all ``${variable}`` occurences.
  If found it will be replaced with it's current value.

**Returns:**

* ``json_objOut``

  / *Type*: dict /

  Output JSON object as dictionary with all variables resolved.
        """
        def __json_updated(k, v, json_obj, parent_params, key_nested, param_value, duplicated_handle, recursive):
            if param_value is not None:
                list_elements = self.__parse_dict_path(param_value)
                str_exec_value_1 = "self.jp_globals"
                for element in list_elements:
                    if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                        str_exec_value_1 = f"{str_exec_value_1}[{element}]"
                    else:
                        str_exec_value_1 = f"{str_exec_value_1}['{element}']"
                pattern_parent_param = regex.escape(parent_params)
                if regex.match(rf"^{pattern_parent_param}.*$", param_in_value) and \
                    (f"{parent_params}['{k}']" != param_value):
                    str_exec_value_2 = "json_obj"
                    param_value_2 = param_value.replace(parent_params, '')
                    list_elements = self.__parse_dict_path(param_value_2)
                    for element in list_elements:
                        if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                            str_exec_value_2 = f"{str_exec_value_2}[{element}]"
                        else:
                            str_exec_value_2 = f"{str_exec_value_2}['{element}']"
                else:
                    str_exec_value_2 = str_exec_value_1
                if regex.search(r'\[[^\[]+\]', k):
                    list_elements = self.__parse_dict_path(k)
                elif parent_params != '':
                    str_params = f"{parent_params}['{k}']"
                    list_elements = self.__parse_dict_path(str_params)
                else:
                    list_elements = [k]
                str_execKey = "self.jp_globals"
                for element in list_elements:
                    if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                        str_execKey = f"{str_execKey}[{element}]"
                    else:
                        str_execKey= f"{str_execKey}['{element}']"
            if key_nested is not None:
                if not duplicated_handle and key_nested in json_obj.keys():
                    del json_obj[key_nested]
                root_key = regex.sub(r'\[.*\]', "", k, regex.UNICODE)
                if regex.search(r'^[\p{Nd}]+.*$', root_key, regex.UNICODE):
                    json_obj[f"{root_key}"] = {}
                elif root_key not in self.jp_globals.keys():
                    json_obj[root_key] = {}
                    str_exec = f"self.jp_globals['{root_key}'] = {{}}"
                    try:
                        exec(str_exec)
                    except Exception as error:
                        raise Exception(f"Could not set root key element '{root_key}'! Reason: {error}")
                if regex.match(rf"^[^\[]+\[.+\]+$", k, regex.UNICODE):
                    self.__check_and_create_new_element(k, v, json_obj=json_obj, key_nested=key_nested)
                    if CNameMangling.AVOIDDATATYPE.value in k:
                        k = regex.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                    list_elements = self.__parse_dict_path(k)
                    str_exec_key_1 = "self.jp_globals"
                    for element in list_elements:
                        if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                            str_exec_key_1 = f"{str_exec_key_1}[{element}]"
                        else:
                            str_exec_key_1 = f"{str_exec_key_1}['{element}']"
                    if param_value is None:
                        str_exec_1 = f"{str_exec_key_1} = \"{v}\"" if isinstance(v, str) else f"{str_exec_key_1} = {str(v)}"
                    else:
                        str_exec_1 = f"{str_exec_key_1} = {str_exec_value_1}"
                    try:
                        exec(str_exec_1)
                    except Exception as error:
                        self.__reset()
                        error_msg = f"Could not set parameter '{self.__remove_token_str(key_nested)}' with value '{v}'! Reason: {error}"
                        raise Exception(error_msg)
                    if parent_params != '':
                        json_param = regex.sub(rf'^{regex.escape(parent_params)}(.+)$', '\\1', k)
                        json_param = regex.sub(r'^\[([^\[]+)\].*$', '\\1', json_param)
                        tmp_parent_params = regex.sub(r'^([^\[]+)', '[\'\\1\']', parent_params)
                        str_exec = f"json_obj[{json_param}] = self.jp_globals{tmp_parent_params}[{json_param}]"
                        try:
                            exec(str_exec)
                        except Exception as error:
                            raise Exception(f"Could not set root key element '{parent_params}[{json_param}]'! Reason: {error}")
                    if not recursive:
                        json_obj[root_key] = self.jp_globals[root_key]
            else:
                if CNameMangling.AVOIDDATATYPE.value in k:
                    k = regex.sub(CNameMangling.AVOIDDATATYPE.value, "", k)
                if param_value is None:
                    json_obj[k] = v
                    if parent_params == '':
                        self.jp_globals[k] = v
                    else:
                        tmp_parent_params = regex.sub(r'^([^\[]+)', '[\'\\1\']', parent_params)
                        str_exec = f"self.jp_globals{tmp_parent_params}['{k}'] = {v}" if not isinstance(v, str) else \
                                f"self.jp_globals{tmp_parent_params}['{k}'] = \"{v}\""
                        try:
                            exec(str_exec)
                        except:
                            pass
                else:
                    str_exec_1 = f"{str_execKey} = {str_exec_value_1}"
                    str_exec_2 = f"json_obj['{k}'] = {str_exec_value_2}"
                    try:
                        exec(str_exec_1)
                        exec(str_exec_2)
                    except Exception as error:
                        self.__reset()
                        error_msg = f"Could not set parameter '{self.__remove_token_str(k)}'! Reason: {error}"
                        raise Exception(error_msg)
                if not recursive:
                    self.jp_globals.update({k:v})
            param_value = None

        def __load_nested_value(init_value: str, input_str: str, is_key=False, key=''):
            index_pattern = r"\[[\s\-\+\d]*\]"
            dict_pattern = rf"(\[+\s*'[^\$\[\]\(\)]+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${{\s*[^\[]*\s*}}.*\]+)*|{index_pattern}"
            pattern = rf"\${{\s*[^\[}}\$]*(\.*\${{\s*[\[]*\s*}})*}}*{dict_pattern}"
            is_value_convert_str = False
            if CNameMangling.STRINGCONVERT.value in input_str or regex.match(r'^\[\s*import\s*\]_\d+$', key):
                is_value_convert_str = True
                input_str = input_str.replace(CNameMangling.STRINGCONVERT.value, '')
                input_str = input_str.replace('${', '$${')
                init_value = init_value.replace(CNameMangling.STRINGCONVERT.value, '')
            elif regex.match(rf"^\s*{pattern}\s*$", input_str, regex.UNICODE):
                input_str = input_str.replace('${', '$${')
            input_str = self.__check_param_name(input_str)
            handled_value = self.__nested_param_handler(input_str) if not is_value_convert_str else \
                                    self.__nested_param_handler(input_str, is_key=is_key, convert_to_str=is_value_convert_str)
            if is_value_convert_str and not isinstance(handled_value, str):
                handled_value = str(handled_value)
            return handled_value

        def __handle_list(list_input : list, is_nested : bool, parent_params : str = '') -> list:
            tmp_value = []
            i=0
            for item in list_input:
                if isinstance(item, str) and regex.search(rf'{self.py_call_pattern}', item):
                    raise Exception(f"Python inline code must not be a part of a list! Please check \
the expression '{self.__remove_token_str(item)}'")
                parent_params = f"{parent_params}[{i}]"
                # Handle byte value in JSONP by un-mark the token string
                if isinstance(item, str) and CNameMangling.BYTEVALUE.value in item:
                    item = ast.literal_eval(self.byte_value[item])
                elif isinstance(item, str) and regex.search(pattern, item, regex.UNICODE):
                    is_nested = True
                    init_item = item
                    while isinstance(item, str) and "${" in item:
                        loop_check = item
                        item = __load_nested_value(init_item, item)
                        if item==loop_check:
                            self.__reset()
                            raise Exception(f"Invalid expression found: '{self.__remove_token_str(init_item)}'.")
                elif isinstance(item, list) and "${" in str(item):
                    item = __handle_list(item, is_nested, parent_params)
                elif isinstance(item, dict):
                    item, is_nested = self.__update_and_replace_nested_param(item, is_nested, recursive=True, parent_params=parent_params, dict_in_list=True)
                tmp_value.append(item)
                parent_params = regex.sub(r'\[\d+\]$', '', parent_params)
                i+=1
            return tmp_value

        if bool(self.current_cfg) and not recursive:
            tmp_dict = copy.deepcopy(self.current_cfg)
            for k, v in tmp_dict.items():
                if k in self.list_datatypes:
                    old_key = k
                    k = CNameMangling.AVOIDDATATYPE.value + k
                    self.__change_dict_key(self.current_cfg, old_key, k)
                self.jp_globals.update({k:v})
            del tmp_dict
            json_obj = self.current_cfg | json_obj

        tmp_json = copy.deepcopy(json_obj)
        pattern = r"\${\s*[^\[]+\s*}"
        pattern = rf"{pattern}(\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${{.+\s*\]+)*"
        for k, v in tmp_json.items():
            if "${" not in k and CNameMangling.DUPLICATEDKEY_01.value not in k:
                parent_params = k if parent_params=='' else f"{parent_params}['{k}']"
            key_nested = None
            orig_key = ''
            is_str_convert = False
            is_implicit_creation = False
            duplicated_handle = False
            if regex.match(rf"^.+{CNameMangling.DUPLICATEDKEY_01.value}\d+$", k, regex.UNICODE):
                duplicated_handle = True
                dup_key = k
                if CNameMangling.DUPLICATEDKEY_00.value in k:
                    orig_key = regex.sub(rf"{CNameMangling.DUPLICATEDKEY_01.value}\d+$", "", k)
                    if not regex.match(rf'^\s*{pattern}\s*$', orig_key):
                        json_obj = self.__change_dict_key(json_obj, k, orig_key)
                    else:
                        del json_obj[k]
                    k = orig_key
                else:
                    del json_obj[k]
                    k = regex.sub(rf"{CNameMangling.DUPLICATEDKEY_01.value}\d+$", "", k)
            if CNameMangling.STRINGCONVERT.value in k:
                if '\\' in k:
                    k = repr(k).strip("'")
                is_str_convert = True
                del json_obj[k]
                key_nested = k.replace(CNameMangling.STRINGCONVERT.value, '')
                json_obj[key_nested] = v
                is_nested = True
                while "${" in k:
                    loop_check = k
                    k = __load_nested_value(key_nested, k, is_key=True, key=key_nested)
                    if k == loop_check:
                        self.__reset()
                        raise Exception(f"Invalid expression found: '{self.__remove_token_str(key_nested)}'.")
            elif regex.match(rf"^\s*{pattern}\s*$", k, regex.UNICODE):
                if '\\' in k:
                    k = repr(k).strip("'")
                check_dynamic_key = False
                key_nested = k
                if k.count("${")>1 and regex.match(rf'^\s*"*\s*{pattern}\s*"*\s*$', k, regex.UNICODE):
                    check_dynamic_key = True
                if regex.search(rf"\[\s*'*{pattern}'*\s*\]", key_nested, regex.UNICODE) or \
                    regex.search(rf"\.{pattern}[\.}}]+", key_nested, regex.UNICODE):
                    is_implicit_creation = True
                k = k.replace('${', '$${')
                k = self.__check_param_name(k)
                k = self.__nested_param_handler(k, is_key=True)
                str_exec = 'dummy_data = self.jp_globals'
                # Check digits inside a square brackets indicating a key name of a dict or index of a list
                while regex.search(r'\[\d+\]', k):
                    tmpK = regex.sub(r'\[\d+\].*$', '', k)
                    tmpK = regex.sub(r'_listIndex_', '', tmpK)
                    tmp_exec = str_exec + regex.sub(r'^\s*([^\[]+)', "['\\1']", parent_params) + \
                                    regex.sub(r'^\s*([^\[]+)', "['\\1']", tmpK)
                    try:
                        ldict = {}
                        exec(tmp_exec, locals(), ldict)
                    except:
                        pass
                    if len(ldict)>0 and isinstance(ldict['dummy_data'], dict):
                        k = regex.sub(r'\[(\d+)\]', "['\\1']", k, count=1) # if it a key name, put inside single quotes
                    else:
                        k = regex.sub(r'\[(\d+)\]', "[\\1_listIndex_]", k, count=1) # add temporary suffix to the index due to while condition
                if '_listIndex_' in k:
                    k = regex.sub(r'_listIndex_', '', k)
                tmp_pattern = regex.escape(parent_params)
                if (parent_params != '' and not regex.match(rf'^{tmp_pattern}.+$', k)) or dict_in_list:
                    tmpParam = regex.sub(r'^\s*([^\[]+)', "${\\1}", parent_params) + regex.sub(r'^\s*([^\[]+)', "['\\1']", k)
                    str_exec = str_exec + regex.sub(r'^\s*([^\[]+)', "['\\1']", parent_params) + \
                                    regex.sub(r'^\s*([^\[]+)\[*.*$', "['\\1']", k)
                    k = parent_params + regex.sub(r'^\s*([^\[]+)', "['\\1']", k) # Update absolute path of nested key
                    try:
                        exec(str_exec)
                    except:
                        key_nested = self.__remove_token_str(key_nested)
                        for key in self.key_ddict_coverted.keys():
                            if key_nested == key:
                                key_nested = self.key_ddict_coverted[key]
                                break
                        self.__reset()
                        raise Exception(f"A key with name '{key_nested}' does not exist at this position. \
Use the '<name> : <value>' syntax to create a new key.")
                elif check_dynamic_key:
                    str_exec = str_exec + regex.sub(r'^\s*([^\[]+)', "['\\1']", parent_params) + \
                                    regex.sub(r'^\s*([^\[]+)', "['\\1']", k)
                    try:
                        exec(str_exec)
                    except Exception as error:
                        if isinstance(error, KeyError):
                            key_nested = self.__remove_token_str(key_nested)
                            for key in self.key_ddict_coverted.keys():
                                if key_nested==key:
                                    key_nested = self.key_ddict_coverted[key]
                                    break
                            self.__reset()
                            raise Exception(f"Identified dynamic name of key '{key_nested}' that does not exist. \
But new keys can only be created based on hard code names.")
                        else:
                            pass
                elif parent_params == '' and not regex.search(r'\[[^\]]+\]', k):
                    str_exec = f"{str_exec}['{k}']"
                    try:
                        exec(str_exec)
                    except Exception as error:
                        if isinstance(error, KeyError):
                            raise Exception(f"Could not resolve expression '${{{k}}}'. The based parameter '{k}' is not defined yet! \
Use the '<name> : <value>' syntax to create a new based parameter.")
                        else:
                            raise Exception(f"Could not resolve expression '${{{k}}}'. Reason: {error}")
                if is_implicit_creation and not self.__check_and_create_new_element(k, v, check=True, key_nested=key_nested):
                    self.__reset()
                    raise Exception(f"The implicit creation of data structures based on parameters is not supported \
(affected expression: '{self.__remove_token_str(key_nested)}').")
            param_in_value = None
            if isinstance(v, dict):
                v, is_nested = self.__update_and_replace_nested_param(v, is_nested, recursive=True, parent_params=parent_params)
            elif isinstance(v, list):
                v = __handle_list(v, is_nested, parent_params)
            elif isinstance(v, str) and self.__check_nested_param(v):
                py_builtIn = False
                # Check and handle the Python builtIn in JSONP
                if regex.search(self.py_call_pattern, v):
                    py_builtIn = True
                    if '${' not in v:
                        try:
                            v = self.__py_builtIn_handle(v)
                        except Exception as error:
                            error_msg = f"Could not evaluate the Python builtIn {self.__remove_token_str(v)}. Reason: {str(error)}"
                            self.__reset()
                            raise Exception(error_msg)
                # Handle byte value in JSONP by un-mark the token string
                if isinstance(v, str) and CNameMangling.BYTEVALUE.value in v:
                    v = ast.literal_eval(self.byte_value[v])
                elif isinstance(v, str) and regex.search(pattern, v, regex.UNICODE):
                    if '\\' in v:
                        v = repr(v).strip("'|\"")
                    is_nested = True
                    init_value = v
                    while isinstance(v, str) and "${" in v:
                        loop_check = v
                        if v.count('${')==1 and CNameMangling.STRINGCONVERT.value not in v:
                            if regex.search(r'\${.+\..+}', v):
                                param_in_value = self.__handle_dot_in_nested_param(v)
                                param_in_value = CTextProcessor.multiple_replace(param_in_value, {'${':'', '}':''})
                        # Check datatype of [import] value 
                        if regex.match(r'^\[\s*import\s*\]_\d+$', k):
                            dynamic_imported = regex.search(rf'^(.*){CNameMangling.DYNAMICIMPORTED.value}(.*)$', v)
                            import_value = dynamic_imported[2]
                            import_value = __load_nested_value(import_value, import_value)
                            if not isinstance(import_value, str):
                                type_value = regex.search(r"^<class\s*('.+')>$", str(type(import_value)))
                                type_value = type_value[1] if type_value is not None else type(import_value)
                                error_msg = f"The [import] key requires a value of type 'str', but the type is {type_value}"
                                self.__reset()
                                raise Exception(error_msg)
                        v = __load_nested_value(init_value, v, key=k)
                        # Check and handle the Python builtIn in JSONP
                        if isinstance(v, str) and regex.search(self.py_call_pattern, v):
                            py_builtIn = True
                            try:
                                v = self.__py_builtIn_handle(v)
                            except Exception as error:
                                error_msg = f"Could not evaluate the Python builtIn {self.__remove_token_str(init_value)}. Reason: {str(error)}"
                                self.__reset()
                                raise Exception(error_msg)
                        # Handle dynamic import value
                        if regex.match(r'^\[\s*import\s*\]_\d+$', k):
                            if '${' not in v and CNameMangling.DYNAMICIMPORTED.value in v:
                                dynamic_imported = regex.search(rf'^(.*){CNameMangling.DYNAMICIMPORTED.value}(.*)$', v)
                                if regex.match(r'^[/|\\].+$', dynamic_imported[2]):
                                    v = dynamic_imported[2]
                                else:
                                    v = CString.NormalizePath(dynamic_imported[2], sReferencePathAbs = dynamic_imported[1])
                        if v == loop_check:
                            if not self.json_pre_check:
                                self.__reset()
                                raise Exception(f"Invalid expression found: '{self.__remove_token_str(init_value)}'.")
                            else:
                                break
                    if isinstance(v, str) and regex.search(r'\[[^\]]+\]', v) and not py_builtIn:
                        str_exec = 'value = ' + v
                        try:
                            ldict = {}
                            exec(str_exec, locals(), ldict)
                            v = ldict['value']
                        except:
                            pass
            if duplicated_handle:
                if "${" not in dup_key and parent_params != "":
                    str_params = f"{parent_params}['{k}']"
                    list_elements = self.__parse_dict_path(str_params)
                    str_exec = "self.jp_globals"
                    for element in list_elements:
                        if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                            str_exec = f"{str_exec}[{element}]"
                        else:
                            str_exec = f"{str_exec}['{element}']"
                    str_exec = f"{str_exec} = \"{v}\"" if isinstance(v, str) else f"{str_exec} = {str(v)}"
                else:
                    list_elements = self.__parse_dict_path(k)
                    str_exec = "self.jp_globals"
                    check_dict = self.jp_globals
                    for element in list_elements:
                        if (isinstance(check_dict, dict) or isinstance(check_dict, list)) and element.strip("'") not in check_dict:
                            check_dict[element.strip("'")] = {}
                        if regex.match(r"^[\s\-]*\d+$", element) or regex.match(r"^'[^']+'$", element.strip()):
                            str_exec = f"{str_exec}[{element}]"
                        else:
                            str_exec = f"{str_exec}['{element}']"
                        check_dict = check_dict[element.strip("'")]
                    str_exec = f"{str_exec} = \"{v}\"" if isinstance(v, str) else f"{str_exec} = {str(v)}"
                try:
                    exec(str_exec)
                except:
                    pass
                if orig_key == '':
                    continue
            key_pattern = regex.escape(k)
            if regex.match(rf"^.+\['{key_pattern}'\]$", parent_params, regex.UNICODE):
                parent_params = regex.sub(rf"\['{key_pattern}'\]", "", parent_params)
            elif not recursive:
                parent_params = ''
            __json_updated(k, v, json_obj, parent_params, key_nested, param_in_value, duplicated_handle, recursive)
            if key_nested is not None and not is_str_convert:
                trans_table = str.maketrans({"[":r"\[", "]":r"\]" })
                tmp_list = []
                for key in self.dUpdatedParams:
                    if regex.match(r"^" + k.translate(trans_table) + r"\['.+$", key, regex.UNICODE):
                        tmp_list.append(key)
                for item in tmp_list:
                    self.dUpdatedParams.pop(item)
                if CNameMangling.DUPLICATEDKEY_01.value not in k:
                    self.dUpdatedParams.update({k:v})
        del tmp_json
        return json_obj, is_nested

    def __check_dot_in_param_name(self, json_obj : dict):
        """
This is recrusive funtion collects all parameters which contain "." in the name.

**Arguments:**

* ``json_obj``

  / *Condition*: required / *Type*: dict /

  Json object which want to collect all parameter's name contained "."

**Returns:**

  *no return values*
        """
        for k, v in json_obj.items():
            if "." in k and k not in self.dot_in_param_name:
                self.dot_in_param_name.append(k)
            if isinstance(v, dict):
                self.__check_dot_in_param_name(v)

    def __check_nested_param(self, input : str, is_key=False) -> bool:
        """
Checks nested parameter format.

**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

**Returns:**

  *raise exception if nested parameter format invalid*
        """
        pattern = rf"^\${{\s*[^{regex.escape(self.special_characters)}]+\s*}}(\[.*\])+$"
        pattern_1 = r"\${[^\${]+}(\[[^\[]+\])*[^\[]*\${"
        pattern_2 = r"\[[\p{Nd}\.\-\+'\s]*:[\p{Nd}\.\-\+'\s]*\]|\[[\s\p{Nd}\+\-]*\${.+[}\]][\s\p{Nd}\+\-]*:[\s\p{Nd}\+\-]*\${.+[}\]][\s\p{Nd}\+\-]*\]|" # Slicing pattern
        pattern_2 = pattern_2 + r"\[[\s\p{Nd}\+\-]*\${.+[}\]][\s\p{Nd}\+\-]*:[\p{Nd}\.\-\+'\s]*\]|\[[\p{Nd}\.\-\+'\s]*:[\s\p{Nd}\+\-]*\${.+[}\]][\s\p{Nd}\+\-]*\]" # Slicing pattern
        if not is_key and regex.match(self.py_call_pattern, input):
            return True
        if CNameMangling.DYNAMICIMPORTED.value in input:
            dynamic_imported = regex.search(rf'^(.*){CNameMangling.DYNAMICIMPORTED.value}(.*)$', input)
            input = dynamic_imported[2]
        # Checks special character in parameters
        tmp_input = input
        special_char_in_param = False
        check_input = tmp_input
        while tmp_input.count("${") > 1:
            list_params = regex.findall(r'\${([^\$}]*)}', tmp_input)
            for param in list_params:
                if param.strip()=='' or regex.search(regex.escape(self.special_characters), param) or \
                                        regex.match(r'^\s*\-+.*\s*$', param) or regex.match(r'^\s*[^\-]*\-+\s*$', param):
                    special_char_in_param = True
                    break
                tmp_input = tmp_input.replace(f'${{{param}}}', '')
            if special_char_in_param or check_input==tmp_input:
                break
            check_input = tmp_input
        if "${" not in input:
            return True
        error_msg = None
        # Start checking nested parameter
        if regex.search(rf"\${{\s*[^{regex.escape(self.special_characters)}]+\['*.+'*\].*}}", input, regex.UNICODE):
            error_msg = f"Invalid syntax: Found index or sub-element inside curly brackets in \
the parameter '{self.__remove_token_str(input)}'"
        elif regex.search(r"\[[\p{Nd}\s]*[\p{L}_]+[\p{Nd}\s]*\]", input, regex.UNICODE):
            invalid_elem = regex.search(r"\[([\p{Nd}\s]*[\p{L}_]+[\p{Nd}\s]*)\]", input, regex.UNICODE)[1]
            error_msg = f"Invalid syntax! Sub-element '{invalid_elem}' in {self.__remove_token_str(input)} \
need to be referenced using ${{{invalid_elem}}} or enclosed in quotes ['{invalid_elem}']."
        elif regex.search(r'\[[!@#\$%\^&\*\(\)=\[\]|;\s\-\+\'",<>?/`~]*\]', input):
            if CNameMangling.STRINGCONVERT.value not in input or \
                regex.match(pattern, input.replace(CNameMangling.STRINGCONVERT.value, "")):
                error_msg = f"Expression '{self.__remove_token_str(input)}' cannot be evaluated. \
Reason: A pair of square brackets is empty or contains not allowed characters."
        elif special_char_in_param:
            if CNameMangling.STRINGCONVERT.value not in input:
                error_msg = f"Expression '{self.__remove_token_str(input)}' cannot be evaluated. \
Reason: A pair of curly brackets is empty or contains not allowed characters."
        elif regex.search(pattern_2, input) or regex.search(r"\[\s*\-\s*\d+\s*\]", input):
            error_msg = f"Slicing is not supported (expression: '{self.__remove_token_str(input)}')."
        elif input.count("${") > input.count("}") and (CNameMangling.STRINGCONVERT.value in input or \
                                                         regex.match(r"^[\s\"]*\${[^!@#%\^&\*\(\)=|;,<>?/`~]+[\s\"]*$", input)):
            error_msg = f"Invalid syntax! One or more than one closed curly bracket is missing in \
expression '{self.__remove_token_str(input.strip())}'."
        elif (not regex.match(r"^\${.+[}\]]+$", input) or (regex.search(pattern_1, input) and not is_key)) \
            and not self.json_pre_check:
            if CNameMangling.STRINGCONVERT.value not in input and CNameMangling.DUPLICATEDKEY_01.value not in input:
                tmp_input = regex.sub(r"(\.\${[\p{L}\p{Nd}\.\_]+}(\[[^\[]+\])*)", "", input)
                if not regex.match(r"^\s*\${[\p{L}\p{Nd}\.\_]+}(\[[^\[]+\])*\s*$", tmp_input):
                    error_msg = f"Invalid expression found: '{self.__remove_token_str(input)}' - The double quotes are missing!!!"
            elif CNameMangling.STRINGCONVERT.value in input:
                input = input.replace(CNameMangling.STRINGCONVERT.value, '')
                if regex.match(r'^\${[^}]+}+(\[.+\])*\s*$', input) and \
                    (input.count("${") != input.count("}") or input.count("[") != input.count("]")):
                    error_msg = f"Invalid expression found: '{self.__remove_token_str(input.strip())}' - The brackets mismatch!!!"                
        elif input.count("{") != input.count("}") or input.count("[") != input.count("]"):
            if CNameMangling.STRINGCONVERT.value not in input:
                error_msg = f"Invalid expression found: '{self.__remove_token_str(input.strip())}'"
                if input.count("${") != input.count("}") or input.count("[") != input.count("]"):
                    error_msg = f"{error_msg} - The brackets mismatch!!!"
        elif regex.search(r'\[[^\[]+\]', input) and is_key:
            invalid_format = []
            for item in regex.findall(r"\[[^\[]+'[^'\[]+'\s*\]", input):
                invalid_format.append(item)
            for item in regex.findall(r"\[\s*'[^'\[]+'[^\]]+\]", input):
                invalid_format.append(item)
            for item in regex.findall(r'\[[^\[]+\][^\[]+\[[^\[]+\]', input):
                invalid_format.append(item)
            if len(invalid_format) > 0:
                error_msg = 'Invalid syntax! Please check the sub-element syntax of'
                for item in invalid_format:
                    error_msg = f"{error_msg} {item},"
                error_msg = f"{error_msg.strip(',')} in the key {input}."
        # End checking nested parameter
        if error_msg is not None:
            self.__reset()
            raise Exception(error_msg)
        else:
            return True
        
    def __change_dict_key(self, dict_input : dict, old_key : str, new_key : str) -> dict:
        """
Replace an existing key in a dictionary with a new key name. The replacement is done by preserving the original order of the keys.

**Arguments:**

* ``dict_input``

  / *Condition*: required / *Type*: dict /

* ``old_key``

  / *Condition*: required / *Type*: str /

* ``new_key``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``dict_output``

  / *Type*: dict /
        """
        list_keys = list(dict_input.keys())
        index = list_keys.index(old_key)
        list_keys.insert(index, new_key)
        list_keys.pop(index + 1)
        dict_output = {}
        for key in list_keys:
            dict_output[key] = dict_input[old_key] if key==new_key else dict_input[key]
        return dict_output
    
    def __key_name_validation(self, key_name : str):
        """
Validates the key names of a JSON object to ensure they adhere to certain rules and conventions.

**Arguments:**

* ``key_name``

  / *Condition*: required / *Type*: str /

**Returns:**

  *No return value*
        """
        def __is_ascii(input : str) -> bool:
            try:
                input.encode('ascii')
                return True
            except UnicodeEncodeError:
                return False
        key_checker = CKeyChecker(self.key_pattern)
        error_msg = ''
        if regex.search(rf'["\s]*{self.py_call_pattern}["\s]*', key_name):
            error_msg = f"Python inline code is not allowed at the left hand side of the colon. Please check \
expression '{self.__remove_token_str(key_name)}'."
        elif CNameMangling.STRINGCONVERT.value in key_name:
            if regex.search(r'\[\s*"\s*\${[^"]+"\s*\]', key_name):
                key_name = self.__remove_token_str(key_name.strip('"'))
                key_name_suggestion_1 = regex.sub(r'(\[\s*")', '[\'', key_name)
                key_name_suggestion_1 = regex.sub(r'("\s*\])', '\']', key_name_suggestion_1)
                key_name_suggestion_2 = regex.sub(r'(\[\s*")', '[', key_name)
                key_name_suggestion_2 = regex.sub(r'("\s*\])', ']', key_name_suggestion_2)
                error_msg = f"Invalid key name {key_name}. Please use the syntax {key_name_suggestion_1} or {key_name_suggestion_2} \
to overwrite the value of this parameter."
            else:
                error_msg = f"A substitution in key names is not allowed! Please update the key name \"{self.__remove_token_str(key_name)}\""
        key_name = self.__remove_token_str(key_name)
        if error_msg!='':
            pass
        elif '${' not in key_name and not regex.match(r'^\s*\[\s*import\s*\]\s*$', key_name.lower()) \
            and not regex.search(self.py_call_pattern, key_name):
            if not key_checker.key_name_checker(key_name) and __is_ascii(key_name):
                error_msg = key_checker.error_msg
        elif regex.search(r'\[[^\'\[]+\'[^\']+\'\s*\]|\[\s*\'[^\']+\'[^\]]+\]', key_name) or \
            regex.search(r'\[[^\d\[\]]+\d+\]|\[\d+[^\d\]]+\]', key_name):
            error_msg = f"Invalid syntax: {key_name}"
            if regex.search(r'\[\s*[\-\+:]\d+\s*\]', key_name) or regex.search(r'\[\s*\d+:\s*\]', key_name):
                error_msg = f"Slicing is not supported (expression: '{key_name}')."
        elif regex.match(r'^\s*\${.+[\]}]*$', key_name):
            tmp_key_name = key_name
            while regex.search(r'\[[^\[\]]+\]', tmp_key_name):
                list_check = regex.findall(r'\[[^\[\]]+\]', tmp_key_name)
                for item in list_check:
                    if regex.match(r'^\[[^\'\$]+.+\]$', item):
                        error_msg = f"Invalid syntax: {key_name}"
                tmp_key_name = regex.sub(r'\[[^\[\]]+\]', '', tmp_key_name)
        elif regex.search(r'\$+\${', key_name):
            correct_key = regex.sub(r'(\$+\${)', '${', key_name)
            error_msg = f"Invalid key name: {key_name} - This key name must be '{correct_key}'"
        elif key_name.count('${') != key_name.count('}') or key_name.count('[') != key_name.count(']'):
            error_msg = f"Invalid key name: {key_name} - The brackets mismatch!!!"
        elif regex.match(r'^\s*[^\$]+\${.+$|^\s*\${.+[^}\]]\s*$', key_name):
            error_msg = f"Invalid key name: '{key_name}'."
        elif regex.search(r'\${[^}]*}', key_name):
            if regex.search(r'\[\s*\]', key_name):
                error_msg = f"Invalid key name: {key_name}. A pair of square brackets is empty!!!"
            else:
                tmp_str = key_name
                while regex.search(r'\${([^}]*)}', tmp_str):
                    param = regex.search(r'\${([^}\$]*)}', tmp_str)
                    if param is None and regex.search(r'\${.*\$(?!\{).*}', tmp_str):
                        param = regex.search(r'\${([^}]*)}', tmp_str)
                    if param is not None:
                        if param[1].strip() == '':
                            error_msg = f"Invalid key name: {key_name}. A pair of curly brackets is empty!!!"
                            break
                        elif not key_checker.key_name_checker(param[1].strip()) and __is_ascii(param[1].strip()):
                            error_msg = key_checker.error_msg
                            break
                        elif regex.search(r'^.+\[.+\]$', param[1].strip()):
                            error_msg = f"Invalid syntax: Found index or sub-element inside curly brackets in the parameter '{key_name}'"
                            break
                        else:
                            nested_param = param[0]
                            nested_param = regex.escape(nested_param)
                            tmp_str = regex.sub(rf"[\[\s']*{nested_param}['\s\]]*", '', tmp_str)
        if error_msg != '':
            self.__reset()
            raise Exception(error_msg)

    def __remove_token_str(self, input : str) -> str:
        '''
Checks and removes reserved tokens which are added while handling a content of JSONP files.
**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``input``

  / *Type*: str /
        '''
        for token_str in CNameMangling:
            if token_str.value in input:
                input = input.replace(token_str.value, '')
        return input

    def __pre_check_json_file(self, input, CJSONDecoder):
        '''
Checks and handle dynamic path of imported file.
**Arguments:**

* ``input``

  / *Condition*: required / *Type*: str /

* ``CJSONDecoder``

  / *Condition*: required / *Type*: str /

**Returns:**

* ``input``

  / *Type*: str /
        '''
        def hash_content(input : str) -> str:
            return hashlib.sha256(input.encode('utf-8')).hexdigest()

        try:
            self.json_check = json.loads(input, cls=CJSONDecoder, object_pairs_hook=self.__process_import_files)
        except Exception as error:
            failed_json_doc = self.__get_failed_json_doc(error)
            json_exception = "not defined"
            if "Cyclic import detection" in str(error):
                json_exception = str(error)
            else:
                if failed_json_doc is None:
                    # json_exception = f"{error}\nIn file: '{self.handling_file.pop(-1)}'" if len(self.handling_file)>0 else f"{error}"
                    json_exception = f"{error}"
                else:
                    json_exception = f"{error}\nNearby: '{failed_json_doc}'\nIn file: '{self.handling_file.pop(-1)}'" if len(self.handling_file)>0 else \
                                    f"{error}\nNearby: '{failed_json_doc}'"
                self.__reset()
                raise Exception(json_exception)
        self.jp_globals = self.json_check
        import_pattern = r'([\'|"]\s*\[\s*import\s*\](_\d+)*\s*[\'|"]\s*:\s*[\'|"][^\'"]+[\'|"])'
        str_json = json.dumps(self.json_check)
        # Check cyclic import by comparing the content of the whole JSONP configuration object.
        if len(self.import_check)>1:
            for item in self.import_check:
                if item == hash_content(regex.sub(r'"(\[import\])_\d+"', '"\\1"', str_json)):
                    raise Exception("Cyclic import detection!!!")
        self.import_check.append(hash_content(regex.sub(r'"(\[import\])_\d+"', '"\\1"', str_json)))
        list_import = regex.findall(import_pattern, str_json)
        if len(list_import)==0:
            input = str_json
        else:
            while regex.search(import_pattern, str_json):
                tmp_json = str_json
                self.__check_dot_in_param_name(self.json_check)
                json_obj, is_nested = self.__update_and_replace_nested_param(self.json_check)
                str_json = json.dumps(json_obj)
                if str_json==tmp_json:
                    break
                str_json = self.__pre_check_json_file(str_json, CJSONDecoder)
            input = str_json
        return input

    def __py_builtIn_handle(self, input : str):
        """
Handles Python builtIn function.
        """
        if CNameMangling.PYBUILTINSTR.value in input:
            input = input.replace(CNameMangling.PYBUILTINSTR.value, '"')
        if CNameMangling.PYTHONBUILTIN.value in input:
            input = regex.sub(rf'(self\.jp_globals(?:(?!self\.jp_globals).)+){CNameMangling.PYTHONBUILTIN.value}', \
                              f'"\\1{CNameMangling.PYTHONBUILTIN.value}"', input)
        if regex.match(r'^<<\s*(.*)>$', input):
            py_inline_code = input
        else:
            py_inline_code = regex.findall(rf'{self.py_call_pattern}+', input)[0]
        str_exec = regex.sub(r'<<\s*(.*)>>', "eval_value = \\1", py_inline_code)
        try:
            ldict = {}
            exec(str_exec, locals(), ldict)
            eval_value = ldict['eval_value']
            # Check if py inline code is set as a value of a JSONP parameter
            if isinstance(eval_value, str) and not regex.match(r'^[0-9\.\-+\s]+$', eval_value):
                if CNameMangling.PYTHONBUILTIN.value in eval_value:
                    eval_value = eval_value.replace(CNameMangling.PYTHONBUILTIN.value, '')
                else:
                    str_exec = f"eval_value = {eval_value}"
                    try:
                        ldict = {}
                        exec(str_exec, locals(), ldict)
                        eval_value = ldict['eval_value']
                    except:
                        pass
        except Exception as error:
            raise Exception(error)
        if not isinstance(eval_value, (str, int, float, bool, type(None), list, dict)):
            error_msg = f"The Python builtIn '{self.__remove_token_str(input)}' return the value with \
the datatype '{type(eval_value)}' is not suitable for JSON."
            raise Exception(error_msg)
        if CNameMangling.DYNAMICIMPORTED.value in input:
            input = regex.sub(f'{CNameMangling.DYNAMICIMPORTED.value}', '/', input)
            input = regex.sub(f'{self.py_call_pattern}', f'{eval_value}', input)
            eval_value = input

        return eval_value
    
    def __py_inline_code_syntax_check(self, input : str):
        """
Checks the syntax of Python inline code.
        """
        error_msg = None
        if regex.match(r'^\s*<<\s*>>\s*$', input):
            error_msg = f"The Python builtIn must not be empty. Please check '{self.__remove_token_str(input)}'"
        elif regex.search(rf'\s*"[^",]*{self.py_call_pattern}[^",]*"', input):
            error_msg = f"Python inline code must not be embedded part of a string! Please check the expression {input}"
        elif not regex.search(self.py_call_pattern, input):
            error_msg = f"Invalid syntax: Check the Python inline code '{input}'. "
            if input.count('<<') > input.count('>>'):
                error_msg = error_msg + "Missing closed bracket!"
            elif input.count('<<') < input.count('>>'):
                error_msg = error_msg + "Missing opened bracket!"
            else:
                error_msg = error_msg + "The correct syntax is '<<Python_inline_code>>'!"
        elif regex.match(r'^<<.+>>$', input.strip()) and (input.count('<<')>1 or input.count('>>')>1):
            return f'"{input}"'
        else:
            py_inline_code = regex.search(rf'{self.py_call_pattern}+', input)
            if len(py_inline_code) > 0:
                py_inline_code = py_inline_code[0]
                if regex.search(rf'[^\s]+', input.replace(py_inline_code, ' ')):
                    # tmp_input is used to check the list format (is py inline code in a list)
                    tmp_input = input.replace(py_inline_code, ' ')
                    tmp_input = regex.sub(r'"[^"]+"', ' ', tmp_input)
                    if not regex.match(r'^\[([^,]+,*)+\s*\]*$', tmp_input):
                        return input
                if py_inline_code.count('"') % 2 == 1:
                    error_msg = f"Invalid syntax in the Python inline code '{py_inline_code}'."
                    self.__reset()
                    raise Exception(error_msg)
                elif regex.search(r'"\s*\${[^"]+"', py_inline_code):
                    py_inline_code = regex.sub(r'"\s*(\${[^"]+)\s*"', f'\\1{CNameMangling.PYTHONBUILTIN.value}', py_inline_code)
                py_inline_code = regex.sub(r'"(\s*(?:(?!\${)[^"])*)"', \
                                         f'{CNameMangling.PYBUILTINSTR.value}\\1{CNameMangling.PYBUILTINSTR.value}', py_inline_code)
                input = regex.sub(rf'({self.py_call_pattern}+)', f'"{py_inline_code}"', input)
        if error_msg is not None:
            self.__reset()
            raise Exception(error_msg)
        return input

    def jsonLoad(self, json_file : str):
        """
This is a wrapper for the json_load() function.
        """
        return self.json_load(json_file)

    def json_load(self, json_file : str):
        """
This method is the entry point of JsonPreprocessor.

``json_load`` loads the JSON file, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``json_file``

  / *Condition*: required / *Type*: str /

  Path and name of main JSON file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``json_obj``

  / *Type*: dict /

  Preprocessed JSON file(s) as Python dictionary
        """
        # Identifies the entry level when loading JSONP file in comparison with imported files levels.
        master_file = True if self.recursive_level==0 else False
        json_file = CString.NormalizePath(json_file, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        if self.import_tree is None:
            self.import_tree = CTreeNode(json_file)
            self.current_node = self.import_tree
        else:
            self.current_node.add_child(json_file)
            self.current_node = self.current_node.children[json_file]
        self.handling_file.append(json_file)
        if master_file:
            self.master_file = json_file
        if  not(os.path.isfile(json_file)):
            self.__reset()
            raise Exception(f"File '{json_file}' is not existing!")

        self.json_path = os.path.dirname(json_file)
        try:
            Json_data= CTextProcessor.load_and_remove_comments(json_file)
        except Exception as reason:
            self.__reset()
            raise Exception(f"Could not read json file '{json_file}' due to: '{reason}'!")
        return self.json_loads(Json_data)

    def jsonLoads(self, jsonp_content : str, reference_dir : str = None):
        """
This is a wrapper for the json_loads() function.
        """
        return self.json_loads(jsonp_content, reference_dir)

    def json_loads(self, jsonp_content : str, reference_dir : str = None):
        """
``json_loads`` loads the JSONP content, preprocesses it and returns the preprocessed result as Python dictionary.

**Arguments:**

* ``jsonp_content``

  / *Condition*: required / *Type*: str /

  The JSONP content.

* ``reference_dir``

  / *Condition*: optional / *Type*: str / *Default*: None /

  A reference path for loading imported files.

**Returns:**

* ``json_obj``

  / *Type*: dict /

  Preprocessed JSON content as Python dictionary
        """
        def __handle_duplicated_in_list(list_input : list, key : str, parent_params : str = ''):
            """
This function handles duplicated keys in a list which including dict elements.
            """
            if len(list_input)>0 and isinstance(list_input[0], str) and \
                CNameMangling.DUPLICATEDKEY_01.value in list_input[0]:
                parent_params = regex.sub(r"\['*[^\[]+'*\]$", '', parent_params)
                # Checks the format of the overwritten parameter
                list_overwritten = regex.findall(r'\(([^\(]+)\)', list_input[0])    # Gets absolute paths of duplicated keys from first element. 
                for item in list_overwritten:
                    if item=='None' and parent_params!='':     # Raise exception if an absolute path is not provided.
                        self.__reset()
                        format_overwritten_1 = regex.sub(r'^\[([^\[]+)\]', '${\\1}', parent_params)
                        format_overwritten_1 = format_overwritten_1 + f"['{key}']"
                        format_overwritten_2 = CTextProcessor.multiple_replace(parent_params, {"][":".", "][":".", "[":"", "]":"", "]":"", "'":""})
                        format_overwritten_2 = f"${{{format_overwritten_2}.{key}}}"
                        raise Exception(f"Missing scope for parameter '${{{key}}}'. To change the value of this parameter, \
an absolute path must be used: '{format_overwritten_1}' or '{format_overwritten_2}'.")
                return list_input[-1]
            elif CNameMangling.DUPLICATEDKEY_01.value in str(list_input):
                i=0
                for element in list_input:
                    parent_params = f"{parent_params}[{i}]"
                    if isinstance(element, dict):
                        list_input[i] = __handle_duplicated_key(element, parent_params)
                    elif isinstance(element, list):
                        list_input[i] = __handle_duplicated_in_list(element, key, parent_params)
                    parent_params = regex.sub(rf"\[{i}\]$", '', parent_params)
                    i+=1
                return list_input
            else:
                return list_input

        def __handle_duplicated_key(dict_input : dict, parent_params : str = '') -> dict:
            """
This function handles duplicated keys in a dictionary.
            """
            list_keys = list(dict_input.keys())
            dict_values = {}
            for key in list_keys:
                if CNameMangling.DUPLICATEDKEY_01.value in key:
                    orig_key = regex.sub(rf"{CNameMangling.DUPLICATEDKEY_01.value}\d+\s*$", "", key)
                    dict_values[orig_key] = copy.deepcopy(dict_input[orig_key])
            for key in dict_values.keys():
                dict_input = self.__change_dict_key(dict_input, key, key + CNameMangling.DUPLICATEDKEY_00.value)
            tmp_dict = copy.deepcopy(dict_input)
            for k, v in tmp_dict.items():
                orig_key = regex.sub(rf"{CNameMangling.DUPLICATEDKEY_01.value}\d+\s*$", "", k)
                if CNameMangling.DUPLICATEDKEY_01.value in k:
                    dict_input[k] = dict_values[orig_key].pop(1)
                parent_params = f"[{k}]" if parent_params=='' else f"{parent_params}['{k}']"
                if isinstance(v, list):
                    v = __handle_duplicated_in_list(v, orig_key, parent_params)
                    dict_input[k] = v
                if isinstance(v, dict):
                    dict_input[k] = __handle_duplicated_key(v, parent_params=parent_params)
                parent_params = regex.sub(rf"\['*{regex.escape(k)}'*\]$", '', parent_params)
            del tmp_dict
            del dict_values
            return dict_input
        
        def __remove_duplicated_key(dict_input : dict) -> dict:
            if isinstance(dict_input, dict):
                for k, v in list(dict_input.items()):
                    __remove_duplicated_key(v)
            elif isinstance(dict_input, list):
                for item in dict_input:
                    __remove_duplicated_key(item)

        def __check_keyname_format(json_obj : dict):
            """
This function checks key names in JSON configuration files.
            """
            for k, v in json_obj.items():
                if "${" in k:
                    self.__check_nested_param(k, is_key=True)
                else:
                    self.__key_name_validation(k)
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, str) and "${" in item:
                            self.__check_nested_param(item)
                        elif isinstance(item, dict):
                            __check_keyname_format(item)
                elif isinstance(v, dict):
                    __check_keyname_format(v)

        def __handle_last_element(input : str) -> str:
            '''
This function handle a last element of a list or dictionary
            '''
            param = regex.search(rf'({nested_pattern})', input)
            if param is not None and regex.match(r'^[\s\[\]{}]*$', input.replace(param[0], '')):
                str_param = param[0]
                if str_param.count('[')<str_param.count(']'):
                    while regex.search(r'\[[^\]]+\]', str_param):
                        str_param = regex.sub(r'\[[^\]]+\]', '', str_param)
                    while regex.search(r'\${[^}]+}', str_param):
                        str_param = regex.sub(r'\${[^}]+}', '', str_param)
                    index = len(str_param)
                    str_param = param[0]
                    str_param = str_param[:-index]
                tmp_pattern = regex.escape(str_param)
                input = regex.sub(rf'({tmp_pattern})', '"\\1"', input)
            else:
                str_param = regex.findall(r'^[{\[\s*]*(.+)$', input.strip())[0]
                input = input.replace(str_param, f'"{str_param}"')
            return input

        if not isinstance(jsonp_content, str):
            self.__reset()
            raise Exception(f'Expected a string, but got a value of type {type(jsonp_content)}')
        # Identifies the entry level when loading JSONP content in comparison with imported files levels.
        first_level = True if self.recursive_level==0 else False
        if reference_dir is not None:
            self.json_path = CString.NormalizePath(reference_dir, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
            if not os.path.exists(self.json_path):
                self.__reset()
                raise Exception(f"Reference directory '{reference_dir}' is not existing!")
        if self.import_tree is None:
            self.import_tree = CTreeNode(f'Root:{self.json_path}')
            self.current_node = self.import_tree
        if self.master_file is None or not first_level:
            try:
                Json_data= CTextProcessor.load_and_remove_comments(jsonp_content, is_file=False)
            except Exception as reason:
                self.__reset()
                raise Exception(f"Could not read JSONP content due to: '{reason}'!")
        else:
            Json_data = jsonp_content
        # Checking: Do token strings which are reserved in CNameMangling present jsonp file.
        reserved_tokens = [token_str.value for token_str in CNameMangling]
        for reserved_token in reserved_tokens:
            if reserved_token in Json_data:
                self.__reset()
                raise Exception(f"The JSONP content contains a reserved token '{reserved_token}'")
        index_pattern = r"\[[\s\-\+\d]*\]|\[.*:.*\]"
        dict_pattern = rf"\[+\s*'.+'\s*\]+|\[+\s*\d+\s*\]+|\[+\s*\${{\s*[^\[]+\s*}}.*\]+|{index_pattern}"
        nested_pattern = rf"\${{\s*[^\[}}\$]+(\.*\${{\s*[^\[]+\s*}})*\s*}}({dict_pattern})*"
        json_data_updated = ""
        nested_params = []
        for line in Json_data.splitlines():
            if line == '' or line.isspace():
                continue
            try:
                list_dummy = shlex.split(line)
            except Exception as error:
                self.__reset()
                raise Exception(f"{error} in line: '{line}'")
            line = line.rstrip()
            # Handles byte value in JSONP by make-up byte values by token string
            list_byte_value = regex.findall(r'[^"]\s*(b\'[^\']+\')\s*', line)
            for byte_value in list_byte_value:
                self.byte_value_index +=1
                key = f'{CNameMangling.BYTEVALUE.value}{self.byte_value_index}'
                self.byte_value.update({key: byte_value})
                line = line.replace(byte_value, f'"{key}"')
            # Checks the syntax of the Python inline code
            if '<<' in line or '>>' in line:
                if regex.search(rf'\${{\s*{self.py_call_pattern}\s*}}', line):
                    invalid_param = regex.findall(rf'\${{\s*{self.py_call_pattern}\s*}}', line)[0]
                    raise Exception(f"Python inline code must not be used within dollar operator expression! \
Please check the expression '{invalid_param}'")
                patterns = [
                    r':\s*([^<:\[]*<.*>[^>,\]\}\n]*)\s*[,\]\}\n]*',            # normal JSONP value
                    r'\[\s*([^<,]*<(?:(?!>>).)*>*>[^>,\]\}\n]*)\s*[,\]\}\n]*', # first list element in JSONP value
                    r',\s*([^<,]*<(?:(?!>>).)*>*>[^>,\]\}\n]*)\s*,',           # list element in JSONP value
                    r',\s*([^<,]*<(?:(?!>>).)*>*>[^>,\]\}\n]*)\s*\]'           # last list element in JSONP value
                ]
                py_inline = []
                py_inline = [match for pattern in patterns for match in regex.findall(pattern, line)]
                if len(py_inline)>0:
                    for item in py_inline:
                        if item.strip()=='' or ('<<' not in item and '>>' not in item):
                            continue
                        new_item = self.__py_inline_code_syntax_check(item)
                        line = line.replace(item, new_item)
            if "${" in line:
                line = regex.sub(r'\${\s*([^\s][^}]+[^\s])\s*}', '${\\1}', line)
                cur_line = line
                tmp_list_03 = []
                while regex.search(r'\${([^}]*)}', line):
                    tmp_line = line
                    param = regex.search(r'\${([^}\$]*)}', line)
                    if param is None and regex.search(r'\${.*\$(?!\{).*}', line):
                        param = regex.search(r'\${([^}]*)}', line)
                    if param is not None:
                        nested_params.append(param[0])
                        if ':' in param[0]:
                            tmp_list_03.append(param[0])
                            tmp_pattern = regex.escape(param[0])
                            line = regex.sub(tmp_pattern, CNameMangling.NESTEDPARAM.value, line)
                    if line == tmp_line:
                        break
                tmp_list_01 = regex.findall(r"(\"[^\"]+\")", line)
                line = regex.sub(r"(\"[^\"]+\")", CNameMangling.COLONS.value, line)
                slicing_pattern = r"\[[\p{L}\p{Nd}\.\-\+\${}'\s]*:[\p{L}\p{Nd}\.\-\+\${}'\s]*\]"
                tmp_list_02 = regex.findall(slicing_pattern, line)
                line = regex.sub(slicing_pattern, CNameMangling.SLICEINDEX.value, line)
                index_pattern = r"\[[\s\-\+\d]*\]"
                index_list = []
                if regex.search(index_pattern, line):
                    index_list = regex.findall(index_pattern, line)
                    line = regex.sub(f"({index_pattern})", CNameMangling.LISTINDEX.value, line)
                items = regex.split(r"\s*:\s*", line)
                int_items = len(items)-1 if items[-1]=='' else len(items) 
                new_line = ''
                pre_item = ''
                i=1
                for item in items:
                    if CNameMangling.COLONS.value in item:
                        while CNameMangling.COLONS.value in item:
                            item = item.replace(CNameMangling.COLONS.value, tmp_list_01.pop(0), 1)
                    if CNameMangling.LISTINDEX.value in item:
                        while CNameMangling.LISTINDEX.value in item and len(index_list)>0:
                            item = item.replace(CNameMangling.LISTINDEX.value, index_list.pop(0), 1)
                    if CNameMangling.SLICEINDEX.value in item:
                        while CNameMangling.SLICEINDEX.value in item:
                            item = item.replace(CNameMangling.SLICEINDEX.value, tmp_list_02.pop(0), 1)
                    if CNameMangling.NESTEDPARAM.value in item:
                        while CNameMangling.NESTEDPARAM.value in item:
                            item = item.replace(CNameMangling.NESTEDPARAM.value, tmp_list_03.pop(0))
                    cur_item = item
                    if "${" in item:
                        tmp_list = []
                        is_handle = False
                        if '"' in item and item.count('"')%2==0:
                            tmp_list = regex.findall(r'"[^"]+"', item)
                            item = regex.sub(r'"[^"]+"', CNameMangling.STRINGVALUE.value, item)
                        if regex.search(r'[\(\)\!#%\^\&\/\\\=`~\?]+', item):
                            if regex.match(r'^.+,\s*$', item):
                                item = regex.sub(r'^\s*(.+),\s*$', '"\\1",', item)
                            else:
                                item = regex.sub(r'^\s*(.+)\s*$', '"\\1"', item)
                            is_handle = True
                        if "," in item and not is_handle:
                            if item.count(',')>1:
                                if not (regex.match(r'^\[|{.+$', item.strip()) or \
                                        item.count('${')!=item.count('}') or item.count('[')!=item.count(']')):
                                    tmp_pattern_1 = regex.escape(pre_item)
                                    tmp_pattern_2 = regex.escape(cur_item)
                                    if regex.search(rf'{tmp_pattern_1}\s*:\s*{tmp_pattern_2}', cur_line):
                                        item = regex.sub(r'^\s*(.+)\s*', '"\\1"', item)
                                        is_handle = True
                            if not is_handle:
                                sub_items = item.split(',')
                                int_sub_items = len(sub_items) -1 if sub_items[-1]=='' else len(sub_items)
                                new_sub_item = ""
                                j=1
                                for sub_item in sub_items:
                                    if "${" in sub_item:
                                        if int_sub_items>1 and j<int_sub_items:
                                            if sub_item.count("${") < sub_item.count("}") or sub_item.count("[") < sub_item.count("]"):
                                                sub_item = __handle_last_element(sub_item)
                                            elif regex.match(r'^\${.+$', sub_item.strip()):
                                                sub_item = f'"{sub_item.strip()}"'
                                            else:
                                                sub_item = regex.sub(r'(\${.+$)', '"\\1"', sub_item.strip())
                                        else:
                                            sub_item = __handle_last_element(sub_item)
                                    if j < int_sub_items:
                                        new_sub_item = f'{new_sub_item}{sub_item}, '
                                    else:
                                        new_sub_item = f'{new_sub_item}{sub_item},' if sub_item=='' else f'{new_sub_item}{sub_item}'
                                    j+=1
                                item = new_sub_item
                        else:
                            if "${" in item and not is_handle:
                                if i==int_items:
                                    item = __handle_last_element(item)
                                elif not regex.match(r'^[\s{]*"[^"]*"\s*$', item):
                                    if CNameMangling.STRINGVALUE.value in item:
                                        item = regex.sub(r'(^[\s{]*)([^\s].+[^\s])\s*$', '\\1\'\\2\' ', item)
                                    else:
                                        item = regex.sub(r'(^[\s{]*)([^\s].+[^\s])\s*$', '\\1"\\2" ', item)
                        while CNameMangling.STRINGVALUE.value in item:
                            if "${" in tmp_list[0]:
                                str_value = tmp_list.pop(0)
                                str_value = regex.sub(rf'({nested_pattern})', '\\1' + CNameMangling.STRINGCONVERT.value, str_value)
                                item = item.replace(CNameMangling.STRINGVALUE.value, str_value, 1)
                            else:
                                item = item.replace(CNameMangling.STRINGVALUE.value, tmp_list.pop(0), 1)
                    if i<int_items:
                        new_line = f"{new_line}{item} : "
                    else:
                        new_line = f"{new_line}{item} :" if item=='' else f"{new_line}{item}"
                    pre_item = cur_item
                    i+=1
                if regex.search(r"\[\s*\+\s*\d+\s*\]", new_line):
                    new_line = regex.sub(r"\[\s*\+\s*(\d+)\s*\]", "[\\1]", new_line)
                json_data_updated = f"{json_data_updated}{new_line}\n"
            else:
                json_data_updated = f"{json_data_updated}{line}\n"
        json_data_updated = CTextProcessor.normalize_digits(json_data_updated)
        json_data_updated = regex.sub(r'\[\s+\'', '[\'', json_data_updated)
        json_data_updated = regex.sub(r'\'\s+\]', '\']', json_data_updated)
        # Get the list of key names which are enclosed by double quotes
        list_key_name = regex.findall(r'[,\s{]*("[^"\n]*")\s*:\s*', json_data_updated)
        tmp_json_data_updated = regex.sub(r":\s*\"[^\"]*\"", ": \"\"", json_data_updated)
        tmp_json_data_updated = regex.sub(r"\[[^:]*:[^:]*\]", "[]", tmp_json_data_updated)
        # Get the list of nested key names and Python inline code in key names
        list_key_name = list_key_name + regex.findall(r'[,\s{]*(\${[^:,\n]+)\s*:\s*[^\]}]', tmp_json_data_updated)
        list_key_name = list_key_name + regex.findall(rf'[,\s{{]*({self.py_call_pattern})\s*:\s*[^\]}}]', tmp_json_data_updated)
        for key in list_key_name:
            error_msg = None
            if regex.match(rf'^"{CNameMangling.BYTEVALUE.value}\d+"$', key):
                tmp_key = self.byte_value[key.strip('"')]
                error_msg = f"Type error in key {tmp_key}. Key names must be strings; byte values are not supported."
            elif regex.match(r'^"\s+[^\s]+.+"$|^".+[^\s]+\s+"$', key):
                new_key = '"' + key.strip('"').strip() + '"'
                json_data_updated = json_data_updated.replace(key, new_key)
                key = new_key
            elif regex.match(r'^\s*\${.*$', key):
                if key.count('{') != key.count('}'):
                    error_msg = f"Invalid syntax: '{key.strip()}' - The curly brackets do not match."
                elif key.count('[') != key.count(']'):
                    error_msg = f"Invalid syntax: '{key.strip()}' - The square brackets do not match."
            if error_msg is not None:
                self.__reset()
                raise Exception(error_msg)
            if r'\"' in key:  # Ignore key name validation in case user converts a dictionary to string.
                continue
            key_decode = bytes(key, 'utf-8').decode('utf-8')
            self.__key_name_validation(key_decode.strip('"'))
        for param in nested_params:
            self.__key_name_validation(param)
        CJSONDecoder = None
        if self.syntax != CSyntaxType.json:
            if self.syntax == CSyntaxType.python:
                CJSONDecoder = CPythonJSONDecoder
            else:
                self.__reset()
                raise Exception(f"Provided syntax '{self.syntax}' is not supported.")
        # Load the temporary Json object without checking duplicated keys for 
        # verifying duplicated keys later. The pre-check method also checks dynamic 
        # imported files in JSON files.
        if first_level:
            self.json_pre_check = True
            try:
                sdummy_data = self.__pre_check_json_file(json_data_updated, CJSONDecoder)
            except Exception as error:
                if "Cyclic import detection" in str(error):
                    pass
                else:
                    self.__reset()
                    raise Exception(error)
            self.i_dynamic_import = 0
            self.recursive_level = 0
            self.is_dynamic_import  = False
            self.handling_file = [] if self.master_file is None else [self.master_file]
            if not regex.match(f'^Root:.+$', self.import_tree.value):
                self.json_path = os.path.dirname(self.import_tree.value)
            else:
                self.json_path = regex.sub(r'(^Root:)', '', self.import_tree.value)
            self.import_tree.children = {}
            self.current_node = self.import_tree
            self.json_pre_check = False

        # Load Json object with checking duplicated keys feature is enabled.
        # The duplicated keys feature uses the self.json_check object to check duplicated keys. 
        try:
            json_obj = json.loads(json_data_updated,
                               cls=CJSONDecoder,
                               object_pairs_hook=self.__process_import_files)
        except Exception as error:
            failed_json_doc = self.__get_failed_json_doc(error)
            json_exception = "not defined"
            if "Cyclic import detection" in str(error):
                json_exception = str(error)
            else:
                if failed_json_doc is None:
                    # json_exception = f"{error}\nIn file: '{self.handling_file.pop(-1)}'" if len(self.handling_file)>0 else f"{error}"
                    json_exception = f"{error}"
                else:
                    json_exception = f"{error}\nNearby: '{failed_json_doc}'\nIn file: '{self.handling_file.pop(-1)}'" if len(self.handling_file)>0 else \
                                    f"{error}\nNearby: '{failed_json_doc}'"
            if first_level:
                self.__reset()
            raise Exception(json_exception)
        self.__check_dot_in_param_name(json_obj)

        if first_level:
            json_obj = __handle_duplicated_key(json_obj)
            for k, v in json_obj.items():
                if regex.match(r"^[\p{Nd}]+.*$", k) or regex.match(r"^[\s\"]*\${.+}[\s\"]*$", k) \
                    or CNameMangling.DUPLICATEDKEY_01.value in k:
                    continue
                if k in self.list_datatypes:
                    k = CNameMangling.AVOIDDATATYPE.value + k
                self.jp_globals.update({k:v})
            __check_keyname_format(json_obj)
            json_obj, is_nested = self.__update_and_replace_nested_param(json_obj)
            self.json_check = {}
            self.__reset()
            __remove_duplicated_key(json_obj)
            json_obj = DotDict(json_obj)
        return json_obj

    def jsonDump(self, json_obj : dict, out_file : str) -> str:
        """
This is a wrapper for the json_dump() function.
        """
        return self.json_dump(json_obj, out_file)

    def json_dump(self, json_obj : dict, out_file : str) -> str:
        """
This method writes the content of a Python dictionary to a file in JSON format and returns a normalized path to this JSON file.

**Arguments:**

* ``json_obj``

  / *Condition*: required / *Type*: dict /

* ``out_file`` (*string*)

  / *Condition*: required / *Type*: str /

  Path and name of the JSON output file. The path can be absolute or relative and is also allowed to contain environment variables.

**Returns:**

* ``out_file`` (*string*)

  / *Type*: str /

  Normalized path and name of the JSON output file.
        """
        out_file = CString.NormalizePath(out_file, sReferencePathAbs=os.path.dirname(os.path.abspath(sys.argv[0])))
        json_obj = json.dumps(json_obj, ensure_ascii=False, indent=4)
        try:
            with open(out_file, "w", encoding='utf-8') as f:
                f.write(json_obj)
        except Exception as error:
            error_msg = f"Could not write a JSON file '{out_file}'! Reason: {error}"
            raise Exception(error_msg)

        return out_file