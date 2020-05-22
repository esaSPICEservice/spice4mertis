#!/usr/bin/env python3

import os
import textwrap


from argparse import ArgumentParser, RawDescriptionHelpFormatter

from spice4mertis.core.director import run



def main():

    with open(os.path.dirname(__file__) + '/config/version',
              'r') as f:
        for line in f:
            version = line

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                                description=textwrap.dedent('''\

 SPICE4MERTIS -- Version {}, SPICE Based tool for BepiColombo MERTIS. 

   SPICE4MERTIS is a command-line or Python package tool aimed to 
   support MERTIS science operations and data analysis.

'''.format(version)),
                                epilog='''                                      
   Source and documentation is available here:
      https://github.com/esaSPICEservice/spice4mertis

   developed and maintained by the
    __   __   __      __   __     __   ___     __   ___  __          __   ___
   /__\ /__` '__\    /__` |__) | /  ` |__     /__` |__  |__) \  / | /  ` |__
   \__, .__/ \__/    .__/ |    | \__, |___    .__/ |___ |  \  \/  | \__, |___

   esa_spice@sciops.esa.int     for  BepiColombo MERTIS team
   http://spice.esac.esa.int         

''')
    parser.add_argument('metakernel', metavar='METAKERNEL', type=str, nargs='+',
                    help='Meta-kernel to be read.')
    parser.add_argument('-v', '--version',
                    help='Display the version of SPICE4MERTIS',
                    action='store_true')
    parser.add_argument('-st', '--starttime',
                    help='Input UTC start time in YYYY-MM-DDTHH:MM:SS. Default is now.',
                    default='')
    parser.add_argument('-fs', '--finishtime',
                    help='Input UTC finish time in YYYY-MM-DDTHH:MM:SS. Default is start time.',
                    default='')
    parser.add_argument('-sp', '--step',
                    help='Step for the time interval in seconds. Default is 60 seconds.',
                    default=60)
    parser.add_argument('-ta', '--target',
                    help='Target of the observation. Default is MERCURY.',
                    default='MERCURY')
    parser.add_argument('-fr', '--frame',
                    help='Specify object reference. Default is IAU_<TARGET>',
                    default='')
    parser.add_argument('-sr', '--sensor',
                    help='Specify sensor. Default is MPO_MERTIS_TIS_SPACE.',
                    default='MPO_MERTIS_TIR_PLANET')
    parser.add_argument('-pl', '--pixelline',
                    help='Specify sensor pixel sample (x coordinate). Default is center of CCD.',
                    default='')
    parser.add_argument('-ps', '--pixelsample',
                    help='Specify sensor pixel sample (x coordinate). Default is center of CCD.',
                    default='')
    args = parser.parse_args()

    if args.version:
        print(version)
        return

    mk = args.metakernel
    time_start = args.starttime
    time_finish = args.finishtime
    step = args.step
    frame = args.frame
    sensor = args.sensor
    pixel_sample = args.pixelsample
    pixel_line = args.pixelline
    target = args.target.upper()


    run(mk, time_start, time_finish, step, target, frame, sensor, pixel_line, pixel_sample)

    return