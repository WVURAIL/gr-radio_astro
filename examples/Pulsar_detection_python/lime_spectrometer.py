import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import h5py
from scipy.fftpack import fft
#import pyfftw

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)

#query device info
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs: print(freqRange)

#apply settings
samp_rate =20e6
sdr.setSampleRate(SOAPY_SDR_RX, 0, samp_rate)
sdr.setFrequency(SOAPY_SDR_RX, 0, 1420e6)
sdr.setGain(SOAPY_SDR_RX, 0, 53)
sdr.setAntenna(SOAPY_SDR_RX,0, "LNAW")

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

vec_length = 2040*2  #2040
#create a re-usable buffer for rx samples
buff = numpy.array([0]*vec_length, numpy.complex64)  #lime packet are 1020 I think
#buff = pyfftw.empty_aligned(vec_length, dtype='complex64')

sr = sdr.readStream(rxStream, [buff], len(buff))
t1 = sr.timeNs


#test for just receive some samples
# while True:
#     sr = sdr.readStream(rxStream, [buff], len(buff))
#     #print(sr.ret) #num samples or error code
#     #print(sr.flags) #flags set by receive operation
#     deltat = (sr.timeNs - t1)/dt
#     if deltat > 1:
#         print(deltat) #timestamp for receive buffer
#     t1 = sr.timeNs
    

h5 = h5py.File("livenoisefile.h5", 'w')

spectrumDataset = h5.create_dataset('timestream', (1,vec_length), dtype=numpy.complex64, maxshape=(None,vec_length))
timeDataset = h5.create_dataset('timestampNs', (1,1), dtype=numpy.uint64, maxshape=(None,1))
n_times = 1
n = 0
integrations = 20
dt =  integrations*vec_length /samp_rate*1e9#nanoseconds
integrated_spectrum = numpy.array([0]*vec_length, numpy.complex64)
#spec1 = pyfftw.empty_aligned(vec_length, dtype='complex64')

while True:
    for i in range(integrations):
        sr = sdr.readStream(rxStream, [buff], len(buff))
        spec1 = fft(buff)
        #spec1 = pyfftw.interfaces.numpy_fft.fft(buff)
        spec1 = spec1*spec1.conjugate()
        integrated_spectrum +=  spec1
    if n == n_times:
        n_times = n+1
        timeDataset.resize((n_times,1))
        #self.inputDataset.resize((self.n_times, 1))
        spectrumDataset.resize((n_times,vec_length))
    else:
        pass
    #print( n_times) #debugging.  remove
    timeDataset[n] = sr.timeNs
    #inputDataset[self.n] = in_num
    spectrumDataset[n] = integrated_spectrum
    n += 1
    deltat = (sr.timeNs - t1)/dt
    if deltat > 1:
        print(deltat) #timestamp for receive buffer
    t1 = sr.timeNs
    integrated_spectrum = 0*integrated_spectrum

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)

#h5.close()
