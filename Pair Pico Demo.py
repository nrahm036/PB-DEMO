#create (write) pwm signal on Pico A
#send said signal to Pico B
#interpret signal (at pico b)
#send back (to pico a)

import machine
import time
from machine import Pin
from machine import UART

#initialize UART comms Pico a to b 
uart = UART(1, 9600, tx=Pin(8), rx=Pin(9))
uart.init(9600, bits=8, parity=None, stop=1)

#esablishes pwm output on pico a 
p8 = machine.Pin(8)
pwm8 = machine.PWM(p8)
print(type(pwm8))
pwm8.freq(1000)                                                                          # Set PWM frequency to be sent to Pico B, on pin 8
pwm8.duty_u16(32768)                                                                      #1023 = 100% so 512 = 50%

#initialize reciever on pico b 8=tx, reciever pin
pwm_reciever = machine.PWM(Pin(8))

#(pico a) sends pwm signal, waits 10 seconds before sending signal again
while True:
    uart.write("Duty cycle is =" + str(pwm8.duty_u16()))
    time.sleep(10)
    
    recieved_message = ""
    #(pico b) recieves pwm and processes
    
    if uart.any():
        recieved_message = uart.read().decode() .strip()
        
        #checks if recieved_message has desired pwm value
        if "The PWM value is" in  recieved_message:
            pass
        elif "The anolog value is" in recieved_message:
            pass 
        else:
            #something weird happened?
            print ("This was not what I was expecting!")

        
            #expected_pwm_value = float(recieved_message.split(":")[1].strip()[:-1])

            # Split the string using ":" and convert to float 
            calculated_pwm_value = (pwm_reciever.duty_u16() / 65535) * 100              
            # 65535 is the max 16 bit value, this gives percent of duty cycle
            
            difference = expected_pwm_value - calculated_pwm_value
            print ("the measured pwm value was:{:.2F}%" .format(calculated_pwm_value))
            print ("the difference in pwm value was:{:.2F}%" .format(difference))
            uart.write("Received and Processed: {:.2f}%".format(calculated_pwm_value))  
            #sends response back to pico a, includes measured pwm value
            
# example changes
