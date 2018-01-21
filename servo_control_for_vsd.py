import RPi.GPIO as GPIO #Import the GPIO library
import time #Import time library

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(16, GPIO.OUT)

pwm = GPIO.PWM(16, 50)
pwm.start(7.5)



try:
    while True:    
        pwm.ChangeDutyCycle(10.6)
        time.sleep(5)
        pwm.ChangeDutyCycle(9.7)
        time.sleep(5)
        pwm.ChangeDutyCycle(9.0)
        time.sleep(5)
        pwm.ChangeDutyCycle(8.3)
        time.sleep(5)
        pwm.ChangeDutyCycle(7.6)
        time.sleep(5)
        pwm.ChangeDutyCycle(6.8)
        time.sleep(5)
        pwm.ChangeDutyCycle(6.2)
        time.sleep(5)
        pwm.ChangeDutyCycle(5.6)
        time.sleep(5)
        pwm.ChangeDutyCycle(5.1)
        time.sleep(5)
        pwm.ChangeDutyCycle(4.7)
        time.sleep(5)
        pwm.ChangeDutyCycle(3.7)
        time.sleep(5)
            
        
except KeyboardInterrupt:
    GPIO.cleanup()
