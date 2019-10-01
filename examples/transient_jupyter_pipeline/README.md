# Jupyter Notebooks
There are currently multiple jupyter python notebooks for pulse simulation and detection. They are described below in order of development in the pipeline


*Pulsar SImulator_10MHz_PSRB0329+54 -- the initial pulsar simulator. This has steps of analogue chain, dispersion, and save file as described below.


* Pulsar SImulator_10MHz_PSRB0329+54_second_noise_reduction_technique. -- The first attempt to reduce the simulated pulsar. 
 * The analogue, dispersion, and first dedispersion attempt were done


* Pulsar SImulator_10MHz_PSRB0329+54_correct dispersion_technique -- The correct dedispersion algorithm was made.
 * The analogue, dispersion, and first dedispersion attempt were done


* Pulsar SImulator_10MHz_PSRB0329+54_final_before_optimization -- All parts of the initial detection algorithm for the simulated pulse were made.
 * Consists of all steps below with the following changes to Detection
 
 *Detection (previous)*

* A matched filter is created to find the pulsar and best DM
 * The filter used is a Gaussian pulse because the noise is uncorreclated white noise
  * In the future, a 3d matched filter will be created instead of a 2d matched filter
  * The pulse is made with variance `pw/(period/packet_length)`
   *Packet length is `int(len(downsampled_filtered_mixed_down)/step/integration_size)`
 * The Gaussian is made with the same equation to make the distribution in the analogue chain above

* The new filter is cross correlated with the dedispersed data.
 * Correlation done using `numpy.correlate`
 * The arguments of the correlation function are the data containing the pulse, the filter, and the mode of correlation.
  * The order of the arguments must be in this order. 
  *  For signal, the output needs to be the same shape as the input, so `mode='same'` is the final argument
  * For noise, the output must be only as a result of real cross correlation, so `mode=real`.

* The peaks of the cross correlated noise is calcualted by using a peak finding function
 *Takes two argument, the data and the the threshold above which peaks will be found
 * The array used for the data must have at least two dimensions, where the first is the DM being tested, and the second is the number of data points. 
 * `len(threshold)` must be equal to `len(DMs)`, since the threshold should change slightly for each DM. 
* Then the average value of the peaks is found

* The std and mean of the noise is found by using `numpy.std` and `numpy.mean` on the correlated noise.

* The SNR is calculated.
 * This determines if a pulsar has been detected
 * Calculated by  (y_{av}-noise_mean)/noise_std
 *The noise is subtracted from the peaks and then divided by the std
 * If SNR is above 10, for more than five data points, then a pulsar of FRB has been detected.
  * This is to ensure that with higher amplitude, non white noise, stray signals will not be mistaken for a pulsar.


* Pulsar_Detection_Pipeline -- The detection pipeline which uses pulsar data rather than a pulsar simulation
 * The most up to date pipeline which is descibed below


* Pulsar_Simulation_Detection -- an application of the pulsar detection pipeline to the simulated pulsar.
 * Only difference between the two is the simulated pulsar code.

------------------------------------------------------------------------------------------------------------------------------------------------
The entire process of FRB and pulsar detection, from pulse simulation to dedispersion is simulated through the latest python document, which as of now is "Pulsar SImulator_10MHz_PSRB0329+54_final_before_optimization.ipynb".

* The initial parameters for the pulse are chosen. They are as follows:

1. Centre Frequency: 1400MHz
2. Bandwidth: 10MHz
3. Frequency simulation pulse was run at: 1200MHz
4. Period: .005s
5. Pulse Width .0004s

* These values can change, and they are up to the individual to choose.

*The analogue chain is simulated.*
* The sample rate at which the telescope is set to 12GHz.
* An array with an amplitude of +-period and length of `sampling_rate*period` is made and is defined as `t`.This is the pulse timestep.
* A normal distribution of values that have a variance of 1 and a mean of 0 are produced to simulate the gaussian pulse packet. 
* Next a Gaussian function of points is created using `G = e^{-\frac{x^2}{2*pw^2}}`
 *  `t` is the spread of values: the independent variable x
 * `pw`,(the pulse width) is the variance.
* The two arrays, gaussian and normal, are  multiplied together to create a Gaussian distribution of points: a Gaussian noise packet.

* All frequencies outside of our bandwidth are ignored by taking an FFT of the data and then applying a filter.
 * The FFT gives broadband noise.
 * The filter is used to eliminate all frequencies except for those defined within our desired bandwidth.
  * The bandwidth is centered around +-1400MHz thus we will have two intervals of points that we wish to keep. 
  * All other frequencies are given an amplitude of zero.

* The IFFT of the resulting signal is taken , returning a Gaussian pulse in the time domain which is defined as `blimited_pulse`. 

* IQ sampling and mixing are performed
 * The mixing signal is made from Euler's equation:  `mixing_signal = np.exp(-2.00j*np.pi* Cf/sample_rate *np.arange(length))`
  * The `Cf` is the centre frequency given in Hz.
  * `sample_rate` is the rate of sampling. 
  * It is assumed that this mixing signal is centred about 0. 
 * The pulse and the mixing signal are multiplied together and another FFT is taken.
 * A low pass filter called `N_cutoff` is defined and applied to the FFT
  *This is to prevent the sampled up data from being in the mixed data set that is called `f_mixed`.
 * The data is downsampled by taking the IFFT and defining a new array which takes values from the `f_mixed` set at intervals of `sample_rate/Bw`
  * `Bw` is the Bandwidth in Hz. 
  *This array is called `downsampled_filtered_mixed_down_s`

* The analogue chain has been completed.

*Dispersion*

* This pulse is dispersed as it travels through space, and so the simulated pulse must be dispersed as well.
 * If a pulsar is what is desired, then `numpy.tile` is used to create n copies of the argument and concatenate the argument and the copies. 
* The pulsar is dispersed by defining the number of frequency samples in the bandwidth called `stepfreq_step`. 
* The time delay in seconds is given by `t = 4.15e3*DM*(v_1^-2 - v_2^2)` 
 * This delay time must be significantly less than the dispersion time of the data. 
* The FFT of this is taken, and convolved with the FFT of the `downsampled_filtered_mixed_down` then the IFFT of the convolution is taken 
 * A note to be careful of: in order to achieve an FFT and IFFT without an overall gain change, it needs to be specified in the arguments of the IFFT and FFT functions that `norm='ortho'`.
*The pulse is now dispersed

*Add noise*

* Assume noncorrelated noise is what is included with the pulse. 
 * Will allow a simple template to be used for a matched filter. 
* The added noise is concatenated to the noise and signal
 * This is meant to simulate looking away from the pulsar and then looking onto it.

*Save File*


* The data is saved as an int16 file and this is what is used as the GNUradio simulation. 
 * The ratio of the maximum amplitude in the data set and the length of an int16 file is multiplied to the whole data set.

* To ensure that the exact same data is being processed in both GNUradio and the Jupyter notebook, the array that was used to create the saved file, is used for the rest of the simulation. 
 *The noise is also multiplied by the same constant as the previously mentioned file.

*Dedispersion*

* To see the dispersion of the pulse, the FFT of the array is taken and then integrated. 
 * The number of frequency channels is arbitrary; in the notebook, the value was set to 400 channels and labeled as `step`. 
 * The integration time for the data must be less than the pulse width of our observed pulse.
  * Found by taking `len_signal/n_freq/int_time`
 * The FFT is looped and done at 400 step intervals. The FFTed array is multiplied to its complex conjugate. 
  * This process is done n times, where n is given by the `dispersed_downsampled_filtered_mixed_signal` array over the ``steps * the number of integrations``.

* SNR can be estimated using the peak of the pulse before it was dispersed, and the variance used to create the white noise. 
 *Will be used later to compare to the calculated SNR.
* We save all of the FFTed and integrated data, which I called `rec_spect`, to an int16 file, so that bench testing can be compared to the FFT and integrate blocks in GNUradio.

* `rec_spect` is run  through np.fft.fftshift, which shifts the frequencies so that they go from negative to positive. 
 * The array was also transposed and flipped so that time would be on the x axis of the imshow plots. The x axis ranges were also defined using numpy.fft.fftfreq and fft.fftshift.

* The time delay of the pulse is calculated
 * Done by using the equation originally used to dedisperse the pulse to find the delay for every frequency. 
 * Multiple DMs are tested to show that many can be searched in the case of an unknown pulsar to find the corrrect DM
* The number of time samples and total time are divided into each change in time above.
 * Tells how many bins to shift.
* When performed for every dispersion measure, a 2D array is yielded to be used in numpy.roll. 
 * Shifts the data for every DM option.

*Creating DM Vs Time*

* To get a 2d array of DMs vs time, the sum along the frequency axis is taken. 
 * If the data is plotted with `numpy.imshow`, then a bow tie shape can be seen. 
 * The correct DM is the one that has the highest amplitude. 
 *There is a slight error for which DM has the highest DM, which is thought to be a result of how the pulse was simulated

*Detection (current)*
 * An fft of the data is taken
 * The signal is then run through a tukey window,in order to reduce the noise present at the beginning of the power spectrum]
 
 * Two possible detection algorithms are used. The first is if the period of the object is known.
  * If this is the case, then the power spectrum is folded along the period in order to find the average pulse over iterations
  * There is some variation with the number of bins between each spike, so an algorithm is created to moniter the changing bin distances between the pulses
  * After the pulses are summed, the entire summed array is divided by the number of iterations through the pulse period
  * Then noise is created since at present, no there is no purely noise file from the telescope
   * This is done by removing any point more than three std from the mean and replacing it with the mean of the data
  * Finally the DNR is found by finding the max point of each summed peak per DM, and by subtracting the noise mean from it then dividing it by the noise std.
 
 
 * The other method is if the period of the pulsar is not known.
  * A matched filter is created to find the pulsar and best DM
  * The filter used is a Gaussian pulse because the noise is uncorreclated white noise
   * In the future, a 3d matched filter will be created instead of a 2d matched filter

 * The new filter is cross correlated with the dedispersed data.
  * Correlation done using `numpy.correlate`
  * The arguments of the correlation function are the data containing the pulse, the filter, and the mode of correlation.
   * The order of the arguments must be in this order. 
   *  For signal, the output needs to be the same shape as the input, so `mode='same'` is the final argument
   * For noise, the output must be only as a result of real cross correlation, so `mode=real`.
  
  * Again, the noise is artificially created by turning points more than 3 std of the mean of the data into the a value equal to the mean of the data.

 * The peaks of the cross correlated noise is calcualted by using a peak finding function
  *Takes two argument, the data and the the threshold above which peaks will be found
  * The array used for the data must have at least two dimensions, where the first is the DM being tested, and the second is the number of data points. 
  * `len(threshold)` must be equal to `len(DMs)`, since the threshold should change slightly for each DM. 
 * Then the average value of the peaks is found

 * The std and mean of the noise is found by using `numpy.std` and `numpy.mean` on the correlated noise.

 * The SNR is calculated.
  * This determines if a pulsar has been detected
  * Calculated by  (y_{av}-noise_mean)/noise_std
  * The noise is subtracted from the peaks and then divided by the std
  * If SNR is above 10, for more than five data points, then a pulsar of FRB has been detected.
   * This is to ensure that with higher amplitude, non white noise, stray signals will not be mistaken for a pulsar.
