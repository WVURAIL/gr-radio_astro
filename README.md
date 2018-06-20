# gr-radio_astro

##

Modules and blocks here to help create a grc flowchart for use in radio astronomy.  

## Installation

1.) Clone the repository into an appropriate folder/repository: 

``git clone https://github.com/WVURAIL/gr-radio_astro.git``

2.) Go to the ``gr-radio_astro`` folder/repository, create a build directory inside the repository:

``
cd gr-radio_astro
``

``
mkdir build
`` 

3.)  run cmake inside the build directory:

``cd build;  cmake ..``

4.) run make inside build directory

``make``

5.)  If no errors, install

``make install``

Blocks should now be available in gnuradio-companion.
 
 **Additionally install h5py**
 
 On Ubuntu can run:
 
 ``sudo apt install python-h5py``
 
 Generic linux can try:
 
 ``sudo pip install h5py``
