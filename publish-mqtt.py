#!/usr/bin/env /usr/bin/python3
import AHT20,WittyPi
import datetime, time
import paho.mqtt.client as mqtt
import json



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def publish_aht20_config(client):
    send_retain=True
    client.publish('homeassistant/sensor/BOB-Ambient/bob-ambient-T/config', '{"device_class":"temperature","name":"Temperature","unit_of_measurement":"°C","value_template":"{{ value_json.temperature|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/ambient","unique_id":"bob-ambient-T","device":{"identifiers":["BOB-Ambient"],"name":"BOB-Ambient","model":"AHT20","manufacturer":"aht"},"expire_after":600}',retain=send_retain)
    client.publish('homeassistant/sensor/BOB-Ambient/bob-ambient-H/config', '{"device_class":"humidity","name":"Humidity","unit_of_measurement":"%","value_template":"{{ value_json.humidity|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/ambient","unique_id":"bob-ambient-H","device":{"identifiers":["BOB-Ambient"],"name":"BOB-Ambient","model":"AHT20","manufacturer":"aht"},"expire_after":600}',retain=send_retain)

def publish_wittypi_config(client):
    send_retain=True
    client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-T/config', '{"device_class":"temperature","name":"Temperature","unit_of_measurement":"°C","value_template":"{{ value_json.temperature|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/wittypi","unique_id":"bob-wp-T","device":{"identifiers":["BOB-WittyPi"],"name":"BOB-WittyPi","model":"LM75B","manufacturer":"WittyPi"},"expire_after":600}',retain=send_retain)
    client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-I/config', '{"device_class":"current","name":"Output Current","unit_of_measurement":"A","value_template":"{{ value_json.output_current|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/wittypi","unique_id":"bob-wp-I","device":{"identifiers":["BOB-WittyPi"],"name":"BOB-WittyPi","manufacturer":"WittyPi"},"expire_after":600}',retain=send_retain)
    client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-Vo/config', '{"device_class":"voltage","name":"Output Voltage","unit_of_measurement":"V","value_template":"{{ value_json.output_voltage|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/wittypi","unique_id":"bob-wp-Vo","device":{"identifiers":["BOB-WittyPi"],"name":"BOB-WittyPi","manufacturer":"WittyPi"},"expire_after":600}',retain=send_retain)
    client.publish('homeassistant/sensor/BOB-WittyPi/bob-wp-Vi/config', '{"device_class":"voltage","name":"Input Voltage","unit_of_measurement":"V","value_template":"{{ value_json.input_voltage|float|round(2) }}","state_class":"measurement","state_topic":"v1/bob/wittypi","unique_id":"bob-wp-Vi","device":{"identifiers":["BOB-WittyPi"],"name":"BOB-WittyPi","manufacturer":"WittyPi"},"expire_after":600}',retain=send_retain)

INTERVAL=30
#MQTT_HOST = '10.192.123.2'
MQTT_HOST = '192.168.78.96'
USE_WITTIPY = True
USE_AHT = True

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time()

# Initialize an AHT20
if USE_AHT:
    aht20 = AHT20.AHT20(0)
# init smbus to wittypi
if USE_WITTIPY:
    wp = WittyPi.WittyPi(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sensor", password="xxx")
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_HOST, 1883, 60)

client.loop_start()
sendcount=0

if USE_AHT:
    publish_aht20_config(client)
if USE_WITTIPY:
    publish_wittypi_config(client)
try:
    while True:
        # Fill a string with date, humidity and temperature
        if USE_AHT:
            hum = aht20.get_humidity()
            temp = aht20.get_temperature()

            sensor_data['temperature'] = round(temp, 2)
            sensor_data['humidity'] = round(hum, 2)

            # Print in the console
            #data = str(datetime.datetime.now()) + ";" + "{:10.2f}".format(hum) + " %RH;" + "{:10.2f}".format(temp) + " °C"
            #print(data)
            # Sending humidity and temperature data to broaker
            client.publish('v1/bob/ambient', json.dumps(sensor_data), 1)

        if USE_WITTIPY:
            wittypi_data = wp.getAll()
            # {'input_voltage': 4.42, 'output_voltage': 5.18, 'temperature': 33.0, 'output_current': 0.64, 'powermode': 0}
            client.publish('v1/bob/wittypi',json.dumps(wittypi_data),1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        sendcount += 1
        if sendcount > 80:
            sendcount = 0
            if USE_AHT:
                publish_aht20_config(client)
            if USE_WITTIPY:
                publish_wittypi_config(client)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
