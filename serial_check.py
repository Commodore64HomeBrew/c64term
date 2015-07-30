from serial.tools import list_ports
import serial

def locate_port():
    """Attempt to locate the serial port to which the device
    is connected."""

    status_request_string = 'OI;'  # Output information
    expected_response = 'DISPENSEMATE'

    device_port = None
    for port_name, port_desc, hw_id in list_ports.comports():
        print "found - %s,%s,%s"%(port_name,port_desc,hw_id)
        with serial.Serial(port=port_name, **device_serial_settings) as ser:
            ser.write(status_request_string)
            if ser.readline().startswith(expected_response):
                device_port = port_name
                break
    if not device_port:
        raise UserWarning('Could not find a serial port belonging to '
            'the asymtek dispensemate.')
    return device_port

print "found port :%s:"%locate_port()
