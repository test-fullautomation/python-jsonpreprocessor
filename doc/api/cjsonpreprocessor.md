# API reference

## Module `JsonPreprocessor.CJsonPreprocessor`

```python
from JsonPreprocessor.CJsonPreprocessor import CJsonPreprocessor, CSyntaxType
```

---

## class `CSyntaxType`

Defines the accepted keywords in JSONP files.

| Attribute | Value | Meaning |
|---|---|---|
| `CSyntaxType.python` | `"python"` | JSON keywords **and** Python keywords `True`, `False`, `None` are allowed |
| `CSyntaxType.json` | `"json"` | only JSON keywords `true`, `false`, `null` are allowed |

---

## class `CJsonPreprocessor`

Extends the JSON syntax by the following features:

- c/c++-style comments within JSON files
- import of JSON files into JSON files
- definition and usage of parameters within JSON files
- Python keywords `True`, `False` and `None`

### Constructor

```python
CJsonPreprocessor(syntax=CSyntaxType.python, current_cfg={}, key_pattern=r'.+')
```

| Argument | Type | Default | Description |
|---|---|---|---|
| `syntax` | `CSyntaxType` | `CSyntaxType.python` | If set to `python`, Python keywords are allowed as part of JSON files. |
| `current_cfg` | `dict` | `{}` | Parameters which are available in addition to the parameters of the JSONP file. They can be referenced and overwritten and are part of the result. |
| `key_pattern` | `str` | `r'.+'` | Regular expression (module `regex`) all key names must match. See [User defined naming convention](../user-guide/naming-convention.md). |

**Raises** an `Exception` if `key_pattern` is not a string, is empty, is `'.*'` or contains only whitespace.

---

### `jsonLoad(json_file)` / `json_load(json_file)`

Entry point of the JsonPreprocessor. Loads the JSONP file, preprocesses it and returns the result as Python dictionary.

| Argument | Type | Description |
|---|---|---|
| `json_file` | `str` | Path and name of the main JSONP file. The path can be absolute or relative (to the executed script) and may contain environment variables. |

**Returns:** `DotDict` - the preprocessed JSONP file(s) as Python dictionary.

**Raises:** `Exception` in case of any error.

---

### `jsonLoads(jsonp_content, reference_dir=None)` / `json_loads(...)`

Loads JSONP content from a string, preprocesses it and returns the result as Python dictionary.

| Argument | Type | Default | Description |
|---|---|---|---|
| `jsonp_content` | `str` | - | The JSONP content. |
| `reference_dir` | `str` | `None` | Reference directory for imported files with relative paths. Must exist. |

**Returns:** `DotDict` - the preprocessed JSONP content as Python dictionary.

**Raises:** `Exception` if the content is not a string, the reference directory does not exist, or in case of any error in the content.

---

### `jsonDump(json_obj, out_file)` / `json_dump(...)`

Writes the content of a Python dictionary to a file in standard JSON format (UTF-8, indentation 4).

| Argument | Type | Description |
|---|---|---|
| `json_obj` | `dict` | The dictionary to be written. |
| `out_file` | `str` | Path and name of the JSON output file. The path can be absolute or relative (to the executed script) and may contain environment variables. |

**Returns:** `str` - normalized path and name of the written JSON file.

**Raises:** `Exception` if the file cannot be written.

---

### `getVersion()`

**Returns:** `str` - the version of the JsonPreprocessor.

### `getVersionDate()`

**Returns:** `str` - the version date of the JsonPreprocessor.

---

## The `DotDict` return type

All loading methods return a `DotDict` (package [`pydotdict`](https://pypi.org/project/pydotdict/)): a `dict` subclass
that additionally provides attribute access to keys (`values.key.sub_key`). Nested dictionaries are also of type `DotDict`.
If the JSONP content is not a JSON object (e.g. a list), the plain Python value is returned.
