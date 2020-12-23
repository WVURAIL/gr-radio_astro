# FOR Ubuntu 20.04 (on a Fresh install of OS)


1. Install GNURadio

* Open **Terminal**
* Install gnuradio, external python dependencies and SDR drivers

`sudo apt install gnuradio gr-osmosdr airspy python3-h5py python3-ephem`

* In at least one test case `liborc-0.4-dev` was need to be installed by running 

`sudo apt install liborc-0.4-dev`

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
