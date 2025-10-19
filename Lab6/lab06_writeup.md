# Names: Jiwen Li, Cynthia Liu
## Lab 6
### Reflection Questions

4.1: Suppose you just cloned a repository that included one python file, my_first_file.py, and you now want to add a second file to your repository named my_second_file.py which contains the following code and push it to Github.com.
Code -
print("Hello World")
Complete the sequence of linux shell commands:
git clone git@github.com:my-name/my-imaginary-repo.git
touch "my_second_file.py"
echo 'print("Hello World")' > my_second_file.py
git add .
git commit -m "create second file"
git push


4.2: Describe the workflow you adopted for this lab (i.e. did you develop on your VM and push/pull to get code to your RPi, did you edit files directly on your RPi, etc.). Are there ways you might be more efficient in the next lab (i.e. learning a text-based editor so you can edit natively on the RPi, understanding Git commands better, etc.)?

ANSWER HERE AFTER

4.3: In the starter code, we added a 200 ms sleep. Suppose you needed to poll the ultrasonic ranger as fast as possible, so you removed the sleep function. Now, your code has just the function ultrasonicRead() inside a while loop. However, even though there are no other functions in the while loop, you notice there is a constant delay between each reading. Dig through the python library to find out why there is a constant delay. What is the delay amount? In addition, what communication protocol does the Raspberry Pi use to communicate with the Atmega328P on the GrovePi when it tries to read the ultrasonic ranger output using the `grovepi` python library?

There is a built in delay to the ultrasonicRead() function of 200 ms, which is why there is still a constant delay between each reading after the delay was removed from our code. The Raspberry Pi uses I2C communication protocol to communicate with the Atmega328P on the GrovePi, with the RPi as the leader and the GrovePi as the follower.

4.4: When you rotate the Grove Rotary Angle Sensor, its analog output voltage changes between 0 V and 5 V and the GrovePi library reports integer values between 0 and 1023. Explain how this conversion works and why the Raspberry Pi cannot do it directly.

It uses an ADC to convert voltage values between 0 and 5 V to an integer value between 0-1023 using a predefined equation for conversion that is linear. The RPi cannot do this directly because it doesn't have an ADC, the pins are digital only and therefore only have two logic states: high and low. This means it can't convert the input voltages to all those different integer values, but rather only two states.

4.5: Your LCD RGB Backlight screen is not displaying any text even though your code executes without errors. Describe how you would debug the issue. Include at least two terminal commands.
