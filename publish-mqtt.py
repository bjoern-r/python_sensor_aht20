#!/usr/bin/env /usr/bin/python3
import AHT20
import datetime, time
import paho.mqtt.client as mqtt
import json



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def publish_aht20_config(client):
    client.publish('homeassistant/sensor/BOB-Ambient/bob-ambient-T/config', '{"device_class":"temperature","name":"Temperature","unit_of_measurement":"°C","value_template":"{{ value_json.temperature|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/ambient","unique_id":"bob-ambient-T","device":{"identifiers":["BOB-Ambient"],"name":"BOB-Ambient","model":"AHT20","manufacturer":"aht"},"expire_after":600}')
    client.publish('homeassistant/sensor/BOB-Ambient/bob-ambient-H/config', '{"device_class":"humidity","name":"Humidity","unit_of_measurement":"%","value_template":"{{ value_json.humidity|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/ambient","unique_id":"bob-ambient-H","device":{"identifiers":["BOB-Ambient"],"name":"BOB-Ambient","model":"AHT20","manufacturer":"aht"},"expire_after":600}')

def publish_wittypi_config(client):
    client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-T/config', '{"device_class":"temperature","name":"Temperature","unit_of_measurement":"°C","value_template":"{{ value_json.temperature|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/wittypi","unique_id":"bob-wp-T","device":{"identifiers":["BOB-WittyPi"],"name":"BOB-WittyPi","model":"LM75B","manufacturer":"WittyPi"},"expire_after":600}')
    #client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-H/config', '{"device_class":"humidity","name":"Humidity","unit_of_measurement":"%","value_template":"{{ value_json.humidity|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/ambient","unique_id":"bob-ambient-H","device":{"identifiers":["BOB-Ambient"],"name":"BOB-Ambient","model":"AHT20","manufacturer":"aht"},"expire_after":600}')

INTERVAL=30
MQTT_HOST = '10.192.123.2'
#MQTT_HOST = '192.168.78.25'

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time()

# Initialize an AHT20
aht20 = AHT20.AHT20(0)
# init smbus to wittypi
wp = WittyPi.WittyPi(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sensor", password="xxx")
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_HOST, 1883, 60)

client.loop_start()

publish_aht20_config(client)
publish_wittypi_config(client)
try:
    while True:
        # Fill a string with date, humidity and temperature
        hum = aht20.get_humidity()
        temp = aht20.get_temperature()

        sensor_data['temperature'] = round(temp, 2)
        sensor_data['humidity'] = round(hum, 2)

        wittypi_data = wp.getAll()

        # Print in the console
        #data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(hum) + " %RH;" + "{:10.2f}".format(temp) + " °C"
        #print(data)
        # Sending humidity and temperature data to broaker
        client.publish('v1/bob/ambient', json.dumps(sensor_data), 1)
        client.publish('v1/bob/wittypi',json.dumps(wittypi_data),1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        sendcount += 1
        if sendcount > 20:
            sendcount = 0
            publish_aht20_config(client)
            publish_wittypi_config(client)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
