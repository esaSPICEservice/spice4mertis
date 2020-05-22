#!/usr/bin/env python3
import spiceypy
import numpy as np


def pixel_boresight(sensor, i, j):

    #
    # We check if the resolution of the camera has been provided as an input
    # if not we try to obtain the resolution of the camera from the IK
    #

    sensor_id = spiceypy.bodn2c(sensor)
    (shape, sensor_frame, bsight, vectors, bounds) = spiceypy.getfov(sensor_id, 100)

    pixel_samples = spiceypy.gdpool(f'INS{sensor_id}_PIXEL_SAMPLES', 0, 1)
    pixel_lines =   spiceypy.gdpool(f'INS{sensor_id}_PIXEL_LINES',   0, 1)

    #
    # We generate a matrix using the resolution of the framing camera as the
    # dimensions of the matrix
    #
    nx, ny = (int(pixel_lines[0]), int(pixel_samples[0]))
    x = np.linspace(bounds[0][0], bounds[2][0], nx)
    y = np.linspace(bounds[0][1], bounds[2][1], ny)

    return [x[int(i)], y[int(j)], bsight[2]]


def geometry(et, bsight, target, frame, sensor, observer=''):

    if not observer:
        observer = sensor

    # Time tag [UTC]
    # pixel id [(x,y)]
    # corner id [(x,y)]

    # Requested geometry

    # lat lon intersection (planetocentric)
    # lat lon subspacecraft
    # lat lon subsolar
    # target distance intersection
    # target angular diameter
    # local solar time intersection
    # phase angle intersection
    # emission angle intersection
    # incidence angle intersection

    #
    # We retrieve the camera information using GETFOV. More info available:
    #
    #   https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html
    #
    sensor_id = spiceypy.bodn2c(sensor)
    (shape, sensor_frame, ibsight, vectors, bounds) = spiceypy.getfov(sensor_id, 100)


    visible = spiceypy.fovtrg(sensor, target, 'ELLIPSOID', frame, 'LT+S', observer, et)

    if not visible:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    tarid = spiceypy.bodn2c(target)

    n, radii = spiceypy.bodvrd(target, 'RADII', 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re

    try:
        #
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html
        #
        # For each pixel we compute the possible intersection with the target, if
        # the target is intersected we then compute the illumination angles. We
        # use the following SPICE APIs: SINCPT and ILLUMF
        #
        #   https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html
        #   https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumf_c.html
        #
        (spoint, trgepc, srfvec) = \
            spiceypy.sincpt('ELLIPSOID', target, et, frame, 'LT+S', observer, sensor_frame, bsight)

        (tarlon, tarlat, taralt) = spiceypy.recgeo(spoint, re, f)
        tardis = spiceypy.vnorm(srfvec)

        #
        # Angular diameter
        #
        tarang = np.degrees(2 * np.arctan( max(radii) / spiceypy.vnorm(spoint + srfvec) ))



        #
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumf_c.html
        #
        (trgenpc, srfvec, phase, incdnc, emissn, visiblef, iluminatedf) = \
             spiceypy.illumf('ELLIPSOID', target, 'SUN', et, frame, 'LT+S', observer, spoint)

        phase *= spiceypy.dpr()
        incdnc *= spiceypy.dpr()
        emissn *= spiceypy.dpr()

        #
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html
        #
        #    VARIABLE  I/O  DESCRIPTION
        #    --------  ---  --------------------------------------------------
        #    et         I   Epoch in seconds past J2000 epoch.
        #    body       I   ID-code of the body of interest.
        #    lon        I   Longitude of surface point (RADIANS).
        #    type       I   Type of longitude "PLANETOCENTRIC", etc.
        #    timlen     I   Available room in output time string.
        #    ampmlen    I   Available room in output `ampm' string.
        #    hr         O   Local hour on a "24 hour" clock.
        #    mn         O   Minutes past the hour.
        #    sc         O   Seconds past the minute.
        #    time       O   String giving local time on 24 hour clock.
        #    ampm       O   String giving time on A.M./ P.M. scale.
        (hr, mn, sc, ltime, ampm) = \
            spiceypy.et2lst(et, tarid, tarlon, 'PLANETOCENTRIC', 80, 80)

        #
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html
        #
        #    Variable  I/O  Description
        #    --------  ---  --------------------------------------------------
        #    method     I   Computation method.
        #    target     I   Name of target body.
        #    et         I   Epoch in TDB seconds past J2000 TDB.
        #    fixref     I   Body-fixed, body-centered target body frame.
        #    abcorr     I   Aberration correction flag.
        #    obsrvr     I   Name of observing body.
        #    spoint     O   Sub-observer point on the target body.
        #    trgepc     O   Sub-observer point epoch.
        #    srfvec     O   Vector from observer to sub-observer point
        #
        (spoint, trgepc, srfev) = \
            spiceypy.subpnt('INTERCEPT/ELLIPSOID', target, et, frame, 'LT+S', observer)

        (sublon, sublat, subalt) = spiceypy.recgeo(spoint, re, f)


        #
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html
        #
        #    Variable  I/O  Description
        #    --------  ---  --------------------------------------------------
        #    method     I   Computation method.
        #    target     I   Name of target body.
        #    et         I   Epoch in ephemeris seconds past J2000 TDB.
        #    fixref     I   Body-fixed, body-centered target body frame.
        #    abcorr     I   Aberration correction.
        #    obsrvr     I   Name of observing body.
        #    spoint     O   Sub-solar point on the target body.
        #    trgepc     O   Sub-solar point epoch.
        #    srfvec     O   Vector from observer to sub-solar point.
        #
        (spoint, trgepc, srfev) = \
            spiceypy.subslr('INTERCEPT/ELLIPSOID', target, et, frame, 'LT+S', observer)

        (sunlon, sunlat, sunalt) = spiceypy.recgeo(spoint, re, f)

        return tarlon, tarlat, sublon, sublat, sunlon, sunlat, tardis, tarang, ltime, phase, emissn, incdnc

    except:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


def pixel_geometry(et, sensor, pix_line,pix_sample, target, frame, observer=''):

    bsight = pixel_boresight(sensor, pix_line, pix_sample)
    return geometry(et, bsight, target, frame, sensor, observer=observer)