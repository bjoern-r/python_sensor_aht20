from smbus import SMBus
import time

def get_normalized_bit(value, bit_index):
    # Return only one bit from value indicated in bit_index
    return (value >> bit_index) & 1

WP_I2C_ADDR = 0x08
WP_I2C_ID=0
WP_I2C_VOLTAGE_IN_I=1
WP_I2C_VOLTAGE_IN_D=2
WP_I2C_VOLTAGE_OUT_I=3
WP_I2C_VOLTAGE_OUT_D=4
WP_I2C_CURRENT_OUT_I=5
WP_I2C_CURRENT_OUT_D=6
WP_I2C_POWER_MODE=7
WP_I2C_LV_SHUTDOWN=8
WP_I2C_ALARM1_TRIGGERED=9
WP_I2C_ALARM2_TRIGGERED=10
WP_I2C_ACTION_REASON=11
WP_I2C_FW_REVISION=12

WP_I2C_LM75B_TEMPERATURE=50

class WittyPi:
    # I2C communication driver for WittyPi, using only smbus2

    def __init__(self, bus=0):
        self._busnr=bus;
        self.i2c_bus=SMBus(self._busnr)
        # Check ID
        fw_id = self.get_fw_id()
        if fw_id == 55:
            print("WittyPi 4 L3V7 with FW",self.get_fw_revision(), "found")

    def get_input_voltage(self):
        i = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_VOLTAGE_IN_I)
        d = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_VOLTAGE_IN_D)
        res = i + float(d)/100.
        return res

    def get_power_mode(self):
        b = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_POWER_MODE)
        return b # int 0 or 1

    def get_output_voltage(self):
        i = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_VOLTAGE_OUT_I)
        d = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_VOLTAGE_OUT_D)
        return float(i) + float(d)/100.


    def get_output_current(self):
        i = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_CURRENT_OUT_I)
        d = self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_CURRENT_OUT_D)
        return float(i) + float(d)/100.


    def getAll(self):
        wittypi = {}
        #UTCtime,localtime,timestamp = get_rtc_timestamp()
        #wittypi['DateTime'] = localtime.strftime("%Y-%m-%d_%H-%M-%S")
        #wittypi['timestamp'] = timestamp
        wittypi['input_voltage'] = self.get_input_voltage()
        wittypi['output_voltage'] = self.get_output_voltage()
        wittypi['temperature'] = self.get_temperature()
        wittypi['output_current'] = self.get_output_current()
        wittypi['powermode'] = self.get_power_mode()
        return wittypi

    def get_fw_id(self):
        return self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_ID)

    def get_fw_revision(self):
        return self.i2c_bus.read_byte_data(WP_I2C_ADDR, WP_I2C_FW_REVISION)

    def get_temperature(self):
        d = self.i2c_bus.read_i2c_block_data(WP_I2C_ADDR, WP_I2C_LM75B_TEMPERATURE,2)
        val = ((d[0]<<3)|(d[1]>>5))
        if val >= 0x400:
            val = (val&0x3FF)-1024
        return val*0.125
'''
    def get_status_busy(self):
        # Get the busy bit
        return get_normalized_bit(self.get_status(), AHT20_STATUSBIT_BUSY)
            
    def get_measure(self):
        # Get the full measure

        # Command a measure
        self.cmd_measure()

        # Check if busy bit = 0, otherwise wait 80 ms and retry
        while self.get_status_busy() == 1:
            time.sleep(0.08) # Wait 80 ns
        
        # TODO: do CRC check

        # Read data and return it
        return self.i2c_bus.read_i2c_block_data(AHT20_I2CADDR, 0x0, 7)

    def get_temperature(self):
        # Get a measure, select proper bytes, return converted data
        measure = self.get_measure()
        measure = ((measure[3] & 0xF) << 16) | (measure[4] << 8) | measure[5]
        measure = measure / (pow(2,20))*200-50
        return measure

    def get_humidity(self):
        # Get a measure, select proper bytes, return converted data
        measure = self.get_measure()
        measure = (measure[1] << 12) | (measure[2] << 4) | (measure[3] >> 4)
        measure = measure * 100 / pow(2,20)
        return measure
'''