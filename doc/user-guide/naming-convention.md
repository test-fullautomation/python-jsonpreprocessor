# User defined naming convention

By default, key names in JSONP files can contain any characters (but cannot be empty). Only the brackets
`[`, `]`, `{`, `}`, `<`, `>` must not be used, because they are syntax elements of the JSONP format
(see [Special characters within key names](../jsonp-format/special-characters.md)).

It might be required to add further limitations to the set of allowed characters. For this purpose the JsonPreprocessor
supports an optional **user defined convention for key names**. It is enforced by a `regex` pattern that is passed to the
constructor (parameter `key_pattern`).

## Example

Key names may only contain letters, digits and underscores, but must start with a letter:

```python hl_lines="4"
from JsonPreprocessor.CJsonPreprocessor import CJsonPreprocessor
import pprint

json_preprocessor = CJsonPreprocessor(key_pattern=r'^\p{L}[\p{L}\p{Nd}_]*$')
try:
    values = json_preprocessor.jsonLoad("./file.jsonp")
    pprint.pprint(values)
except Exception as reason:
    print(f"'{reason}'")
```

The regular expressions `\p{L}` and `\p{Nd}` are provided by the [`regex`](https://pypi.org/project/regex/) module:

| Expression | Matches |
|---|---|
| `\p{L}` | all Unicode characters classified as **letter** |
| `\p{Nd}` | all Unicode characters classified as **decimal digit** |

A key name that does not match causes an error:

```text
Error: Key name '1st_value' is invalid. Expected format: '^\p{L}[\p{L}\p{Nd}_]*$'
```

## Rules for the pattern

| Pattern | Result |
|---|---|
| not of type `str` | error |
| `''` or `'.*'` | error - these patterns would allow empty key names |
| whitespace only | error |
| default `'.+'` | every non-empty key name is allowed |

!!! info "RobotFramework AIO"
    The TestsuitesManagement of RobotFramework AIO uses the convention `^\p{L}[\p{L}\p{Nd}_]*$` for the names of
    parameters that are made available in Robot Framework.
