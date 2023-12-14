from machine import Pin, I2C,PWM
import utime
import ssd1306

buzzer = PWM(Pin(14))

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

i2c = I2C(0, scl = Pin(17), sda= Pin(16), freq = 400000)
display = ssd1306.SSD1306_I2C(128,64,i2c)

def ultrasonnic():
    timepassed = 0
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    signaloff = 0
    signalon = 0
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    #distance = "{:.1f}".format(distance)
    return distance

while True:
    distance = ultrasonnic()
    buzzer.freq(200)
   # print(type(distance))
    #converted_distance = int(distance)
    if(distance < 3):
       buzzer.duty_u16(1000)
    else:
       buzzer.duty_u16(0)
        
    display.fill(0)
    printdistance = "{:.1f}".format(distance)
    display.text("The distance",0,0,1)
    display.text(printdistance,0,10,1)
    display.text("cm",25,10,1)
    display.show()

    print("Distance:", distance, "cm")

    utime.sleep(1)

