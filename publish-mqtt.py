import AHT20
import datetime, time
import paho.mqtt.client as mqtt
import json



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

INTERVAL=10
MQTT_HOST = '10.192.123.1'

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time()

# Initialize an AHT20
aht20 = AHT20.AHT20(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sensor", password="xxx")
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        # Fill a string with date, humidity and temperature
        hum = aht20.get_humidity()
        temp = aht20.get_temperature()

        data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(hum) + " %RH;" + "{:10.2f}".format(temp) + " °C"
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        # Print in the console
        print(data)
        # Sending humidity and temperature data to broaker
        client.publish('v1/bob/ambient', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
