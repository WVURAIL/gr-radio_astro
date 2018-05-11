# -*- coding:utf-8 -*-
"""Classes for representing angles, and positions on a unit sphere.

This module provides three classes for representing angles: `Angle`,
`AlphaAngle` and `DeltaAngle`, and one class for representing a point
on a unit sphere, `AngularPosition`.

par`Angle` is for representing generic angles. `AlphaAngle` is for
representing longitudinal angles such as geographic longitude, right
ascension and others. `DeltaAngle` is for representing latitudinal
angles such as geographic latitude, declination and others.

An angle object can be initialized with value in various units, it can
normalize its value into an appropriate range. The value can be
retrieved in various units, using appropriately named attributes.

Sexagesimal representation of an angle can be obtained through
appropriate attributes of the angle object. The number of decimal
places in the final part of a sexagesimal representation, and whether
rounding or truncation is used to produce these many decimal places,
can be customized.

An angle object can provide string representation of itself. The
delimiters used in the string representation can be customized. The
string representation is based on the sexagesimal value and hence it
also reflects the precision and truncation settings.

The `AngularPosition` class can be used for representing points on a
sphere. It uses an `AlphaAngleSphere` instance for storing the longitudinal
angle, and a `DeltaAngleSphere` instance for storing the latitudinal angle.
The input values of angular coordinates are normalized to the simplest values.

It can calcuate the separation and bearing, also called position angle,
to another point on the sphere. The results for separation and
bearing agree with those from the SLALIB (pyslalib) library. See tests in
``test_angles.py`` for more details.

The separation and bearing calculations do not use spherical
trignometry. They involve Cartesian vectors, and instances of the class
`CartesianVector` are used for these calculations.

See docstrings of classes and methods for more details.

Almost all the methods of the classes call functions for performing
calculations. If needed these functions can be used directly.

Functions include those for converting angles between different units,
parsing sexagesimal strings, creating string representations of angles,
converting angles between various units, normalizing angles into a
given range, finding separation and bearing bewteen two points and
others. Normalization of angles can be performed in two different
ways. One method normalizes angles in the manner that longitudinal
angles are normalized i.e., [0, 360.0) or [0, 2π) or [0, 24.0). The
other method normalizes angles in the manner that latitudinal angles
are normalized i.e., [-90, 90] or [-π/2, π/2].

See docstrings of classes and functions for documentation and examples.

:author: Prasanth Nair
:contact: prasanthhn@gmail.com
:license: BSD (http://www.opensource.org/licenses/bsd-license.php)
"""
import warnings
import math
import re

__version__ = "2.0"


def r2d(r):
    """Convert radians into degrees."""
    return math.degrees(r)


def d2r(d):
    """Convert degrees into radians."""
    return math.radians(d)


def h2d(h):
    """Convert hours into degrees."""
    return h * 15.0


def d2h(d):
    """Convert degrees into hours."""
    return d * (24.0 / 360.0)


def arcs2d(arcs):
    """Convert arcseconds into degrees."""
    return arcs / 3600.0


def d2arcs(d):
    """Convert degrees into arcseconds."""
    return d * 3600.0


def h2r(h):
    """Convert hours into radians."""
    return d2r(h2d(h))


def r2h(r):
    """Convert radians into hours."""
    return d2h(r2d(r))


def arcs2r(arcs):
    """Convert arcseconds into radians."""
    return d2r(arcs2d(arcs))


def r2arcs(r):
    """Convert radians into arcseconds."""
    return d2arcs(r2d(r))


def arcs2h(arcs):
    """Convert arcseconds into hours."""
    return d2h(arcs2d(arcs))


def h2arcs(h):
    """Convert hours into arcseconds."""
    return d2arcs(h2d(h))


def normalize(num, lower=0, upper=360, b=False):
    """Normalize number to range [lower, upper) or [lower, upper].

    Parameters
    ----------
    num : float
        The number to be normalized.
    lower : int
        Lower limit of range. Default is 0.
    upper : int
        Upper limit of range. Default is 360.
    b : bool
        Type of normalization. Default is False. See notes.

        When b=True, the range must be symmetric about 0.
        When b=False, the range must be symmetric about 0 or ``lower`` must
        be equal to 0.

    Returns
    -------
    n : float
        A number in the range [lower, upper) or [lower, upper].

    Raises
    ------
    ValueError
      If lower >= upper.

    Notes
    -----
    If the keyword `b == False`, then the normalization is done in the
    following way. Consider the numbers to be arranged in a circle,
    with the lower and upper ends sitting on top of each other. Moving
    past one limit, takes the number into the beginning of the other
    end. For example, if range is [0 - 360), then 361 becomes 1 and 360
    becomes 0. Negative numbers move from higher to lower numbers. So,
    -1 normalized to [0 - 360) becomes 359.

    When b=False range must be symmetric about 0 or lower=0.

    If the keyword `b == True`, then the given number is considered to
    "bounce" between the two limits. So, -91 normalized to [-90, 90],
    becomes -89, instead of 89. In this case the range is [lower,
    upper]. This code is based on the function `fmt_delta` of `TPM`.

    When b=True range must be symmetric about 0.

    Examples
    --------
    >>> normalize(-270,-180,180)
    90.0
    >>> import math
    >>> math.degrees(normalize(-2*math.pi,-math.pi,math.pi))
    0.0
    >>> normalize(-180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180)
    -180.0
    >>> normalize(180, -180, 180, b=True)
    180.0
    >>> normalize(181,-180,180)
    -179.0
    >>> normalize(181, -180, 180, b=True)
    179.0
    >>> normalize(-180,0,360)
    180.0
    >>> normalize(36,0,24)
    12.0
    >>> normalize(368.5,-180,180)
    8.5
    >>> normalize(-100, -90, 90)
    80.0
    >>> normalize(-100, -90, 90, b=True)
    -80.0
    >>> normalize(100, -90, 90, b=True)
    80.0
    >>> normalize(181, -90, 90, b=True)
    -1.0
    >>> normalize(270, -90, 90, b=True)
    -90.0
    >>> normalize(271, -90, 90, b=True)
    -89.0
    """
    if lower >= upper:
        ValueError("lower must be lesser than upper")
    if not b:
        if not ((lower + upper == 0) or (lower == 0)):
            raise ValueError('When b=False lower=0 or range must be symmetric about 0.')
    else:
        if not (lower + upper == 0):
            raise ValueError('When b=True range must be symmetric about 0.')

    from math import floor, ceil
    # abs(num + upper) and abs(num - lower) are needed, instead of
    # abs(num), since the lower and upper limits need not be 0. We need
    # to add half size of the range, so that the final result is lower +
    # <value> or upper - <value>, respectively.
    res = num
    if not b:
        res = num
        if num > upper or num == lower:
            num = lower + abs(num + upper) % (abs(lower) + abs(upper))
        if num < lower or num == upper:
            num = upper - abs(num - lower) % (abs(lower) + abs(upper))

        res = lower if num == upper else num
    else:
        total_length = abs(lower) + abs(upper)
        if num < -total_length:
            num += ceil(num / (-2 * total_length)) * 2 * total_length
        if num > total_length:
            num -= floor(num / (2 * total_length)) * 2 * total_length
        if num > upper:
            num = total_length - num
        if num < lower:
            num = -total_length - num

        res = num

    res *= 1.0  # Make all numbers float, to be consistent

    return res


def d2d(d):
    """Normalize angle in degree to [0, 360)."""
    return normalize(d, 0, 360)


def h2h(h):
    """Normalize angle in hours to [0, 24.0)."""
    return normalize(h, 0, 24)


def r2r(r):
    """Normalize angle in radians to [0, 2π)."""
    return normalize(r, 0, 2 * math.pi)


def deci2sexa(deci, pre=3, trunc=False, lower=None, upper=None,
              b=False, upper_trim=False):
    """Returns the sexagesimal representation of a decimal number.

    Parameters
    ----------
    deci : float
        Decimal number to be converted into sexagesimal. If `lower` and
        `upper` are given then the number is normalized to the given
        range before converting to sexagesimal.
    pre : int
        The last part of the sexagesimal number is rounded to these
        many decimal places. This can be negative. Default is 3.
    trunc : bool
        If True then the last part of the sexagesimal number is
        truncated and not rounded to `pre` decimal places. Default is
        False.
    lower : int
        Lower bound of range to which number is to be normalized.
    upper : int
        Upper bound of range to which number is to be normalized.
    b : bool
        Affects type of normalization. See docstring for `normalize`.
    upper_trim : bool
        If `lower` and `upper` are given and this is True, then if the
        first part of the sexagesimal number is equal to `upper`, it is
        replaced with `lower` (value used is int(lower)). This converts numbers
        such as "24 00 00.000" to "00 00 00.000". Default value is False.

    Returns
    -------
    s : 4 element tuple; (int, int, int, float)
        A tuple of sign and the three parts of the sexagesimal
        number. Sign is 1 for positive and -1 for negative values. The
        sign applies to the whole angle and not to any single part,
        i.e., all parts are positive and the sign multiplies the
        angle. The first and second parts of the sexagesimal number are
        integers and the last part is a float.

    Notes
    -----
    The given decimal number `deci` is converted into a sexagesimal
    number. The last part of the sexagesimal number is rounded to `pre`
    number of decimal points. If `trunc == True` then instead of
    rounding, the last part is truncated.

    If `lower` and `upper` are given then the number is normalized to
    the given range before converting into sexagesimal format. The `b`
    argument determines the type of normalization. See docstring of the
    `normalize` function for details.

    If `upper_trim` is True then, if after convertion to sexagesimal
    the first part is equal to `upper`, it is replaced with `lower` (value used
    is int(lower)). This is useful in cases where numbers such as "24 00 00.00"
    needs to be converted into "00 00 00.00"

    The returned sign, first element of tuple, applies to the whole
    number and not just to a single part.

    Examples
    --------
    >>> deci2sexa(-11.2345678)
    (-1, 11, 14, 4.444)
    >>> deci2sexa(-11.2345678, pre=5)
    (-1, 11, 14, 4.44408)
    >>> deci2sexa(-11.2345678, pre=4)
    (-1, 11, 14, 4.4441)
    >>> deci2sexa(-11.2345678, pre=4, trunc=True)
    (-1, 11, 14, 4.444)

    >>> deci2sexa(-11.2345678, pre=1)
    (-1, 11, 14, 4.4)
    >>> deci2sexa(-11.2345678, pre=0)
    (-1, 11, 14, 4.0)
    >>> deci2sexa(-11.2345678, pre=-1)
    (-1, 11, 14, 0.0)

    >>> x = 23+59/60.0+59.99999/3600.0

    To 3 decimal places, this number is 24 or 0 hours.

    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=True)
    (1, 0, 0, 0.0)
    >>> deci2sexa(x, pre=3, lower=0, upper=24, upper_trim=False)
    (1, 24, 0, 0.0)

    To 5 decimal places, we get back the full value.

    >>> deci2sexa(x, pre=5, lower=0, upper=24, upper_trim=True)
    (1, 23, 59, 59.99999)

    """
    if lower is not None and upper is not None:
        deci = normalize(deci, lower=lower, upper=upper, b=b)

    sign = 1
    if deci < 0:
        deci = abs(deci)
        sign = -1

    hd, f1 = divmod(deci, 1)
    mm, f2 = divmod(f1 * 60.0, 1)
    sf = f2 * 60.0

    # Find the seconds part to required precision.
    fp = 10 ** pre
    if trunc:
        ss, _ = divmod(sf * fp, 1)
    else:
        ss = round(sf * fp, 0)

    ss = int(ss)

    # If ss is 60 to given precision then update mm, and if necessary
    # hd.
    if ss == 60 * fp:
        mm += 1
        ss = 0
    if mm == 60:
        hd += 1
        mm = 0

    hd = int(hd)
    mm = int(mm)
    if lower is not None and upper is not None and upper_trim:
        # For example 24h0m0s => 0h0m0s.
        if hd == upper:
            hd = int(lower)

    if hd == 0 and mm == 0 and ss == 0:
        sign = 1

    ss /= float(fp)
    # hd and mm parts are integer values but of type float
    return (sign, hd, mm, ss)


def sexa2deci(sign, hd, mm, ss, todeg=False):
    """Combine sexagesimal components into a decimal number.

    Parameters
    ----------
    sign : int
        Sign of the number: 1 for +ve, -1 for negative.
    hd : float
        The hour or degree like part.
    mm : float
        The minute or arc-minute like part.
    ss : float
        The second or arc-second like part.
    todeg : bool
        If True then convert to degrees, assuming that the input value
        is in hours. Default is False.

    Returns
    -------
    d : float
        The decimal equivalent of the sexagesimal number.

    Raises
    ------
    ValueError
        This exception is raised if `sign` is not -1 or 1.

    Notes
    -----
    The angle returned is::

      sign * (hd + mm / 60.0 + ss / 3600.0)

    In sexagesimal notation the sign applies to the whole quantity and
    not to each part separately. So the `sign` is asked separately, and
    applied to the whole quantity.

    If the sexagesimal quantity is in hours, then we frequently want to
    convert it into degrees. If the `todeg == True` then the given
    value is assumed to be in hours, and the returned value will be in
    degrees.

    Examples
    --------
    >>> d = sexa2deci(1,12,0,0.0)
    >>> d
    12.0
    >>> d = sexa2deci(1,12,0,0.0,todeg=True)
    >>> d
    180.0
    >>> x = sexa2deci(1,9,12.456,0.0)
    >>> assert round(x,4) == 9.2076
    >>> x  = sexa2deci(1,11,30,27.0)
    >>> assert round(x, 4) == 11.5075
    """
    divisors = [1.0, 60.0, 3600.0]
    d = 0.0
    # sexages[0] is sign.
    if sign not in (-1, 1):
        raise ValueError("Sign has to be -1 or 1.")

    sexages = [sign, hd, mm, ss]
    for i, divis in zip(sexages[1:], divisors):
        d += i / divis

    # Add proper sign.
    d *= sexages[0]

    if todeg:
        d = h2d(d)

    return d


def fmt_angle(val, s1=" ", s2=" ", s3="", pre=3, trunc=False,
              lower=None, upper=None, b=False, upper_trim=False):
    """Return sexagesimal string of given angle in degrees or hours.

    Parameters
    ----------
    val : float
        The angle (in degrees or hours) that is to be converted into a
        sexagesimal string.
    s1 : str
        Character to be used between the first and second parts of the
        the sexagesimal representation.
    s2 : str
        Character to be used between the second and third parts of the
        the sexagesimal representation.
    s3 : str
        Character to be used after the third part of the sexagesimal
        representation.
    pre : int
        The final part of the sexagesimal number is rounded to these
        many decimal places. This can be negative.
    trunc : bool
        If True then the third part of the sexagesimal number is
        truncated to `pre` decimal places, instead of rounding.
    lower, upper : float
        If `lower` and `upper` are given then the given value is
        normalized into the this range before converting to sexagesimal
        string.
    b : bool
        This affect how the normalization is performed. See notes. This
        works exactly like that for the function `normalize()`.
    upper_trim : bool
        If `lower` and `upper` are given, then if the first part of the
        sexagesimal number equals `upper`, it is replaced with
        `lower`. For examples, "12 00 00" gets turned into "00 00
        00".

    See also
    --------
    normalize
    deci2sexa

    Examples
    --------
    >>> fmt_angle(12.348978659, pre=4, trunc=True)
    '+12 20 56.3231'
    >>> fmt_angle(12.348978659, pre=5)
    '+12 20 56.32317'
    >>> fmt_angle(12.348978659, s1='HH ', s2='MM ', s3='SS', pre=5)
    '+12HH 20MM 56.32317SS'

    >>> x = 23+59/60.0+59.99999/3600.0
    >>> fmt_angle(x)
    '+24 00 00.000'
    >>> fmt_angle(x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000'
    >>> fmt_angle(x, pre=5)
    '+23 59 59.99999'
    >>> fmt_angle(-x, lower=0, upper=24, upper_trim=True)
    '+00 00 00.000'
    >>> fmt_angle(-x)
    '-24 00 00.000'

    """
    x = deci2sexa(val, pre=pre, trunc=trunc, lower=lower, upper=upper,
                  upper_trim=upper_trim, b=b)

    left_digits_plus_deci_point = 3 if pre > 0 else 2
    p = "{3:0" + "{0}.{1}".format(pre + left_digits_plus_deci_point, pre) + "f}" + s3
    p = "{0}{1:02d}" + s1 + "{2:02d}" + s2 + p

    return p.format("-" if x[0] < 0 else "+", *x[1:])


def phmsdms(hmsdms):
    """Parse a string containing a sexagesimal number.

    This can handle several types of delimiters and will process
    reasonably valid strings. See examples.

    Parameters
    ----------
    hmsdms : str
        String containing a sexagesimal number.

    Returns
    -------
    d : dict

        parts : a 3 element list of floats
            The three parts of the sexagesimal number that were
            identified.
        vals : 3 element list of floats
            The numerical values of the three parts of the sexagesimal
            number.
        sign : int
            Sign of the sexagesimal number; 1 for positive and -1 for
            negative.
        units : {"degrees", "hours"}
            The units of the sexagesimal number. This is infered from
            the characters present in the string. If it a pure number
            then units is "degrees".

    Examples
    --------
    >>> phmsdms("12") == {
    ... 'parts': [12.0, None, None],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 0.0, 0.0]
    ... }
    True

    >>> phmsdms("12h") == {
    ... 'parts': [12.0, None, None],
    ... 'sign': 1,
    ... 'units': 'hours',
    ... 'vals': [12.0, 0.0, 0.0]
    ... }
    True

    >>> phmsdms("12d13m14.56") == {
    ... 'parts': [12.0, 13.0, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 13.0, 14.56]
    ... }
    True

    >>> phmsdms("12d13m14.56") == {
    ... 'parts': [12.0, 13.0, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 13.0, 14.56]
    ... }
    True

    >>> phmsdms("12d14.56ss") == {
    ... 'parts': [12.0, None, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [12.0, 0.0, 14.56]
    ... }
    True

    >>> phmsdms("14.56ss") == {
    ... 'parts': [None, None, 14.56],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ... 'vals': [0.0, 0.0, 14.56]
    ... }
    True

    >>> phmsdms("12h13m12.4s") == {
    ... 'parts': [12.0, 13.0, 12.4],
    ... 'sign': 1,
    ... 'units': 'hours',
    ... 'vals': [12.0, 13.0, 12.4]
    ... }
    True

    >>> phmsdms("12:13:12.4s") == {
    ... 'parts': [12.0, 13.0, 12.4],
    ... 'sign': 1,
    ... 'units': 'degrees',
    ...  'vals': [12.0, 13.0, 12.4]
    ... }
    True

    But `phmsdms("12:13mm:12.4s")` will not work.

    """
    units = None
    sign = None
    # Floating point regex:
    # http://www.regular-expressions.info/floatingpoint.html
    #
    # pattern1: find a decimal number (int or float) and any
    # characters following it upto the next decimal number.  [^0-9\-+]*
    # => keep gathering elements until we get to a digit, a - or a
    # +. These three indicates the possible start of the next number.
    pattern1 = re.compile(r"([-+]?[0-9]*\.?[0-9]+[^0-9\-+]*)")

    # pattern2: find decimal number (int or float) in string.
    pattern2 = re.compile(r"([-+]?[0-9]*\.?[0-9]+)")

    hmsdms = hmsdms.lower()
    hdlist = pattern1.findall(hmsdms)

    parts = [None, None, None]

    def _fill_right_not_none():
        # Find the pos. where parts is not None. Next value must
        # be inserted to the right of this. If this is 2 then we have
        # already filled seconds part, raise exception. If this is 1
        # then fill 2. If this is 0 fill 1. If none of these then fill
        # 0.
        rp = reversed(parts)
        for i, j in enumerate(rp):
            if j is not None:
                break
        if i == 0:
            # Seconds part already filled.
            raise ValueError("Invalid string.")
        elif i == 1:
            parts[2] = v
        elif i == 2:
            # Either parts[0] is None so fill it, or it is filled
            # and hence fill parts[1].
            if parts[0] is None:
                parts[0] = v
            else:
                parts[1] = v

    for valun in hdlist:
        try:
            # See if this is pure number.
            v = float(valun)
            # Sexagesimal part cannot be determined. So guess it by
            # seeing which all parts have already been identified.
            _fill_right_not_none()
        except ValueError:
            # Not a pure number. Infer sexagesimal part from the
            # suffix.
            if "hh" in valun or "h" in valun:
                m = pattern2.search(valun)
                parts[0] = float(valun[m.start():m.end()])
                units = "hours"
            if "dd" in valun or "d" in valun:
                m = pattern2.search(valun)
                parts[0] = float(valun[m.start():m.end()])
                units = "degrees"
            if "mm" in valun or "m" in valun:
                m = pattern2.search(valun)
                parts[1] = float(valun[m.start():m.end()])
            if "ss" in valun or "s" in valun:
                m = pattern2.search(valun)
                parts[2] = float(valun[m.start():m.end()])
            if "'" in valun:
                m = pattern2.search(valun)
                parts[1] = float(valun[m.start():m.end()])
            if '"' in valun:
                m = pattern2.search(valun)
                parts[2] = float(valun[m.start():m.end()])
            if ":" in valun:
                # Sexagesimal part cannot be determined. So guess it by
                # seeing which all parts have already been identified.
                v = valun.replace(":", "")
                v = float(v)
                _fill_right_not_none()
        if not units:
            units = "degrees"

    # Find sign. Only the first identified part can have a -ve sign.
    for i in parts:
        if i and i < 0.0:
            if sign is None:
                sign = -1
            else:
                raise ValueError("Only one number can be negative.")

    if sign is None:  # None of these are negative.
        sign = 1

    vals = [abs(i) if i is not None else 0.0 for i in parts]

    return dict(sign=sign, units=units, vals=vals, parts=parts)


def pposition(hd, details=False):
    """Parse string into angular position.

    A string containing 2 or 6 numbers is parsed, and the numbers are
    converted into decimal numbers. In the former case the numbers are
    assumed to be floats. In the latter case, the numbers are assumed
    to be sexagesimal.

    Parameters
    ----------
    hd: str
      String containing 2 or 6 numbers. The numbers can be spearated
      with character or characters other than ".", "-", "+".

      The string must contain either 2 or 6 numbers.

    details: bool
      The detailed result from parsing the string is returned. See
      "Returns" section below.

      Default is False.

    Returns
    -------
    x: (float, float) or dict
      A tuple containing decimal equivalents of the parsed numbers. If
      the string contains 6 numbers then they are assumed be
      sexagesimal components.

      If ``details`` is True then a dictionary with the following keys
      is returned:

        x: float
          The first number.
        y: float
          The second number
        numvals: int
          Number of items parsed; 2 or 6.
        raw_x: dict
          The result returned by ``phmsdms`` for the first number.
        raw_y: dict
          The result returned by ``phmsdms`` for the second number.

      It is up to the user to interpret the units of the numbers
      returned.

    Raises
    ------
    ValueError:
      The exception is raised if the string cannot be interpreted as a
      sequence of 2 or 6 numbers.

    Examples
    --------
    The position of M100 reported by SIMBAD is
    "12 22 54.899 +15 49 20.57". This can be easily parsed in the
    following manner.

    >>> from angles import pposition
    >>> ra, de = pposition("12 22 54.899 +15 49 20.57")
    >>> ra
    12.38191638888889
    >>> de
    15.822380555555556

    """
    # :TODO: split two angles based on user entered separator and process each part separately.
    # Split at any character other than a digit, ".", "-", and "+".
    p = re.split(r"[^\d\-+.]*", hd)
    if len(p) not in [2, 6]:
        raise ValueError("Input must contain either 2 or 6 numbers.")

    # Two floating point numbers if string has 2 numbers.
    if len(p) == 2:
        x, y = float(p[0]), float(p[1])
        if details:
            numvals = 2
            raw_x = p[0]
            raw_y = p[1]
    # Two sexagesimal numbers if string has 6 numbers.
    elif len(p) == 6:
        x_p = phmsdms(" ".join(p[:3]))
        x = sexa2deci(x_p['sign'], *x_p['vals'])
        y_p = phmsdms(" ".join(p[3:]))
        y = sexa2deci(y_p['sign'], *y_p['vals'])
        if details:
            raw_x = x_p
            raw_y = y_p
            numvals = 6

    if details:
        result = dict(x=x, y=y, numvals=numvals, raw_x=raw_x,
                      raw_y=raw_y)
    else:
        result = x, y

    return result


def sep(a1, b1, a2, b2):
    """Angular spearation between two points on a unit sphere.

    This will be an angle between [0, π] radians.

    Parameters
    ----------
    a1, b1 : float
        Longitude-like and latitude-like angles defining the first
        point. Both are in radians.

    a2, b2 : float
        Longitude-like and latitude-like angles defining the second
        point. Both are in radians.

    Notes
    -----
    The great cicle angular separation of the second point from the
    first is returned as an angle in radians. the return value is
    always in the range [0, π].

    Results agree with those from SLALIB routine sla_dsep. See
    test_sep_against_slalib_dsep() in test_angles.py.


    Examples
    --------
    >>> r2d(sep(0, 0, 0, d2r(90.0)))
    90.0
    >>> r2d(sep(0, d2r(45.0), 0, d2r(90.0)))
    45.00000000000001
    >>> r2d(sep(0, d2r(-45.0), 0, d2r(90.0)))
    135.0

    >>> r2d(sep(0, d2r(-90.0), 0, d2r(90.0)))
    180.0
    >>> r2d(sep(d2r(45.0), d2r(-90.0), d2r(45.0), d2r(90.0)))
    180.0
    >>> r2d(sep(0, 0, d2r(90.0), 0))
    90.0

    >>> r2d(sep(0, d2r(45.0), d2r(90.0), d2r(45.0)))
    60.00000000000001
    >>> import math
    >>> 90.0 * math.cos(d2r(45.0))  # Distance along latitude circle.
    63.63961030678928
    """
    # Tolerance to decide if the calculated separation is zero.
    tol = 1e-15

    v = CartesianVector.from_spherical(1.0, a1, b1)
    v2 = CartesianVector.from_spherical(1.0, a2, b2)
    d = v.dot(v2)
    c = v.cross(v2).mod

    res = math.atan2(c, d)

    if abs(res) < tol:
        return 0.0
    else:
        return res


def bear(a1, b1, a2, b2):
    """Find bearing/position angle between two points on a unit sphere.

    Parameters
    ----------
    a1, b1 : float
        Longitude-like and latitude-like angles defining the first
        point. Both are in radians.

    a2, b2 : float
        Longitude-like and latitude-like angles defining the second
        point. Both are in radians.

    Notes
    -----
    Position angle of the second point with respect to the first
    is returned in radians. Position angle is calculated clockwise
    and counter-clockwise from the direction towards the North
    pole. It is between [0 and π] if the second point is in the
    eastern hemisphere w.r.t the first, and between (0, -π) if
    the second point is in the western hemisphere w.r.t the first.

    .. warning::

        If the first point is at the pole then bearing is undefined and
        0 is returned.

    Results agree with those from SLALIB rountine sla_dbear. See
    test_bear_against_slalib_dbear() in test_angles.py.

    Examples
    --------
    >>> from angles import bear, r2d, d2r
    >>> bear(0, 0, 0, -d2r(90.0))
    3.141592653589793
    >>> bear(0, -d2r(90.0), 0, 0)
    0.0
    >>> bear(0, -d2r(45.0), 0, 0)
    0.0
    >>> bear(0, -d2r(89.678), 0, 0)
    0.0

    >>> r2d(bear(d2r(45.0), d2r(45.0), d2r(46.0), d2r(45.0)))
    89.64644212193384

    >>> r2d(bear(d2r(45.0), d2r(45.0), d2r(44.0), d2r(45.0)))
    -89.64644212193421

    """
    # Find perpendicular to the plane containing the base and
    # z-axis. Then find the perpendicular to the plane containing
    # the base and the target. The angle between these two is the
    # position angle or bearing of the target w.r.t the base. Check
    # sign of the z component of the latter vector to determine
    # quadrant: 1st and 2nd quadrants are +ve while 3rd and 4th are
    # negative.
    #
    # Tolerance to decide if first is on the pole and also to decide if
    # the calculated bearing is zero.
    tol = 1e-15

    v1 = CartesianVector.from_spherical(1.0, a1, b1)
    v2 = CartesianVector.from_spherical(1.0, a2, b2)

    # Z-axis
    v0 = CartesianVector.from_spherical(r=1.0, alpha=0.0, delta=d2r(90.0))

    if abs(v1.cross(v0).mod) < tol:
        # The first point is on the pole. Bearing is undefined.
        warnings.warn(
            "First point is on the pole. Bearing undefined.")
        return 0.0

    # Vector perpendicular to great circle containing two points.
    v12 = v1.cross(v2)

    # Vector perpendicular to great circle containing base and
    # Z-axis.
    v10 = v1.cross(v0)

    # Find angle between these two vectors.
    dot = v12.dot(v10)
    cross = v12.cross(v10).mod
    x = math.atan2(cross, dot)

    # If z is negative then we are in the 3rd or 4th quadrant.
    if v12.z < 0:
        x = -x

    if abs(x) < tol:
        return 0.0
    else:
        return x


class HMS(object):
    """Class for representing angle as HMS, designed to be used with Angle."""
    def __init__(self, angle):
        self.angle = angle
        self.s1 = 'HH '
        self.s2 = 'MM '
        self.s3 = 'SS'

    def __gethms(self):
        a = self.angle
        lower = r2h(a._lower) if a._lower is not None else None
        upper = r2h(a._upper) if a._upper is not None else None
        return deci2sexa(
            a.h, pre=a.pre, trunc=a.trunc, lower=lower, upper=upper,
            upper_trim=a._upper_trim, b=a._b)

    def __sethms(self, val):
        if len(val) != 4:
            raise ValueError(
                "HMS must be of the form [sign, HH, MM, SS.ss..]")
        if val[0] not in (-1, 1):
            raise ValueError("Sign has to be -1 or 1.")

        self.angle.h = sexa2deci(*val)

    hms = property(__gethms, __sethms, doc="HMS tuple.")

    def __getsign(self):
        return self.hms[0]

    def __setsign(self, sign):
        if sign not in (-1, 1):
            raise ValueError("Sign has to be -1 or 1.")
        x = self.hms
        self.hms = (sign, x[1], x[2], x[3])

    sign = property(__getsign, __setsign, doc="Sign of HMS angle.")

    def __gethh(self):
        return self.hms[1]

    def __sethh(self, val):
        if not isinstance(val, int):
            raise ValueError("HH takes only integers.")
        x = self.hms
        self.hms = (x[0], val, x[2], x[3])

    hh = property(__gethh, __sethh, doc="HH of HMS angle.")

    def __getmm(self):
        return self.hms[2]

    def __setmm(self, val):
        if not isinstance(val, int):
            raise ValueError("MM takes integers only.")
        x = self.hms
        self.hms = (x[0], x[1], val, x[3])

    mm = property(__getmm, __setmm, doc="MM of HMS angle.")

    def __getss(self):
        return self.hms[3]

    def __setss(self, val):
        x = self.hms
        self.hms = (x[0], x[1], x[2], val)

    ss = property(__getss, __setss, doc="SS of HMS angle.")

    def __str__(self):
        a = self.angle
        lower = r2h(a._lower) if a._lower is not None else None
        upper = r2h(a._upper) if a._upper is not None else None
        return fmt_angle(
            a.h, s1=self.s1, s2=self.s2, s3=self.s3, pre=a.pre, trunc=a.trunc,
            lower=lower, upper=upper, upper_trim=a._upper_trim, b=a._b)


class HMSDescriptor(object):
    """Descriptor that returns HMS instance attached to given Angle instance."""
    def __get__(self, obj, objtype=None):
        return HMS(obj)

    def __set__(self, obj, value):
        HMS(obj).hms = value


class DMS(object):
    """Class for representing angle as DMS, designed to be used with Angle."""
    def __init__(self, angle):
        self.angle = angle
        self.s1 = 'DD '
        self.s2 = 'MM '
        self.s3 = 'SS'

    def __getdms(self):
        a = self.angle
        lower = r2d(a._lower) if a._lower is not None else None
        upper = r2d(a._upper) if a._upper is not None else None
        return deci2sexa(
            a.d, pre=a.pre, trunc=a.trunc, lower=lower, upper=upper,
            upper_trim=a._upper_trim, b=a._b)

    def __setdms(self, val):
        if len(val) != 4:
            raise ValueError(
                "DMS must be of the form [sign, DD, MM, SS.ss..]")
        if val[0] not in (-1, 1):
            raise ValueError("Sign has to be -1 or 1.")
        self.angle.d = sexa2deci(*val)

    dms = property(__getdms, __setdms, doc="DMS tuple.")

    def __getsign(self):
        return self.dms[0]

    def __setsign(self, sign):
        if sign not in (-1, 1):
            raise ValueError("Sign has to be -1 or 1")
        x = self.dms
        self.dms = (sign, x[1], x[2], x[3])

    sign = property(__getsign, __setsign, doc="Sign of DMS angle.")

    def __getdd(self):
        return self.dms[1]

    def __setdd(self, val):
        if not isinstance(val, int):
            raise ValueError("DD takes only integers.")
        x = self.dms
        self.dms = (x[0], val, x[2], x[3])

    dd = property(__getdd, __setdd, doc="DD of DMS angle.")

    def __getmm(self):
        return self.dms[2]

    def __setmm(self, val):
        if not isinstance(val, int):
            raise ValueError("MM takes only integers.")
        x = self.dms
        self.dms = (x[0], x[1], val, x[3])

    mm = property(__getmm, __setmm, doc="MM of DMS angle.")

    def __getss(self):
        return self.dms[3]

    def __setss(self, val):
        x = self.dms
        self.dms = (x[0], x[1], x[2], val)

    ss = property(__getss, __setss, doc="SS of DMS angle.")

    def __str__(self):
        a = self.angle
        lower = r2d(a._lower) if a._lower is not None else None
        upper = r2d(a._upper) if a._upper is not None else None
        return fmt_angle(
            a.d, s1=self.s1, s2=self.s2, s3=self.s3, pre=a.pre, trunc=a.trunc,
            lower=lower, upper=upper, upper_trim=a._upper_trim, b=a._b)


class DMSDescriptor(object):
    """Descriptor that returns DMS instance attached to given Angle instance."""
    def __get__(self, obj, objtype=None):
        return DMS(obj)

    def __set__(self, obj, value):
        DMS(obj).dms = value


class Angle(object):
    """A class for representing an angle.

    This is the basic Angle object. The angle is initialized to the
    given value. Default is 0 radians. This class will accept any
    reasonably well formatted sexagesimal string representation, in
    addition to numerical values.

    The value of the angle in different units are available as attributes. The
    angle object can be converted to a sexagesimal string, which can be
    customized using other attributes. The angle can be access in HMS and DMS
    formats using appropriate attributes.

    Converting to string using either str() or print(will return a string)
    representation of the angle.

    Parameters
    ----------
    sg : str
        A string containing a sexagesimal number.
    r : float
        Angle in radians.
    d : float
        Angle in degrees.
    h : float
        Angle in hours.
    arcs : float
        Angle in arcseconds.

    Atttributes
    -----------
    r : float
        Angle in radians
    d : float
        Angle in degrees
    h : float
        Angle in hours
    arcs : float
        Angle in arc-seconds

    hms: angles.HMS
        HMS object that represents the angle. ``hms.sign``, ``hms.hh``,
        ``hms.mm`` and ``hms.ss`` gives the sexagesimal representation of the
        angle in hours. We can assign values to these attributes. ``hms`` must
        be assigned a tuple of the format (sign, hh, mm, ss).

    dms : angles.DMS
        DMS object that represents the angle.  ``dms.sign``, ``dms.dd``,
        ``dms.mm`` and ``dms.ss`` gives the sexagesimal representation of the
        angle in hours. We can assign values to these attributes. ``dms`` must
        be assigned a tuple of the format (sign, hh, mm, ss).

    ounit : str
        Output unit. Influences string representation.
    pre : float
        The last part of the sexagesimal string is rounded to these
        many decimal points. This can be negative. This also affects ``hms.ss``
        and ``dms.ss`` attributes.
    trunc : bool
        If True, then the last part of the sexagesimal string is
        truncated to `pre` decimal places, instead of rounding. This also
        affects ``hms.ss`` and ``dms.ss`` attributes.
    s1 : str
        Separator between first and second parts of sexagesimal string.
    s2 : str
        Separator between second and third parts of sexagesimal string.
    s3 : str
        Separator after the third part of sexagesimal string.

    Notes
    -----
    Angle class can be initialized with keywords ``sg``, ``r``, ``d``, ``h`` or
    ``arcs``. The first keyword found from the above is used as the input value.

    The output string representation depends on `ounit`, `pre` and
    `trunc` attributes.

    The `ounit` attribute determines the unit. It can be "radians",
    "degrees" or "hours". For "radians", the string representation is
    just the number itself.

    The attribute `pre` determines the number of decimal places in the
    last part of the sexagesimal representation i.e., ``hms.ss``, ``dms.ss``,
    and string representation. This can be negative. If `trunc` is true then
    the number is truncated to `pre` places, else it is rounded.

    See also
    --------
    phmsdms
    sexa2deci
    deci2sexa
    normalize

    Examples
    --------
    >>> from __future__ import print_function
    >>> from angles import Angle
    >>> a = Angle(sg="12h34m16.592849219")
    >>> a.r, a.d, a.h, a.arcs  # doctest: +NORMALIZE_WHITESPACE
    (3.291152306055805, 188.56913687174583, 12.571275791449722, 678848.892738285)

    >>> a.hms.sign, a.hms.hh, a.hms.mm, a.hms.ss
    (1, 12, 34, 16.593)
    >>> a.hms.hms
    (1, 12, 34, 16.593)
    >>> a.h
    12.571275791449722

    >>> a.dms.sign, a.dms.dd, a.dms.mm, a.dms.ss
    (1, 188, 34, 8.893)
    >>> a.dms.dms
    (1, 188, 34, 8.893)
    >>> a.d
    188.56913687174583

    >>> print(a.ounit)
    hours
    >>> print(a)
    +12 34 16.593
    >>> a.pre, a.trunc
    (3, False)
    >>> a.pre = 4
    >>> print(a)
    +12 34 16.5928
    >>> a.pre = 3
    >>> a.trunc = True
    >>> print(a)
    +12 34 16.592

    >>> a.ounit = "degrees"
    >>> print(a)
    +188 34 08.892
    >>> a.ounit = "radians"
    >>> print(a)  # doctest: +SKIP
    3.29115230606

    >>> a.ounit = "degrees"
    >>> a.s1 = "DD "
    >>> a.s2 = "MM "
    >>> a.s3 = "SS"
    >>> print(a)
    +188DD 34MM 08.892SS

    The default unit is inferred from the input values.

    >>> a = Angle("35d24m34.5")
    >>> print(a)
    +35 24 34.500
    >>> a = Angle("35:24:34.5")
    >>> print(a)
    +35 24 34.500
    >>> a.ounit
    'degrees'
    >>> a = Angle("35h24m34.5")
    >>> print(a)
    +35 24 34.500
    >>> a.ounit
    'hours'

    Assigning values to attributes changes the value of the angle, but ``ounit``
    has to changed manually.

    >>> a = Angle(r=10)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (572.9577951308232, 38.197186342054884, 10, 2062648.0624709637, 'radians')

    >>> a.d = 10
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (10.0, 0.6666666666666666, 0.17453292519943295, 36000.0, 'radians')

    >>> a.dms.mm = 60
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (11.0, 0.7333333333333333, 0.19198621771937624, 39600.0, 'radians')

    >>> a.dms.dms = (1, 12, 10, 5.234)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (12.168120555555557, 0.8112080370370371, 0.21237376747404604,
    43805.234000000004, 'radians')

    >>> a.hms.hms = (1, 1, 1, 1)
    >>> a.d, a.h, a.r, a.arcs, a.ounit  # doctest: +NORMALIZE_WHITESPACE
    (15.254166666666668, 1.0169444444444444, 0.2662354329813017,
    54915.00000000001, 'radians')

    >>> print(a)  # doctest: +SKIP
    0.266235432981
    >>> a.ounit = 'hours'
    >>> print(a)
    +01 01 01.000
    >>> a.ounit = 'degrees'
    >>> print(a)
    +15 15 15.000

    Angle objects can be added to and subtracted from each other.

    >>> a = Angle(h=12.5)
    >>> b = Angle(h=13.0)
    >>> c = a - b
    >>> c.h
    -0.5000000000000011
    >>> c = a + b
    >>> c.h
    25.5

    """
    # This class handles the basic features of an Angle class. The only
    # items that need to be overridden are the `_setnorm` method and
    # the __str__ method.
    #
    # The former determines how angle values are normalized. In this
    # class it just sets the given value in radians to the `_raw`
    # attribute. Other classes can override it with a different
    # normalization scheme. For example, AlphAngle normalizes value to
    # [0, 24) hours and DeltaAngle normalizes to [-90, 90] degrees. The
    # input value to `_setnorm` is in radians.
    #
    # The string representation will need to be changed when
    # normalizing method changes. So override __str__.
    _units = ("radians", "degrees", "hours")
    _keyws = ('r', 'd', 'h', 'arcs', "sg")
    _raw = 0.0  # angle in radians
    _iunit = 0
    _ounit = "radians"
    _upper_trim = False
    _lower = None  # always in radians
    _upper = None  # always in radians
    _b = False
    pre = 3
    trunc = False
    s1 = " "
    s2 = " "
    s3 = ""

    def __init__(self, sg=None, **kwargs):
        if sg is not None:
            kwargs['sg'] = sg
        x = (True if i in self._keyws else False for i in kwargs)
        if not all(x):
            raise TypeError("Only one of {0} are allowed.".format(self._keyws))
        if "sg" in kwargs:
            x = phmsdms(kwargs['sg'])
            if x['units'] not in self._units:
                raise ValueError("Unknow units: {0}".format(x['units']))
            self._iunit = self._units.index(x['units'])
            if self._iunit == 1:
                self._setnorm(d2r(sexa2deci(x['sign'], *x['vals'])))
            elif self._iunit == 2:
                self._setnorm(h2r(sexa2deci(x['sign'], *x['vals'])))
            if len(kwargs) != 1:
                warnings.warn("Only sg = {0} used.".format(kwargs['sg']))
        elif "r" in kwargs:
            self._iunit = 0
            self._setnorm(kwargs['r'])
            if len(kwargs) != 1:
                warnings.warn("Only r = {0} used.".format(kwargs['r']))
        elif "d" in kwargs:
            self._iunit = 1
            self._setnorm(d2r(kwargs["d"]))
            if len(kwargs) != 1:
                warnings.warn("Only d = {0} used.".format(kwargs['d']))
        elif "h" in kwargs:
            self._iunit = 2
            self._setnorm(h2r(kwargs['h']))
            if len(kwargs) != 1:
                warnings.warn("Only h = {0} used.".format(kwargs['h']))
        elif "arcs" in kwargs:
            self._iunit = 1
            self._setnorm(arcs2r(kwargs['arcs']))
            if len(kwargs) != 1:
                warnings.warn("Only arcs = {0} used.".format(kwargs['arcs']))

        self._ounit = self._units[self._iunit]

    def _getnorm(self):
        return self._raw

    def _setnorm(self, val):
        # Override this method in other classes.
        self._raw = val

    def __getr(self):
        return self._getnorm()

    def __setr(self, val):
        self._iunit = 0
        self._setnorm(val)

    r = property(__getr, __setr, doc="Angle in radians.")

    def __getd(self):
        return r2d(self._getnorm())

    def __setd(self, val):
        self._iunit = 1
        self._setnorm(d2r(val))

    d = property(__getd, __setd, doc="Angle in degrees.")

    def __geth(self):
        return r2h(self._getnorm())

    def __seth(self, val):
        self._iunit = 2
        self._setnorm(h2r(val))

    h = property(__geth, __seth, doc="Angle in hours.")

    def __getarcs(self):
        return r2arcs(self._getnorm())

    def __setarcs(self, val):
        self._iunit = 1
        self._setnorm(arcs2r(val))

    arcs = property(__getarcs, __setarcs, doc="Angle in arcseconds.")

    def __getounit(self):
        return self._ounit

    def __setounit(self, val):
        if val not in self._units:
            raise ValueError("Unit can only be {0}".format(self._units))
        self._ounit = val

    ounit = property(__getounit, __setounit, doc="String output unit.")

    hms = HMSDescriptor()

    dms = DMSDescriptor()

    def __repr__(self):
        return str(self.r)

    def __str__(self):
        if self.ounit == "radians":
            return str(self.r)
        elif self.ounit == "degrees":
            return fmt_angle(self.d, s1=self.s1, s2=self.s2,
                             s3=self.s3,
                             pre=self.pre, trunc=self.trunc)
        elif self.ounit == "hours":
            return fmt_angle(self.h, s1=self.s1, s2=self.s2,
                             s3=self.s3,
                             pre=self.pre, trunc=self.trunc)

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise ValueError("Addition needs to Angle objects.")
        return Angle(r=self.r + other.r)

    def __sub__(self, other):
        if not isinstance(other, Angle):
            raise ValueError("Subtraction needs two Angle objects.")
        return Angle(r=self.r - other.r)


class AlphaAngle(Angle):
    """Angle for longitudinal angles such as Right Ascension.

    AlphaAngle is a subclass of Angle that can be used to represent
    longitudinal angles such as Right Ascension, azimuth and longitude.

    In AlphaAngle the attribute `ounit` is always "hours" and
    formatting is always as an HMS sexagesimal string.

    The angle is normalized to [0, 24) hours.

    This takes the same parameters as the `Angle` class, and has the
    same attributes as the `Angle` class. The attribute `ounit` is
    read-only.

    Notes
    -----
    The `pre` and `trunc` properties will affect both the string
    representation as well as the sexagesimal parts. The angle is
    normalized into [0, 24) hours in such a way that 25 hours become 1
    hours and -1 hours become 23 hours.

    See also
    --------
    Angle (for common attributes)

    Examples
    --------
    >>> from __future__ import print_function
    >>> from angles import AlphaAngle
    >>> a = AlphaAngle(d=180.5)
    >>> print(a)
    +12HH 02MM 00.000SS
    >>> a = AlphaAngle(h=12.0)
    >>> print(a)
    +12HH 00MM 00.000SS
    >>> a = AlphaAngle(h=-12.0)

    The attribute `ounit` is read-only.

    >>> a.ounit
    'hours'
    >>> print(a)
    +12HH 00MM 00.000SS

    >>> a = AlphaAngle("12h14m23.4s")
    >>> print(a)
    +12HH 14MM 23.400SS
    >>> a.r, a.d, a.h, a.arcs
    (3.204380873430289, 183.5975, 12.239833333333333, 660951.0)

    The `hms` attribute contains instance of  HMS class that gives the
    sexagesimal represenation of the angle in hours. The individual parts are
    accessible as `hms.sign`, `hms.hh`, `hms.mm` and `hms.ss`. A tuple of all 4
    attributes are available as `hms.hms`. The `pre` and `trunc` attributes are
    taken into account while generating the `hms` attribute.

    The `dms` attribute is similar to HMS except it is an instance of the DMS
    class and has attribute ``dd`` instead of ``hh``. It is the sexagesimal
    represenation of the angle in degrees.

    >>> a = AlphaAngle(h=12.54678345)
    >>> a.hms.hms
    (1, 12, 32, 48.42)
    >>> a.hms.sign, a.hms.hh, a.hms.mm, a.hms.ss
    (1, 12, 32, 48.42)
    >>> print(a)
    +12HH 32MM 48.420SS
    >>> a.pre = 5
    >>> a.hms.hms
    (1, 12, 32, 48.42042)
    >>> print(a)
    +12HH 32MM 48.42042SS

    Separators can be changed.

    >>> a.s1 = " : "
    >>> a.s2 = " : "
    >>> a.s3 = ""
    >>> print(a)
    +12 : 32 : 48.42042

    >>> a.pre = 3
    >>> a.dms.dms
    (1, 188, 12, 6.306)

    Angles are properly normalized.

    >>> a = AlphaAngle(h=25.0)
    >>> print(a)
    +01HH 00MM 00.000SS
    >>> a = AlphaAngle(h=-1.0)
    >>> print(a)
    +23HH 00MM 00.000SS

    The sexagesimal parts are properly converted into their respective
    ranges.

    >>> a.hms.hh = 23
    >>> a.hms.mm = 59
    >>> a.hms.ss = 59.99999
    >>> a.hms.hms
    (1, 0, 0, 0.0)
    >>> print(a)
    +00HH 00MM 00.000SS
    >>> a.pre = 5
    >>> a.hms.hms
    (1, 23, 59, 59.99999)
    >>> print(a)
    +23HH 59MM 59.99999SS

    Angles can be added to and subtracted from each other.

    >>> a = AlphaAngle(h=12.0)
    >>> b = AlphaAngle(h=13.0)
    >>> c = a - b
    >>> c.h
    23.0
    >>> c = a + b
    >>> round(c.h, 12)
    1.0

    """
    _upper_trim = True
    _lower = 0
    _upper = h2r(24)

    def __init__(self, sg=None, **kwargs):
        super(AlphaAngle, self).__init__(sg=sg, **kwargs)
        self.__ounit = "hours"
        self.s1 = "HH "
        self.s2 = "MM "
        self.s3 = "SS"

    def _setnorm(self, val):
        # override method from Angle.
        self._raw = r2r(val)  # [0, 2π) i.e., h = [0, 24).

    def __getounit(self):
        return self.__ounit

    ounit = property(fget=__getounit,
                     doc="Formatting unit: always hours for RA.")

    def __str__(self):
        # Always HMS. Need lower, upper so that upper_trim works.
        return fmt_angle(self.h, s1=self.s1, s2=self.s2, s3=self.s3,
                         pre=self.pre, trunc=self.trunc,
                         lower=r2h(self._lower), upper=r2h(self._upper),
                         upper_trim=self._upper_trim)

    def __add__(self, other):
        """Adds any type of angle to this."""
        if not isinstance(other, Angle):
            raise ValueError("Addition needs two Angle objects.")
        return AlphaAngle(r=self.r + other.r)

    def __sub__(self, other):
        """Subtracts any type of angle from this."""
        if not isinstance(other, Angle):
            raise ValueError("Subtraction needs two Angle objects.")
        return AlphaAngle(r=self.r - other.r)


class DeltaAngle(Angle):
    """Angle for latitudinal angles such as Declination.

    DeltaAngle is a subclass of Angle for latitudinal angles such as
    Declination, elevation and latitude.

    In DeltaAngle the attribute `ounit` is always "degrees" and
    formatting is always as a DMS sexagesimal string.

    The angle is normalized to the range [-90, 90] degrees.

    This takes the same parameters as the `Angle` class, and has the
    same attributes as the `Angle` class. The attribute `ounit` is
    read-only. Additonal attributes are given below.

    Notes
    -----
    The `pre` and `trunc` properties will affect both the string
    representation as well as the sexagesimal parts. The angle is
    normalized between [-90, 90], in such a way that -91 becomes -89
    and 91 becomes 89.

    See also
    --------
    Angle (for common attributes)

    Examples
    --------
    >>> from __future__ import print_function
    >>> from angles import DeltaAngle
    >>> a = DeltaAngle(d=-45.0)
    >>> print(a)
    -45DD 00MM 00.000SS
    >>> a = DeltaAngle(d=180.0)
    >>> print(a)
    +00DD 00MM 00.000SS
    >>> a = DeltaAngle(h=12.0)
    >>> print(a)
    +00DD 00MM 00.000SS
    >>> a = DeltaAngle(sg="91d")
    >>> print(a)
    +89DD 00MM 00.000SS

    Attribute `ounit` is always "degrees".

    >>> a.ounit
    'degrees'

    If no keyword is provided then the input is taken to a sexagesimal
    string and the units will be determined from it.  The numerical
    value of the angle in radians, hours, degrees and arc-seconds can
    be extracted from appropriate attributes.

    >>> a = DeltaAngle("12d23m14.2s")
    >>> print(a)
    +12DD 23MM 14.200SS
    >>> a.r, a.d, a.h, a.arcs
    (0.2161987825813487, 12.387277777777777, 0.8258185185185185, 44594.2)

    The `dms` attribute contains instance of  DMS class that gives the
    sexagesimal represenation of the angle in degrees. The individual parts are
    accessible as `dms.sign`, `dms.dd`, `dms.mm` and `dms.ss`. A tuple of all 4
    attributes are available as `dms.dms`. The `pre` and `trunc` attributes are
    taken into account while generating the `dms` attribute.

    The `hms` attribute is similar to DMS except it is an instance of the HMS
    class and has attribute ``hh`` instead of ``dd``. It is the sexagesimal
    represenation of the angle in hours.

    >>> a = DeltaAngle(d=12.1987546)
    >>> a.dms.dms
    (1, 12, 11, 55.517)
    >>> a.pre = 5
    >>> a.dms.dms
    (1, 12, 11, 55.51656)
    >>> a.dms.dd, a.dms.mm, a.dms.ss
    (12, 11, 55.51656)
    >>> a.pre = 0
    >>> a.dms.dms
    (1, 12, 11, 56.0)

    The separators can be changed.

    >>> a = DeltaAngle(d=12.3459876)
    >>> a.s1 = " : "
    >>> a.s2 = " : "
    >>> a.s3 = ""
    >>> print(a)
    +12 : 20 : 45.555

    Angles are properly normalized.

    >>> a = DeltaAngle(d=-91.0)
    >>> print(a)
    -89DD 00MM 00.000SS
    >>> a = DeltaAngle(d=91.0)
    >>> print(a)
    +89DD 00MM 00.000SS

    The sexagesimal parts are properly normalized into their respective
    ranges.

    >>> a.dms.sign = 1
    >>> a.dms.dd = 89
    >>> a.dms.mm = 59
    >>> a.dms.ss = 59.9999
    >>> a.pre = 3
    >>> print(a)
    +90DD 00MM 00.000SS
    >>> a.pre = 5
    >>> print(a)
    +89DD 59MM 59.99990SS

    >>> a.dms.dms = (1, 0, 0, 0.0)
    >>> a.dms.dd = 89
    >>> a.dms.mm = 60
    >>> a.dms.ss = 60
    >>> a.pre = 3
    >>> print(a)
    +89DD 59MM 00.000SS

    Angles can be added to and subtracted from each other.

    >>> a = DeltaAngle(d=12.0)
    >>> b = DeltaAngle(d=13.0)
    >>> c = a - b
    >>> c.d
    -0.9999999999999998
    >>> c = a + b
    >>> c.d
    25.000000000000004
    >>> print(c)
    +25DD 00MM 00.000SS
    >>> c = a - b
    >>> print(c)
    -01DD 00MM 00.000SS

    """
    _upper_trim = False
    _lower = -math.pi / 2
    _upper = math.pi / 2
    _b = True

    def __init__(self, sg=None, **kwargs):
        super(DeltaAngle, self).__init__(sg=sg, **kwargs)
        self.__ounit = "degrees"
        self.s1 = "DD "
        self.s2 = "MM "
        self.s3 = "SS"

    def _setnorm(self, val):
        # overriding the method in Angle.
        self._raw = normalize(val, lower=self._lower, upper=self._upper, b=self._b)

    def __getounit(self):
        return self.__ounit

    ounit = property(fget=__getounit,
                     doc="Formatting unit: always degrees for Dec.")

    def __unicode__(self):
        # Always DMS.
        return fmt_angle(self.d, s1=self.s1, s2=self.s2, s3=self.s3,
                         pre=self.pre, trunc=self.trunc,
                         lower=r2d(self._lower), upper=r2d(self._upper), b=self._b)

    def __str__(self):
        # Always DMS.
        return fmt_angle(self.d, s1=self.s1, s2=self.s2, s3=self.s3,
                         pre=self.pre, trunc=self.trunc,
                         lower=r2d(self._lower), upper=r2d(self._upper), b=self._b)

    def __add__(self, other):
        """Adds any type of angle to this."""
        if not isinstance(other, Angle):
            raise ValueError("Addition needs two Angle objects.")
        return DeltaAngle(r=self.r + other.r)

    def __sub__(self, other):
        """Subtracts any type of angle from this."""
        if not isinstance(other, Angle):
            raise ValueError("Subtraction needs two Angle objects.")
        return DeltaAngle(r=self.r - other.r)


class CartesianVector(object):
    """A 3D Cartesian vector.

    An instance of this is added to an AngularPosition object, so that
    vector methods can be used for calculating bearings and
    separations.

    The latitude like angle is measured from the "equator" and not from
    the z-axis.

    Methods
    -------
    dot
    cross
    mod
    from_s

    """
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_spherical(cls, r=1.0, alpha=0.0, delta=0.0):
        """Construct Cartesian vector from spherical coordinates.

        alpha and delta must be in radians.
        """
        x = r * math.cos(delta) * math.cos(alpha)
        y = r * math.cos(delta) * math.sin(alpha)
        z = r * math.sin(delta)
        return cls(x=x, y=y, z=z)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        """Cross product of two vectors.

        Parameters
        ----------
        v : CartesianVector
            The vector to take cross product with.

        Returns
        -------
        v : CartesianVector
            Cross product of this vector and the given vector.

        """
        n = self.__class__()
        n.x = self.y * v.z - self.z * v.y
        n.y = - (self.x * v.z - self.z * v.x)
        n.z = self.x * v.y - self.y * v.x

        return n

    @property
    def mod(self):
        """Modulus of vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def spherical_coords(self):
        tol = 1e-15
        r = self.mod
        alpha = math.atan2(self.y, self.x)
        delta = math.pi/2.0 if r < tol else math.asin(self.z/r)
        return (r, alpha, delta)

    @property
    def normalized_angles(self):
        _, alpha, delta = self.spherical_coords
        alpha = normalize(r2d(alpha), lower=0, upper=360)
        delta = normalize(r2d(delta), lower=-90, upper=90, b=True)
        return (d2r(alpha), d2r(delta))

    def __repr__(self):
        return "CartesianVector(x={}, y={}, z={})".format(self.x, self.y, self.z)

    def __str__(self):
        return self.__repr__()


def normalize_sphere(alpha, delta):
    """Normalize angles of a point on a sphere.

    Parameters
    ----------
    alpha: float
        The alpha (right ascension/longitude like) angle in degrees.
    delta: float
        The delta (declination/latitude like) angle in degrees.

    Returns
    -------
    (alpha, delta): (float, float)
        Normalized alpha (degrees) and delta (degrees).

    Notes
    -----

    This function converts given position on a sphere into the simplest
    normalized values, considering that the points are on a sphere.

    Input position        Output position

    (180, 91)              (0, 89)
    (180, -91)             (0, -89)
    (0, 91)                (180, 89)
    (0, -91)               (180, -89)
    (120, 280)             (120, -80)

    (h2d(25), 45)          (225, 45)
    (h2d(-25), -45)        (345, -45)
    """
    v = CartesianVector.from_spherical(r=1.0, alpha=d2r(alpha), delta=d2r(delta))
    angles = v.normalized_angles
    return r2d(angles[0]), r2d(angles[1])


class AlphaAngleSphere(AlphaAngle):
    def __init__(self, ap):
        self._ap = ap
        super(AlphaAngleSphere, self).__init__(h=r2h(ap._cv.normalized_angles[0]))

    def _getnorm(self):
        # When DeltaAngleSphere is changed it makes the change in _cv. We need
        # to get that change
        return self._ap._cv.normalized_angles[0]

    def _setnorm(self, val):
        _, delta = self._ap._cv.normalized_angles
        self._ap._cv = CartesianVector.from_spherical(r=self._ap._cv.mod, alpha=val, delta=delta)
        # don't really need this step since _getnorm above
        self._raw = self._ap._cv.normalized_angles[0]


class DeltaAngleSphere(DeltaAngle):
    def __init__(self, ap):
        self._ap = ap
        super(DeltaAngleSphere, self).__init__(d=r2d(ap._cv.normalized_angles[1]))

    def _getnorm(self):
        return self._ap._cv.normalized_angles[1]

    def _setnorm(self, val):
        alpha, _ = self._ap._cv.normalized_angles
        self._ap._cv = CartesianVector.from_spherical(r=self._ap._cv.mod, alpha=alpha, delta=val)
        # don't really need this step since _getnorm above
        self._raw = self._ap._cv.normalized_angles[1]


class AngularPosition(object):
    """Class for representing a point on a unit sphere, say (RA, DEC).

    AngularPosition can be used to work with points on a sphere. This
    object stores two attributes `alpha` and `delta` that represent the
    longitudinal and latitudinal angles, repectively. The former is of
    type `AlphaAngleSphere` and the latter is of type `DeltaAngleSphere`.

    The string representation of AngularPosition is constructed using
    both alpha and delta.

    Difference between two AngularPosition gives the separation between
    them in radians.

    The separation between two angular positions can also be obtained
    by calling the method `sep`.

    The bearing between two points can be obtained using the `bear`
    method.

    Parameters
    ----------
    alpha: longitude/ra like angle in degrees
    delta: latitude/dec like angle in degrees

    Attributes
    ----------
    alpha : AlphaAngleSphere
        The longitude like angle.
    delta : DeltaAngleSphere
        The latitude like angle.
    dlim : str
        Delimiter to use between `alpha` and `delta` angles in string
        representation.

    Methods
    -------
    sep : return great circle separation in radians.
    bear : return bearing/position angle in radians.

    See also
    --------
    Angle
    AlphaAngle
    DeltaAngle

    Examples
    --------
    >>> from __future__ import print_function
    >>> from angles import AngularPosition, r2d

    >>> a = AngularPosition.from_hd("12 22 54.899 +15 49 20.57")
    >>> print(a)
    +12HH 22MM 54.899SS +15DD 49MM 20.570SS
    >>> a = AngularPosition.from_hd("12dd 22 54.899 +15 49 20.57")
    >>> print(a)
    +00HH 49MM 31.660SS +15DD 49MM 20.570SS
    >>> a = AngularPosition.from_hd("12d 22 54.899 +15 49 20.57")
    >>> print(a)
    +00HH 49MM 31.660SS +15DD 49MM 20.570SS

    The input values are normalized to their simplest representation on a
    sphere.

    >>> a = AngularPosition(alpha=165, delta=-91)  # alpha should flip by 180 degrees
    >>> round(a.alpha.d , 12), round(a.delta.d, 12)
    (345.0, -89.0)
    >>> a.delta.d = -91 # alpha should now do another 180 flip and come back to 165
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (165.0, -89.0)
    >>> a.delta.d = 89  # there should be no change in normalized angles
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (165.0, 89.0)
    >>> a.alpha.d = -180  # alpha should normalize to 180 delta shouldn't change
    >>> round(a.alpha.d, 12), round(a.delta.d, 12)
    (180.0, 89.0)

    >>> pos1 = AngularPosition(alpha=12.0, delta=90.0)
    >>> pos2 = AngularPosition(alpha=12.0, delta=0.0)
    >>> r2d(pos2.bear(pos1))
    0.0
    >>> r2d(pos1.bear(pos2))
    0.0
    >>> r2d(pos1.sep(pos2))
    90.0
    >>> pos1.alpha.h = 0.0
    >>> pos2.alpha.h = 0.0
    >>> r2d(pos1.sep(pos2))
    90.0
    >>> r2d(pos2.bear(pos1))
    0.0
    >>> r2d(pos1.bear(pos2))
    0.0

    >>> pos2.delta.d = -90
    >>> r2d(pos1.bear(pos2))
    0.0
    >>> r2d(pos1.sep(pos2))
    180.0

    >>> print(pos1)
    +00HH 00MM 00.000SS +90DD 00MM 00.000SS
    >>> print(pos2)
    +00HH 00MM 00.000SS -90DD 00MM 00.000SS
    >>> pos1.dlim = " | "
    >>> print(pos1)
    +00HH 00MM 00.000SS | +90DD 00MM 00.000SS

    """
    dlim = " "

    def __init__(self, alpha=0.0, delta=0.0):
        self._cv = CartesianVector.from_spherical(r=1.0, alpha=d2r(alpha), delta=d2r(delta))
        self._alpha = AlphaAngleSphere(self)
        self._delta = DeltaAngleSphere(self)

    @classmethod
    def from_hd(cls, hd):
        if not isinstance(hd, str):
            raise ValueError("hd must be a string.")

        # There are several possible combination of units in the
        # string. For simplicity, use set of rules to get alpha
        # value in hours and delta value in degrees.
        r = pposition(hd, details=True)
        if r['numvals'] == 6:
            raw_x = r['raw_x']
            if raw_x['units'] == "degrees" and ("d" in hd or "dd" in hd):
                # phmsdms called by pposition returns degrees if "hh"
                # or "h" is not in hd. We want the reverse here.
                # Assume degrees only if "d" or "dd" is present in hd.
                x = r['x']
            else:
                # Assume that this is hours.
                x = h2d(r['x'])

            raw_y = r['raw_y']
            if raw_y['units'] == "hours":
                y = h2d(r['y'])
            else:
                y = r['y']  # Assume degrees.

        else:
            x = h2d(r['x'])
            y = r['y']

        return cls(alpha=x, delta=y)

    @property
    def alpha(self):
        return self._alpha

    @property
    def delta(self):
        return self._delta

    def sep(self, p):
        """Angular spearation between objects in radians.

        Parameters
        ----------
        p : AngularPosition
            The object to which the separation from the current object
            is to be calculated.

        Notes
        -----
        This method calls the function sep(). See its docstring for
        details.

        See also
        --------
        sep

        """
        return sep(self.alpha.r, self.delta.r, p.alpha.r, p.delta.r)

    def bear(self, p):
        """Find position angle between objects, in radians.

        Parameters
        ----------
        p : AngularPosition
            The object to which bearing must be determined.

        Notes
        -----
        This method calls the function bear(). See its docstring for
        details.

        See also
        --------
        bear

        """
        return bear(self.alpha.r, self.delta.r, p.alpha.r, p.delta.r)

    def __str__(self):
        return "{0}{1}{2}".format(str(self.alpha), self.dlim, str(self.delta))
