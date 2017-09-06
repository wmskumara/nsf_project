import time
import sensor_reading_class import *

while (True):
  src1 = sensor_data()
  temp1 = src1.find_true_temp(adc.read_voltage(1))
  RH1 = src1.find_trueRH_sr1(adc.read_voltage(2),temp1) #send two parameters rh_sensor voltage & temprature
  temp2 = src1.find_true_temp(adc.read_voltage(3))
  RH2 = src1.find_trueRH_sr2(adc.read_voltage(4),temp2) #send two parameters rh_sensor voltage & temprature
  
  print("Temprature sr1 :", round(temp1,2))
  print("RH sr1 :", round(RH1,2))
  print("Temprature sr2 :", round(temp1,2))
  print("RH sr1 :", round(RH2,2))
  print(time.strftime("%H:%M:%S"))
  time.sleep(1)
