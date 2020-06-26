import spiceypy
from spice4mertis.core.geometry import pixel_geometry
import numpy as np
import pandas as pd
import datetime
from spice4mertis.utils.sensor import ccd_center, pixel_lines, pixel_samples

def run(mk, time_start='', time_finish='', step=60, target='MERCURY',
        frame='', sensor='MPO_MERTIS_TIR_PLANET', pixel_line='',
        pixel_sample='', observer='MPO',
        return_output=None):

    spiceypy.furnsh(mk)

    target = target.upper()

    if not return_output : return_output = False
    if not time_start: time_start = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    if not frame: frame = f'IAU_{target}'
    if not time_finish: time_finish = time_start
    if not pixel_sample: pixel_sample = np.floor(ccd_center(sensor)[0])
    if not pixel_line: pixel_line = np.floor(ccd_center(sensor)[1])

    if pixel_sample == 'all':
        pixel_sample = np.arange(1, pixel_samples(sensor), 1)
    else:
        pixel_sample = [pixel_sample]
    if pixel_line == 'all':
        pixel_line = np.arange(1, pixel_lines(sensor), 1)
    else:
        pixel_line = [pixel_line]


    et_start = spiceypy.utc2et(time_start)
    et_finish = spiceypy.utc2et(time_finish)

    if et_start != et_finish:
        interval = np.arange(et_start, et_finish, step)
    else:
        interval = [et_start]

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

    if return_output:
        output = []
        output.append(['utc','et','pixlin','pixsam','tarlon','tarlat','sublon','sublat','sunlon','sunlat','tardis','tarang','ltime','phase','emissn','incdnc'])
        for et in interval:
            utc = spiceypy.et2utc(et, 'ISOC', 3)
            for line in pixel_line:
                for sample in pixel_sample:
                    pixelGeometry = pixel_geometry(et, sensor, line, sample, target, frame, observer=observer)
                    output.append([utc,et,line,sample,pixelGeometry])
        return output
    else : 

        with open('spice4mertis.csv', 'w') as o:
            o.write('utc,et,pixlin,pixsam,tarlon,tarlat,sublon,sublat,sunlon,sunlat,tardis,tarang,ltime,phase,emissn,incdnc\n')
            for et in interval:
                utc = spiceypy.et2utc(et, 'ISOC', 3)
                for line in pixel_line:
                    for sample in pixel_sample:
                        pixelGeometry = pixel_geometry(et, sensor, line, sample, target, frame, observer=observer)
                        print(utc,line,sample,str(pixelGeometry)[1:-1].replace(',',' '))
                        o.write(f'{utc},{et},{line},{sample},{str(pixelGeometry)[1:-1].replace(" ","")}\n')
        return

