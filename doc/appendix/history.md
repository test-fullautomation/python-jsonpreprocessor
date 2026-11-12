# History

| Version | Date | Changes |
|---|---|---|
| 0.12.0 | 02.02.2026 | Usage of `Setuptools` replaced by usage of `PIP/TOML/Setuptools` |
| 0.11.2 | 01/2026 | Stabilized the explicit embedding of binary values |
| 0.11.1 | 12/2025 | Refactored codebase to comply with PEP 8 style guidelines; fixed bugs |
| 0.11.0 | 11/2025 | Added support of explicit embedding of binary values |
| 0.10.1 | 08/2025 | Fixed bugs in the Python inline code feature |
| 0.10.0 | 07/2025 | Added possibility to use Python inline code inside JSONP files |
| 0.9.3 | 07/2025 | Allowed unicode digits to get a list element; updated error messages |
| 0.9.2 | 06/2025 | Improved invalid key name detection; fixed bugs |
| 0.9.1 | 05/2025 | Enhanced cyclic import detection; fixed bugs and updated error messages |
| 0.9.0 | 03/2025 | Added support of a user-defined convention for key names; improved and aligned error messages; fixed bugs and updated the selftest according to the changes |
| 0.8.4 | 02/2025 | Fixed bugs, updated error messages, and improved composite data structure handling |
| 0.8.3 | 11/2024 | Fixed bugs and updated error messages related to dynamic imports |
| 0.8.2 | 10/2024 | Enhanced import JSON file feature which allows dynamic path of imported file |
| 0.8.1 | 10/2024 | Fixed issues related to the naming convention check for key names; improved implicit creation feature; prevented side effects of token string in error messages log; checked absolute path when overwriting parameter |
| 0.8.0 | 08/2024 | Implemented a naming convention check for key names within .jsonp files; fixed issues related to error handling deviation; updated error messages log |
| 0.7.1 | 06/2024 | Maintained release workflow |
| 0.7.0 | 06/2024 | Added `jsonLoads` method that allows users to directly parse JSONP content from strings; improved error messages; fixed bugs |
| 0.6.1 | 05/2024 | Added pydotdict package to installation dependencies |
| 0.6.0 | 05/2024 | JsonPreprocessor returns a dotdict; blocked dynamic key names; improved error messages; fixed bugs |
| 0.5.0 | 04/2024 | Extended debugging support: in case of JSON syntax errors, the exception contains an extract of the JSON content nearby the error position |
| 0.4.0 | 03/2024 | Optimized regular expression patterns; improved duplicated parameters handling; added mechanism to prevent Python application freeze; removed globals scope out of all exec method executions; optimized errors handling while loading nested parameters; fixed bugs |
| 0.3.3 | 01/2024 | Some bugs fixed in implicitly created data structures; improved index handling together with nested parameters; improved format of nested parameters; improved error messages; added `getVersion` and `getVersionDate` methods |
| 0.3.1 | 12/2023 | Added `jsonDump` method to write a file in JSON format; improved nested parameter format; improved error message log; fixed bugs of implicitly created data structures; improved index handling together with nested parameters |
| 0.3.0 | 09/2023 | Implicit creation of data structures; dotdict feature bug fixing; updated nested parameters handling in key name and value; nested parameter feature bug fixing; nested parameters substitution and overwriting improvement; JSONP file path computation improvement |
| 0.2.4 | 06/2023 | Maintenance of dotdict format and log output |
| 0.2.3 | 05/2023 | dotdict format added |
| 0.1.4 | 09/2022 | Documentation updated |
| 0.1.0 | 01/2022 | Initial version |
