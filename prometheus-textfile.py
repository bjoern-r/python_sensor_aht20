#!/usr/bin/env /usr/bin/python3
import AHT20
import time

# Initialize an AHT20
aht20 = AHT20.AHT20(0)

while 1:

    # Fill a string with date, humidity and temperature
    #data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(aht20.get_humidity()) + " %RH;" + "{:10.2f}".format(aht20.get_temperature()) + " °C"

    hum = aht20.get_humidity()
    temp = aht20.get_temperature()
    '''
    create a softline from /tmp/ambient.prom into /var/lib/prometheus/node-exporter
    ln -s /tmp/ambient.prom /var/lib/prometheus/node-exporter/ambient.prom
    '''
    # Write metrics to file in prometheus format
    log = open("/tmp/ambient.prom", "w")
    log.write("# HELP sensor_temp_celsius Ambient temperature\n")
    log.write("# TYPE sensor_temp_celsius gauge\n")
    log.write('sensor_temp_celsius{chip="aht20"} '+str(temp)+"\n")
    log.write("# HELP sensor_humidity_rh Ambient Relative Humidity\n")
    log.write("# TYPE sensor_humidity_rh gauge\n")
    log.write('sensor_humidity_rh{chip="aht20"} '+str(hum)+"\n")
    log.close()

    # Wait
    time.sleep(10)