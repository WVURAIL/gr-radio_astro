# Research block tests

Configure and build the repository before running these tests:

```sh
cmake -S . -B build -DPYTHON_EXECUTABLE=/usr/bin/python3
cmake --build build
ctest --test-dir build --output-on-failure
```

The nine QA files cover the native blocks and six Python research blocks.
Tests import the package assembled under `build/test_modules`.
They do not require a receiver or execute the historical research notebooks.
