# Error handling

In case of any problem the JsonPreprocessor raises an `Exception` with a meaningful message.
There is no partial result - either the complete configuration is valid, or you get an exception.

```python
try:
    values = json_preprocessor.jsonLoad("./file.jsonp")
except Exception as reason:
    print(f"Configuration could not be loaded: {reason}")
    raise
```

## Typical errors and how to fix them

| Message (excerpt) | Cause | Fix |
|---|---|---|
| `File '...' is not existing!` | wrong path in `jsonLoad` or in an `"[import]"` | check the path; relative import paths are relative to the importing file; use [`"[import?]"`](../jsonp-format/imports.md#optional-imports) for optional files |
| `... [import] object ...` | invalid [import object](../jsonp-format/imports.md#conditional-imports) (unknown key, missing `file`, `else` without `if`, wrong data type) | allowed keys: `file`, `if`, `else`, `optional`; `if` requires a `bool` |
| `Could not evaluate the condition of the [import] object.` | the condition refers to a not existing parameter | define the parameter before the import |
| `Expecting ... : line X column Y` with `Nearby: '...'` | JSON syntax error (missing comma, missing quote, ...) | the `Nearby` part shows the text around the error position |
| `The parameter '${x}' is not available!` | reference to a parameter that does not exist | check spelling and import order |
| `The substitution of parameter '${x}' inside the string value ... is not allowed!` | a list or dictionary is used inside a string | reference the value without quotes, or access a single element |
| `A substitution in key names is not allowed!` | `${...}` inside the key of a dictionary definition | use [dynamic key names](../jsonp-format/dynamic-key-names.md) on the left-hand side for existing keys |
| `Identified dynamic name of key ... that does not exist.` | a parameter is used to create a new key | use hard coded key names for [implicit creation](../jsonp-format/implicit-creation.md) |
| `Could not set parameter ... list assignment index out of range` | list index out of range on the left-hand side | lists cannot be extended - overwrite the entire list |
| `Python inline code must not be ...` | Python inline code at a not supported position | see [limitations](../jsonp-format/python-inline-code.md#limitations) |
| `Cyclic import detection: ...` | files import each other | restructure the imports |
| `Key name '...' is invalid. Expected format: '...'` | key name does not match the `key_pattern` | rename the key, see [naming convention](naming-convention.md) |

## Error position in imported files

If an error happens inside an imported file, the message contains the affected file:

```text
Expecting ',' delimiter: line 3 column 4 (char 16)
Nearby: '... {\n   "a" : 1\n   "b" : 2\n}\n ...'
In file: 'C:/project/config/common.jsonp'
```

!!! tip "Debugging complex configurations"
    1. Reduce the configuration step by step (comment out imports with `//`) until the error disappears.
    2. Use `jsonDump` to write the resolved result of a working configuration into a standard JSON file and inspect it.
