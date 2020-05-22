import spiceypy

def definition(sensor):

    #
    # We check if the resolution of the camera has been provided as an input
    # if not we try to obtain the resolution of the camera from the IK
    #
    sensor_id = spiceypy.bodn2c(sensor)

    pixel_samples = spiceypy.gdpool(f'INS{sensor_id}_PIXEL_SAMPLES', 0, 1)[0]
    pixel_lines =   spiceypy.gdpool(f'INS{sensor_id}_PIXEL_LINES',   0, 1)[0]
    ccd_center =    spiceypy.gdpool(f'INS{sensor_id}_CCD_CENTER', 0, 2)

    print(f'{sensor} pixel_samples (x)   = {pixel_samples}')
    print(f'{sensor} pixel_lines   (y)   = {pixel_lines}')
    print(f'{sensor} ccd_sensor    (x,y) = {ccd_center[0]},{ccd_center[1]}')

    return

def pixel_lines(sensor):
    sensor_id = spiceypy.bodn2c(sensor)
    return spiceypy.gdpool(f'INS{sensor_id}_PIXEL_LINES', 0, 1)[0]

def pixel_samples(sensor):
    sensor_id = spiceypy.bodn2c(sensor)
    return spiceypy.gdpool(f'INS{sensor_id}_PIXEL_SAMPLES', 0, 1)[0]

def ccd_center(sensor):
    sensor_id = spiceypy.bodn2c(sensor)
    return spiceypy.gdpool(f'INS{sensor_id}_CCD_CENTER', 0, 2)