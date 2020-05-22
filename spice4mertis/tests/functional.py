from spice4mertis.core.director import run
from spice4mertis.core.output import output
import spice4mertis.utils.sensor as sensor
import spiceypy

def test_sensor_definition(mk):
    spiceypy.furnsh(mk)
    sensor.definition('MPO_MERTIS_TIS_SPACE')

def runSPICE4MERTIS(mk):

    print('CCD Center:')
    run(mk, time_start='2026-09-29T08:09:47')
    print('All Pixels in Line 1:')
    run(mk, pixel_line=1, pixel_sample='all',time_start='2026-09-29T08:09:47')
    print('All Pixels in Sample 1:')
    run(mk, pixel_line='all', pixel_sample=1, time_start='2026-09-29T08:09:47')
    print('All Pixels')
    run(mk, pixel_line='all', pixel_sample='all', time_start='2026-09-29T08:09:47')

    print('All At the Moon')
    run(mk, pixel_line='all', pixel_sample=1, time_start='2020-04-09T03:00:00',
        target='MOON', sensor='MPO_MERTIS_TIS_SPACE',time_finish='2020-04-09T23:00:00', step=60*10)


def test_ouput(mk):
    run(mk, pixel_line='all', pixel_sample='all', time_start='2020-04-09T07:10:00.000',
        target='MOON', sensor='MPO_MERTIS_TIS_SPACE')
    output("spice4mertis.csv")

if __name__ == '__main__':

    mk = '/Users/mcosta/SPICE/BEPICOLOMBO/kernels/mk/bc_plan_local.tm'
    runSPICE4MERTIS(mk)
    test_sensor_definition(mk)
    test_ouput(mk)

