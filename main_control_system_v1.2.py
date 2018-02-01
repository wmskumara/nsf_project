## include main program with maching straight line method and linear regression and find error of both exact points.



import time
import datetime
import math
import csv
import timeit

strtim = timeit.default_timer()
print(strtim)

## time started 18_1_25 / 9.31pm
w = 900         #weight of green leaf
f1 = 728705.0448
f2 = 219.5551
f3 = -1998.3448
f4 = 1146.5436
f5 = -6121.8327
req_moisture = 55
mwb = 80      #moisture on wet basis
mdb = mwb * 100 / (100 - mwb)
lhv = 2270
T1 = 21.5         #wet bulb temp in celcius
ts = T1 + 273
dt = 5.0
area1 = 28.4924 #Area leaf bed sq.m.
area2 = 0.8245  #Area air inlet sq.m.
n = 3           #no of layers
tol = 50     #Duration in seconds
mm1 = [None]*3#create 3 spaces for moisture data layer by layer
mm2 = [None]*3#create 3 spaces for moisture data layer by layer
ss1 = [None]*3
ss2 = [None]*3

crtime = []
moisture = []

t=1


def calK(data1): #call when needed
    tc = float(data1[0])#inlet temperature in celcius
    tx = (tc *9)/5 + 32
    RH = float(data1[1])#relative humidity as a %
    ta = float(tc) + 273.15 #float use because from file read as a string variable
    aw = float(data1[1])/100
    Tw = tc*math.atan(0.151977*(RH + 8.313659)**(.5))+ math.atan(tc + RH) -math.atan(RH - 1.676331)+ 0.00391838*(RH)**(1.5) * math.atan(0.023101*RH) -4.686035
    ty = (Tw *9)/5 +32 #Tw - wet bulb temperature
    Tdw = tx - ty      #hygrometric difference
    #print('temp = ' ,tc , ' :  humidity = ', aw , 'wet bulb tem = ' , round(Tw, 2) ,  'hygrometric difference = ', round(Tdw, 2) )
    RR = (f2 * aw**3 + f3 * aw**2 + f4 * aw + f5)/ta
    KK = f1 * math.exp(RR)
    return KK

def straight_line_method(init_mois,req_mois,tot_duration,time_stamp):
    moisture_in_given_timestamp = (((req_mois-init_mois)/tot_duration) * time_stamp[-1] + init_mois)
    return moisture_in_given_timestamp

def basic_linear_regression(x, y):
    # Basic computations
    # Y = ax + b
    length = len(x)
    #print("length of x = ", length)
    sum_x = sum(x)
    #print("sum of x = ", length)
    sum_y = sum(y)
    #print("sum of y = ", length)

    # Sx^2, and Sxy respectively.
    sum_x_squared = sum(map(lambda a: a * a, x))
    #print("sum_x_squared = ", sum_x_squared)
    sum_of_products = sum([x[i] * y[i] for i in range(length)])
    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))   # intercept
    b = (sum_y - a * sum_x) / length    # slope
    Y = (a*x[-1])+b     # y = ax + b
    return Y

def find_difference(real_time_mois, straight_line_mois):
    difference = real_time_mois - straight_line_mois
    return difference


with open('temp_rh_data.csv') as f:
	with open('moisture_out_by10sec.csv', 'a') as output:
		output.truncate()
		readCSV = csv.reader(f,delimiter=',')
		for data1 in readCSV:#process data every 30 data point 0,30,60 etc.
			ta = float(data1[0]) + 273.15
			tc = float(data1[0])
			aw = float(data1[1]) / 100
			me =(55.49942677-0.1272*ta)*(aw/(1-aw))**0.2275
			ps = .61078 * math.exp(tc * 17.2694 / (tc + 238.3))
			x = .622 * aw *ps / (101.325 - ps * aw)
			e = (1.007 * tc - .026) + x * (2501 + 1.84 * tc)
			k = calK(data1)
			total = 0

			for l in range(0,3):
				if(t == 1):
					m1 = mdb
					ts1 = ts
					print("first time only")
				else:
					m1 = mm1[l]
					ts1 = ss1[l]

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
				me = (55.49942677 - 0.1272 * ta) * (aw / (1 - aw))**0.2275
				mmwb = mm1[l] * 100 / (mm1[l] + 100)
				total += mmwb;                        #total=total+mmwb
			average = total/3
			crtime.append(t)
			moisture.append(average)
			print(t)
			print(average)
			print(crtime)
			#print(crtime[-1])
			print(moisture)
			if (t%10==0):
				given_point_val_of_linear_R = basic_linear_regression(crtime, moisture)
				given_point_val_of_straight_L = straight_line_method(mwb,req_moisture,50400,crtime)
				difference = find_difference(given_point_val_of_linear_R, given_point_val_of_straight_L)
				moiwttime = [t,difference]
				print(difference)
				del crtime[:]
				del moisture[:]
				writer = csv.writer(output, lineterminator = '\n')
				writer.writerow(moiwttime)
			else:
				pass


			#writer = csv.writer(output, lineterminator = '\n')
			#writer.writerow(moiwttime)
			t = t + 1

			#hy_diff = calWB(data1)
			#
			#date_time = datetime.datetime.now()
			#print("\n")
			#print("Dry bulb temperature:", data1[0])
			#print("Humidity:", data1[1])
			#print ('Time :  ', t)
			#print ('Average moisture in wet basis : ', round(average, 2))
			#print ('Hygro Meter Defference :', round(hy_diff, 4))

			#txt = str(t) + '\t' + str(round(average, 3)) + ' \t ' + str(round(hy_diff, 3)) + ' \n'   #write on next line using '\n'
			#file.write(txt)

			#xdata.append(t) #attaching numer't one by one
			#ydata.append(average)
			#self.on_running(xdata, ydata)

##			if(t==tol):
##				break
##			else:
##				pass
			time.sleep(1)
		elapsed = timeit.default_timer()-strtim
		#print(elapsed)
        #end time 2018.1.26 / 5.29
