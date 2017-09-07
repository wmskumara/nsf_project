import time
from sensor_reading_class import *
import math
w = 800         #weight of green leaf
f1 = 728705.0448
f2 = 219.5551
f3 = -1998.3448
f4 = 1146.5436
f5 = -6121.8327
mwb = 77.5      #moisture on wet basis
mdb = mwb * 100 / (100 - mwb)
lhv = 2270
T1 = 20         #wet bulb temp in celcius
ts = T1 + 273
dt = 5.0
area1 = 28.4924 #Area leaf bed sq.m.
area2 = 0.8245  #Area air inlet sq.m.
n = 3           #no of layers
tol = 60000     #Duration in seconds
begin = True


cr_time = time.strftime("%H:%M:%S")
print("cr_time", cr_time)

mm1 = [None]*3#create 3 spaces for moisture data layer by layer
mm2 = [None]*3#create 3 spaces for moisture data layer by layer
ss1 = [None]*3
ss2 = [None]*3
sr1 = sensor_data()

def calK():#call when needed
   tc = sr1.find_true_temp(adc.read_voltage(1))#inlet temperature in celcius
   tx = (tc *9)/5 + 32
   RH = sr1.find_trueRH_sr1(adc.read_voltage(2),tc)#relative humidity as a %
   ta = float(tc) + 273.15 #float use because from file read as a string variable
   aw = float(sr1.find_trueRH_sr1(adc.read_voltage(2),tc))/100
   Tw = tc*math.atan(0.151977*(RH + 8.313659)**(.5))+ math.atan(tc + RH) -math.atan(RH - 1.676331)+ 0.00391838*(RH)**(1.5) * math.atan(0.023101*RH) -4.686035
   ty = (Tw *9)/5 +32 #Tw - wet bulb temperature
   Tdw = tx - ty      #hygrometric difference
   #print('temp = ' ,tc , ' :  humidity = ', aw , 'wet bulb tem = ' , round(Tw, 2) ,  'hygrometric difference = ', round(Tdw, 2) )
   RR = (f2 * aw**3 + f3 * aw**2 + f4 * aw + f5)/ta
   KK = f1 * math.exp(RR)
   return KK

def calWB():
   tc = sr1.find_true_temp(adc.read_voltage(1))
   tx = (tc *9)/5 + 32
   #print ('tc  : ', tc)        
   RH = sr1.find_trueRH_sr1(adc.read_voltage(2),tc)
   Tw = tc*math.atan(0.151977*(RH + 8.313659)**(.5))+ math.atan(tc + RH) -math.atan(RH - 1.676331)+ 0.00391838*(RH)**(1.5) * math.atan(0.023101*RH) -4.686035
   ty = (Tw *9)/5 +32
   Tdw = tx - ty
   #print('temp = ' ,tc , ' :  humidity = ', aw , 'wet bulb tem = ' , round(Tw, 2) ,  'hygrometer difference = ', round(Tdw, 2) )
   #print(Tdw)
   return Tdw

while (True):   
   temp=sr1.find_true_temp(adc.read_voltage(1))
   RH1=sr1.find_trueRH_sr1(adc.read_voltage(2),temp)
   RH2=sr1.find_trueRH_sr2(adc.read_voltage(2),temp)
   print("Temp", temp)
   print("RH1", RH1)
   print("RH2", RH2)
   if temp is not None and RH1 is not None and RH2 is not None:
      avg_temp = round(temp,1)
      avg_RH = round((RH1 + RH2) / 2,1)
      print("avg_temp", avg_temp)
      print("avg_RH", avg_RH)
      ta = avg_temp + 273.15
      tc = avg_temp
      aw = round(avg_RH / 100,1)
      print("aw", aw)
      me =(55.49942677-0.1272*ta)*(aw/(1-aw))**0.2275
      print("Me :", me)      
      ps = .61078 * math.exp(tc * 17.2694 / (tc + 238.3))
      x = .622 * aw *ps / (101.325 - ps * aw)
      e = (1.007 * tc - .026) + x * (2501 + 1.84 * tc)
      k = calK()
      total = 0
      for l in range(0,3):
         if begin:
            print("First time only")
            m1 = mdb
            ts1 = ts
            print("m1", m1)
            print("ts1", ts1)            
         else:
            print("After that")
            m1 = mm1[l]
            ts1 = ss1[l]
            print("m2", m1)
            print("ts2", ts1)              
         V = ((0.000029127032475) * m1**2 - 0.0014472679037 * m1 + 7.3237700916) * area2 / area1
         dl = (.0011 * m1 - 0.0749)/n
         mm2[l] = m1 - k * (m1 - me) * dt / 60
         mm1[l] = mm2[l]
         g = (V * area1 * 353.3 /ta) * 60
         ha = .0025 *g
         md =  m1/((100+m1))
         Cps = .827 + 3.348 * md
         mmwb = m1 * 100 / (m1 + 100)
         wt = w * (100 - mwb)/(100 - mmwb)
         Ros =wt/(area1*dl*n)
         cpintoros = Cps * Ros
         a = ha/cpintoros   


         dhoverdt = ((.559230440794886 / me) * ((55.49942677 - .12722887132 * ta) / me)**3.3954680647) / ((((55.49942677-.12722887132*ta)/me)**4.3954680647+1)**2)
         dpsoverdt = 4114.3 * ps/(tc + 238.3)**2
         ERH = 1 / (((33.5835 - .0518 * ta) / me)**4.5537 + 1)
         dpstoverdt = dhoverdt * ps + dpsoverdt * ERH
         S = (0.461917 * ta) / (aw * ps) - 0.001
         q = dpstoverdt * S * ta
         b = (k * q) / Cps

         ss2[l] = ts1 + (a * (ta - ts1) - b * (m1 - me) / 100) * dt/60
         ss1[l] = ss2[l]
         k2 = Ros * k / g
         x = x + k2 * (m1 - me) * dl
         h = ha / g
         e = e + (lhv * k2 * (m1 - me) - h *(ta -ts1)) * dl
         tc = (e + 0.026 - 2501 * x) / (1.007 + 1.84 * x)
         ta = tc + 273
         P = 101.325*x/(.622+x)
         ps = .61078*math.exp(tc*17.2694/(tc+238.3))

         aw = P/ps
         if aw > 1:
            aw= .99

         d= (f2 * aw**3 + f3 * aw**2 + f4 * aw + f5) / ta
         k = f1* (math.exp(d))
         me = (55.49942677 - 0.12722887132 * ta) * (aw / (1 - aw))**0.22750705619522
         mmwb = mm1[l] * 100 / (mm1[l] + 100)
         total += mmwb;
      average = total/3
      hy_diff = calWB()



      #print ('Time :  ', t)
      print ('Average moisture in wet basis : ', round(average, 3))
      #print ('Hygro Meter Defference :', round(hy_diff, 4))
   
      print("TEmprature :", round(temp,0))
      print("RH1 :", int(round(RH1)))
      print("RH2 :", int(round(RH2)))
      avg_rh_val = (int(round(RH1))+int(round(RH2)))/2
      print("Average RH", avg_rh_val)
      print(time.strftime("%H:%M:%S"))
      begin = False
      time.sleep(1)
   





