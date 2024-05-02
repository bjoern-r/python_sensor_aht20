import AHT20, WittyPi
import datetime, time

# Initialize an AHT20
aht20 = AHT20.AHT20(0)
wp = WittyPi.WittyPi(0)

while 1:

    # Fill a string with date, humidity and temperature
    data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(aht20.get_humidity()) + " %RH;" + "{:10.2f}".format(aht20.get_temperature()) + " °C"
    wpdata = wp.getAll()

    # Print in the console
    print(data)
    print(wpdata)

    # Append in a file
#    log = open("log.txt", "a")
#    log.write(data + "\n")
#    log.close()

    # Wait
    time.sleep(2)
