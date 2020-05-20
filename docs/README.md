# FOR Ubuntu 20.04 (on a Fresh install of OS)


1. Install GNURadio

# Install Guide

1. Clone the repository and within the gr-XXX folder create a build folder

`mkdir build`

2. Change directory into the build folder

`cd build`


3. run the following commands

```
cmake ..
sudo make
sudo make install
sudo ldconfig
```

4. Run GNU Radio Companion to check if the modules were installed. 
