# Lab 5

## Team Members
- Jiwen Li
- Cynthia Liu

## Lab Question Answers

Part 1:
Question 1: What is dBm? What values are considered good and bad for WiFi signal strength?
dBm is decibel-milliwatts, which is used to measure power levels. For WiFi signal strength, the received power is measured in dBm. The values are negative, and the closer to zero it is, the stronger the signal is. Generally, above -60 would be considered good WiFi signal strength, and below -70 would be bad for WiFi signal strength.

Question 2: Why do we need to check the OS? What is the difference between the commands for each OS?
Checking the OS is requried because each OS uses different commands to get the signal strength information that we want. Linux uses iwconfig wlan0, Windows uses netsh wlan show interfaces, and Mac uses airport -I. They also return data differently, so the returned information needs to be processed differently based on the OS, which is why checking the OS is necessary, so that we can use the right commands and processes for data.

Question 3: In your own words, what is subprocess.check_output doing? What does it return?
It will run a specified system command with arguments and return the output of that command.

Question 4: In your own words, what is re.search doing? What does it return?
It searches through a string to find a specified pattern, and returns a Match when the pattern is found. If the pattern is not found, it returns None.

Question 5: In the Windows case, why do we need to convert the signal quality to dBm?
Unlike Linux and Mac, Windows does not report the signal quality directly in dBm, but rather as a percentage, so it has to be converted to dBm.

Question 6: What is the standard deviation? Why is it useful to calculate it?
The standard deviation measures how far the values are from the mean value, with low meaning the values are consistent and a high value meaning there is a lot of fluctuation in the data. In WiFi sampling, it's useful because it can show you how stable or reliable the WiFi signal strength was at a given point.

Question 7: What is a dataframe? Why is it useful to use a dataframe to store the data?
A dataframe is a labeled table (2D, has rows and columns). It is useful to use a dataframe to store the data because it is organized well and it makes it easy to analyze the data later.

Question 8: Why is it important to plot the error bars? What do they tell us?
Error bars are important because they help visualize how much the signal fluctuated at a given point, and how accurate the plotted datapoint is. By plotting them, we can see how stable the data (signal strength) might be (small data bars = more stable).

Question 9: What did you observe from the plot? How does the signal strength change as you move between locations? Why do you think signal strength is weaker in certain locations?
We observed that signal strength would increase or decrease as we moved to various locations. Generally, the signal strength was weaker as we moved further from the router, and became stronger when we were closer to the router. Signal strength is likely weaker in certain locations due to the distance from the router and the reliability of the signal at that given point, which could be affected by multiple factors of environment.

Part 2:
Question 1: How does distance affect TCP and UDP throughput?

Question 2: At what distance does significant packet loss occur for UDP?

Question 3: Why does UDP experience more packet loss than TCP?

Question 4: What happens if we increase the UDP bandwidth (-b 100M)?

Question 5: Would performance be different on 5 GHz Wi-Fi vs. 2.4 GHz?

...
