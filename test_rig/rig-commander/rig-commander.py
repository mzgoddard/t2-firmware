import sys
import usb.core
import time

REQ_DIGITAL         = 1
REQ_ANALOG          = 2
REQ_READALLDIGITAL  = 3
REQ_SETANALOGMODE   = 4

ANALOGMODE_SINGLE   = 0
ANALOGMODE_STREAM   = 1

ADC_MAX_VALUE       = 4095
ADC_REFERENCE       = 2.5
CSA_GAIN            = 45
R_CSA               = 0.02

digital_pins = [
    'SHORT_USBO',
    'SHORT_USB1',
    'SHORT_PORTA33',
    'SHORT_PORTB33',
    'LED_READY',
    'LED_TESTING',
    'LED_PASS',
    'LED_FAIL',
    'UUTPOWER_USB',
    'UUTPOWER_VIN',
    'PORTA_MOSI',
    'PORTA_MISO',
    'PORTA_SCK',
    'PORTA_G3',
    'PORTA_SDA',
    'PORTA_SCL',
    'PORTA_G1',
    'PORTA_G2',
    'PORTB_G3',
    'PORTB_MOSI',
    'PORTB_SCK',
    'PORTB_MISO',
    'PORTB_SDA',
    'PORTB_SCL',
    'PORTB_G1',
    'PORTB_G2',
]

analog_pins = [
    'CURRENT_UUT', 
    'CURRENT_USB0', 
    'CURRENT_USB1', 
    'CURRENT_PORTA33', 
    'CURRENT_PORTB33', 
    'VOLTAGE_VREF', 
    'VOLTAGE_5VUSB1', 
    'VOLTAGE_5VUUT', 
    'VOLTAGE_PORTA33', 
    'VOLTAGE_12', 
    'VOLTAGE_33CP', 
    'VOLTAGE_PORTB33', 
    'VOLTAGE_18', 
    'VOLTAGE_33MT', 
    'VOLTAGE_5VUSB0', 
]

def pin_id (pin):
    p = pin.upper()
    if p in digital_pins:
        return digital_pins.index(p)
    elif p in analog_pins:
        return analog_pins.index(p)
    else:
        return -1

def serial_match (serial):
    return lambda dev: usb.util.get_string(dev, index = dev.iSerialNumber) == serial

def counts_to_volts (counts):
    return counts / ADC_MAX_VALUE * ADC_REFERENCE

def counts_to_amps (counts):
    return counts_to_volts(counts) * CSA_GAIN / R_CSA


class testalator (object):
    """docstring for testalator"""
    def __init__(self, serial):
        super(testalator, self).__init__()
        self.serial = serial
        self.dev = usb.core.find(idVendor = 0x59E3, idProduct = 0xCDA6, custom_match = serial_match(serial))
        if self.dev is None:
            raise ValueError('device is not connected')


    def digital (pin, state):
        return self.dev.ctrl_transfer(0xC0, REQ_DIGITAL, state, pin_id(pin), 64)

    def read_all_digital ():
        states = self.dev.ctrl_transfer(0xC0, REQ_READALLDIGITAL, 0, 0, 64)    
        return zip(digital_pins, states)

    def analog (pin):
        return self.dev.ctrl_transfer(0xC0, REQ_ANALOG, 0, pin_id(pin), 64)

    def set_analog_mode (pin, mode):
        return self.dev.ctrl_transfer(0xC0, REQ_SETANALOGMODE, mode, pin_id(pin), 64)


    # wrappers

    def power_helper (usb, vin):
        return (digital('UUTPOWER_USB', usb)[0], digital('UUTPOWER_VIN', vin)[0])

    def power (source = 'USB'):
        if str(source).upper() == 'VIN':
            return power_helper(False, True)
        elif (str(source).upper() in ('USB', 'ON', '1', 'TRUE')):
            return power_helper(True, False)
        else:
            return power_helper(False, False)

    def test_pass ():
        digital('LED_TESTING', 0)
        digital('LED_FAIL', 0)
        digital('LED_PASS', 1)

    def test_fail ():
        digital('LED_TESTING', 0)
        digital('LED_PASS', 0)
        digital('LED_FAIL', 1)

    def measure_current (pin):
        # configure the pin's ADC

        # return the converted value
        return counts_to_amps(read_adc(pin))

    def measure_voltage (pin):
        # configure the pin's ADC

        # return the converted value
        return counts_to_volts(read_adc(pin))


if __name__ == '__main__':
    pass
    