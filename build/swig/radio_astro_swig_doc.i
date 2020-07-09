
/*
 * This file was automatically generated using swig_doc.py.
 *
 * Any changes to it will be lost next time it is regenerated.
 */




%feature("docstring") gr::radio_astro::dedispersion "Dedisperse incoming power spectrum.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radio_astro::dedispersion.

To avoid accidental use of raw pointers, radio_astro::dedispersion's constructor is in a private implementation class. radio_astro::dedispersion::make is the public interface for creating new instances.

Args:
    vec_length : 
    dms : 
    f_obs : 
    bw : 
    t_int : 
    nt : "

%feature("docstring") gr::radio_astro::dedispersion::make "Dedisperse incoming power spectrum.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radio_astro::dedispersion.

To avoid accidental use of raw pointers, radio_astro::dedispersion's constructor is in a private implementation class. radio_astro::dedispersion::make is the public interface for creating new instances.

Args:
    vec_length : 
    dms : 
    f_obs : 
    bw : 
    t_int : 
    nt : "

%feature("docstring") gr::radio_astro::detect "Event Detection by comparison of signal to RMS Noise level. event detection: fill a circular buffer with complex samples and search for peaks nsigma above the RMS of the data stream input: complex vector of I/Q samples parameters.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radio_astro::detect.

To avoid accidental use of raw pointers, radio_astro::detect's constructor is in a private implementation class. radio_astro::detect::make is the public interface for creating new instances.

Args:
    vec_length : 
    dms : 
    f_obs : 
    bw : 
    t_int : 
    nt : "











%feature("docstring") gr::radio_astro::detect::make "Event Detection by comparison of signal to RMS Noise level. event detection: fill a circular buffer with complex samples and search for peaks nsigma above the RMS of the data stream input: complex vector of I/Q samples parameters.

Constructor Specific Documentation:

Return a shared_ptr to a new instance of radio_astro::detect.

To avoid accidental use of raw pointers, radio_astro::detect's constructor is in a private implementation class. radio_astro::detect::make is the public interface for creating new instances.

Args:
    vec_length : 
    dms : 
    f_obs : 
    bw : 
    t_int : 
    nt : "

%feature("docstring") gr::radio_astro::vmedian "Vector Median of several vectors. For 3 or 4 vectors the code implements exactly the median of the values for more vectors, the result is the sum of all values minus the miniumum and maximum values input: vector of length vector_lenght parameters.

Constructor Specific Documentation:



Args:
    vec_length : 
    n : "

%feature("docstring") gr::radio_astro::vmedian::set_vlen "Return a shared_ptr to a new instance of radio_astro::vmedian.

To avoid accidental use of raw pointers, radio_astro::vmedian's constructor is in a private implementation class. radio_astro::vmedian::make is the public interface for creating new instances."



%feature("docstring") gr::radio_astro::vmedian::make "Vector Median of several vectors. For 3 or 4 vectors the code implements exactly the median of the values for more vectors, the result is the sum of all values minus the miniumum and maximum values input: vector of length vector_lenght parameters.

Constructor Specific Documentation:



Args:
    vec_length : 
    n : "