# gr-radio_astro

This package provides GNUradio OOT modules and `grc` flowgraphs that fascilates Radio Astronomy Observations with software defined radio devices.

There are two flavors of this projects:

1. NSF Integrate and Detect softwares that allow for HI measurements and also event detections from cosmic ray detections. See [here](https://github.com/WVURAIL/gr-radio_astro/wiki/Nsf-gr-radio_astro) and the [lightwork memo series](https://wvurail.org/lightwork/) for more details. 
2. DSPIRA software developed for and by High School Teachers part of the [NSF funded RET program called Digital Signal Processing in Radio Astronomy (DSPIRA)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1611114) at WVU university from the summers of 2017 to 2021. For more details visit the [webpage](https://wvurail.org/dspira-lessons/about/) and the companion website called [dspira-lessons](https://wvurail.org/dspira-lessons/) that has lessons, guides and more material help one to use radio astronomy in a high school classroom. This material is designed by the High School teachers part of this program. 

# Installing

1. Install GNUradio
2. 2. Install gnuradio external python dependencies and SDR drivers by typing the following and hit enter:
   ```
      sudo apt install gnuradio gr-osmosdr airspy python3-h5py python3-ephem git cmake liborc-0.4-dev -y
   ```
3. To clone the repository:
```
git clone https://github.com/WVURAIL/gr-radio_astro.git
```
4. Switch to the gr-radio_astro directory: `cd gr-radio_astro`
5. Make a build directory: `mkdir build`, and then move to it: `cd build`  
6. Then run the following in the build directory:
      ```
      cmake ..
      sudo make
      sudo make install
      ```
**Additional Steps for setting the proper Python environment:**
   
8. Edit your `.bashrc` filr
9. Set Python path: `export PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3.8/dist-packages:$PYTHONPATH`
10. Additionally you can create appropriate symbolic links
       1.  Check which python is the installed version of GNURadio by opening  `gnuradio-companion` in a terminal window and click on `Help --> About` and noting the python version on the dialog box that opens.  
       2.  Go to the following by typing: `cd /usr/local/lib/python3.8/dist-packages` or `cd /usr/local/lib/python3.9/dist-packages` for the appropriate python version. 
       3.  Type `ln -s /usr/local/lib/python3/dist-packages/radio_astro`   

