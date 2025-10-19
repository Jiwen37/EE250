# Names: Jiwen Li, Cynthia Liu
## Lab 6
### Reflection Questions

4.1: Suppose you just cloned a repository that included one python file, my_first_file.py, and you now want to add a second file to your repository named
my_second_file.py which contains the following code and push it to Github.com.
Code -
print(“Hello World”)
Complete the sequence of linux shell commands:
git clone git@github.com:my-name/my-imaginary-repo.git
##complete the sequence
(Note: create the file using the `touch` command)

4.2: Describe the workflow you adopted for this lab (i.e. did you develop on your VM and push/pull to get code to your RPi, did you edit files directly on your RPi, etc.).
Are there ways you might be more efficient in the next lab (i.e. learning a text-based editor so you can edit natively on the RPi, understanding Git commands better, etc.)?

4.3: In the starter code, we added a 200 ms sleep. Suppose you needed to poll the ultrasonic ranger as fast as possible, so you removed the sleep function. Now,
your code has just the function ultrasonicRead() inside a while loop. However, even though there are no other functions in the while loop, you notice there is a
constant delay between each reading. Dig through the python library to find out why there is a constant delay. What is the delay amount? In addition, what communication protocol does the Raspberry Pi use to communicate with the
Atmega328P on the GrovePi when it tries to read the ultrasonic ranger output using the `grovepi` python library?

4.4: When you rotate the Grove Rotary Angle Sensor, its analog output voltage
changes between 0 V and 5 V and the GrovePi library reports integer values
between 0 and 1023. Explain how this conversion works and why the Raspberry
Pi cannot do it directly.

4.5: Your LCD RGB Backlight screen is not displaying any text even though your code
executes without errors. Describe how you would debug the issue. Include at
least two terminal commands.
