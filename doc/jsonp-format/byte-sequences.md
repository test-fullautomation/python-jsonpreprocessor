# Byte sequences

The JsonPreprocessor supports the explicit embedding of binary values (in hexadecimal escape notation):

```json
"bytesequence" : b'\x52\x6f\x62\x6f\x74\x46\x72\x61\x6d\x65\x77\x6f\x72\x6b\x20\x41\x49\x4f'
```

The result is the resolved content of Python type `bytes`:

```python
DotDict({'bytesequence': b'RobotFramework AIO'})
```

!!! warning
    This feature requires **single quotes**: `b'...'`. Double quotes must not be used.
