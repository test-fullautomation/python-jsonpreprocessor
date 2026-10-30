# FAQ

## General

??? question "Do I have to use the extension `.jsonp`?"
    No. The JsonPreprocessor also accepts `.json` files. But the extension `.jsonp` is recommended to have a strict
    separation between standard JSON and the extended format - and to get the right syntax highlighting
    (see [VSCodium support](../user-guide/vscodium-support.md)).

??? question "Is every JSON file also a valid JSONP file?"
    Yes. See [Standard JSON format](../jsonp-format/standard-json.md).

??? question "Can I convert a JSONP configuration back to standard JSON?"
    Yes. Load it with `jsonLoad` and write the result with `jsonDump`. The written file contains standard JSON with all
    imports, parameters and inline code resolved. See [Using the JsonPreprocessor in Python](../user-guide/python-usage.md#write-the-result-as-standard-json).

## Parameters

??? question "Why does a parameter not have the value I expect?"
    The value a parameter has finally depends on the **order** of definitions, redefinitions and imports - the
    definition processed last wins. Check whether an import placed *after* your definition overwrites it.
    See [The order matters](../jsonp-format/overwriting-parameters.md#the-order-matters).

??? question "Can I reference a parameter that is defined later in the file?"
    Yes. Parameters can be referenced independently of the position of their definition, as long as they are defined
    somewhere in the configuration and the references are not cyclic.

??? question "Why is my number a string?"
    You probably used quotes: `"b" : "${a}"` converts the value to `str`. Use `"b" : ${a}` to keep the data type.

??? question "How can I add an element to a list?"
    Adding elements to an existing list on the left-hand side is not possible. Overwrite the entire list instead,
    e.g. `${my_list} : <<${my_list} + ["new"]>>`. See [Python inline code](../jsonp-format/python-inline-code.md).

??? question "I made a typo in a key name, but I get no error."
    With [implicit creation](../jsonp-format/implicit-creation.md) the missing levels of a data structure are created
    automatically - also for misspelled names. Check the result (e.g. with `jsonDump`) or restrict the key names with a
    [naming convention](../user-guide/naming-convention.md).

## Security

??? question "Is it safe to load JSONP files from unknown sources?"
    No. [Python inline code](../jsonp-format/python-inline-code.md) is executed while loading a file. Only load
    JSONP files from trusted sources.

## Robot Framework

??? question "Can I use JSONP files in Robot Framework tests?"
    Yes - with the
    [RobotFramework_TestsuitesManagement](https://github.com/test-fullautomation/robotframework-testsuitesmanagement)
    (part of [RobotFramework AIO](https://robotframework-aio.org/)). There, parameter names are restricted to letters,
    digits and underscores.
