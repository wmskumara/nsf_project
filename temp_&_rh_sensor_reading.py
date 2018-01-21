from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import time
import os


i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCDifferentialPi(bus, 0x68, 0x69, 18)


#temp1 = (round(adc.read_voltage(2)*243,1))
#temp2 = (round(adc.read_voltage(4)*243,1))
#temp3 = (round(adc.read_voltage(6)*243,1))
#temp4 = (round(adc.read_voltage(8)*243,1))

class sensor_data:
    slope1 = 0.0301
    slope2 = 0.0295


    def find_true_temp(self,input_temp_voltage):
        true_temp = input_temp_voltage * 230
        return true_temp
    def find_trueRH_sr1(self,input_RH_voltage,input_temp):
        real_vout = (99.6+94.1)/(94.1)*input_RH_voltage*10.4
        rh = (real_vout - 0.74) / self.slope2
        true_rh = rh / (1.0546-(input_temp*0.00216))
        return true_rh
    def find_trueRH_sr2(self,input_RH_voltage,input_temp):
        real_vout = (99.4+95.2)/(95.2)*input_RH_voltage*10.4
        rh = (real_vout - 0.74) / self.slope1
        true_rh = rh / (1.0546-(input_temp*0.00216))
        return true_rh
