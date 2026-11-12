# Installation

## Requirements

- Python **3.11** or newer

All further dependencies (e.g. `regex`, `pydotdict`, `PythonExtensionsCollection`) are installed automatically.

## Install from PyPI (recommended)

```bash
pip install JsonPreprocessor
```

Behind a proxy:

```bash
pip install --proxy <proxy> JsonPreprocessor
```

## Install from GitHub

Use this way if you want to work with the latest sources or contribute to the project.

```bash
git clone https://github.com/test-fullautomation/python-jsonpreprocessor.git
cd python-jsonpreprocessor
python -m pip install .
```

More details for developers can be found in [Build, test and document](../developers/build-and-test.md).

## Check the installation

```python
from JsonPreprocessor.CJsonPreprocessor import CJsonPreprocessor

print(CJsonPreprocessor().getVersion())
```

!!! note "RobotFramework AIO"
    If you use [RobotFramework AIO](https://robotframework-aio.org/), the JsonPreprocessor is already part of the
    installation. No separate installation is required.

Continue with the [Quick start](quick-start.md).
