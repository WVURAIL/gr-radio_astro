# gr-radio_astro

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14583457.svg)](https://doi.org/10.5281/zenodo.14583457)


This package provides GNUradio OOT modules and `grc` flowgraphs that facilates Radio Astronomy Observations with software defined radio devices.

There are two flavors of this projects:

1. NSF Integrate and Detect softwares that allow for HI measurements and also event detections from cosmic ray detections, developed by Dr. Glen Langston. See [here](https://github.com/WVURAIL/gr-radio_astro/wiki/Nsf-gr-radio_astro) and the [lightwork memo series](https://wvurail.org/lightwork/) for more details. 
2. DSPIRA software developed for and by High School Teachers part of the [NSF funded RET program called Digital Signal Processing in Radio Astronomy (DSPIRA)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1611114) at WVU university from the summers of 2017 to 2021. For more details visit the [webpage](https://wvurail.org/dspira-lessons/about/) and the companion website called [dspira-lessons](https://wvurail.org/dspira-lessons/) that has lessons, guides and more material help one to use radio astronomy in a high school classroom. This material is designed by the High School teachers part of this program. 

# Installing from Source

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
   
8. Edit your `.bashrc` file and add this to the bottom to set Python path: `export PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3.10/dist-packages:$PYTHONPATH`
9. Additionally you can create appropriate symbolic links
   1.  Check which python is the installed version of GNURadio by opening  `gnuradio-companion` in a terminal window and click on `Help --> About` and noting the python version on the dialog box that opens.  
   2.  Go to the following by typing: `cd /usr/local/lib/python3.10/dist-packages` or `cd /usr/local/lib/python3.9/dist-packages` for the appropriate python version. 
   3.  Type `ln -s /usr/local/lib/python3/dist-packages/radio_astro`   


# Running from a bootable USB Flash Drive with preinstalled software:

[Instructions to set up a persistant USB flash with preinstalled software drive are here](https://wvurail.org//dspira-lessons/Install_Ubuntu_spectrometer_onFlashdrive)

---- 
TODO: Update for 3.10 below the instructions are for 3.8

# Installing on a Raspberry Pi. 

## Supported Raspberry Pi Devices

*All devices must have RAM greater than 4GB*
1. Raspberry Pi 4 Model B
2. Raspberry Pi 400


## Installing Ubuntu image with radio astronomy preinstalled  on a Raspberry Pi
This image requires a minimum of 16GB of space on the SD card. 
1. Download the image [here](https://drive.google.com/file/d/1KzfgMEwgwTTZUaCeNR5kRgLj9MfMKyAh/view?usp=sharing)
2. Unzip the `.zip` file.
3. Use [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to install this image. 
   1. Insert SD card into your card reader on your computer
   2. Open Raspberry Pi imager.
   3. Click `Choose OS`, and choose `Use Custom`. 
   4. Select the correct image file downloaded in step 1 and 2 from your system.
   5. Click `Choose storage` and select your inserted SD card.
   6. Click write. 
   7. More info [here](https://www.raspberrypi.org/documentation/installation/installing-images/) and a [video](https://www.youtube.com/watch?v=ntaXWS8Lk34) 
4. Insert SD card to Raspberry Pi and power it up.
5. The default user name is `pi`, with password `raspberry`. Change the password after first boot. 
