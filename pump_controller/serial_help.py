import serial
import serial.tools.list_ports

def list_serial_ports():

    """
    Lists information about all available serial ports.

    Parameters:
    - None

    Returns:
    - None

    Notes:
    - Uses the serial.tools.list_ports.comports() function to obtain a list of available serial ports.
    - Prints information about each port, including device name, description, and hardware ID.
    """


    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()

    # Print information about each port
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}, Hardware ID: {port.hwid}")

def get_serial_port():

    """
    Returns the device name of a USB serial port.

    Parameters:
    - None

    Returns:
    - str: Device name of the USB serial port.

    Raises:
    - Exception: Raised if no USB Serial Port is found. User is prompted to try again
      or define the port manually using list_serial_ports().
    """


    ports = serial.tools.list_ports.comports()

    for port in ports:
        if 'serial' in port.description.lower():
            return port.device
    raise Exception("ERROR: No USB Serial Port Found. Please try again or define port manually using list_serial_ports().")