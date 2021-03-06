import time
import sensor_reading_class import *

while (True):
  src1 = sensor_data()
  temp1 = src1.find_true_temp(adc.read_voltage(1))
  RH1 = src1.find_trueRH_sr1(adc.read_voltage(2),temp1) #send two parameters rh_sensor voltage & temprature
  temp2 = src1.find_true_temp(adc.read_voltage(3))
  RH2 = src1.find_trueRH_sr2(adc.read_voltage(4),temp2) #send two parameters rh_sensor voltage & temprature
  
  print("Temprature sr1 :", int(round(temp1)))
  print("RH sr1 :", int(round(RH1)))
  print("Temprature sr2 :", int(round(temp1)))
  print("RH sr1 :", int(round(RH2)))
  print(time.strftime("%H:%M:%S")) # print current system time
  time.sleep(1) # delay for one second
