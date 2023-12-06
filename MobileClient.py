import paho.mqtt.client as mqtt
import time

# Define MQTT settings
MQTT_BROKER = "localhost"  # broker IP address
MQTT_PORT = 1883
MQTT_TOPIC_LOCK = "smart_lock/status"
MQTT_TOPIC_TEMP_STATUS = "smart_lock/temp_status"
MQTT_TOPIC_NOTIFICATION = "smart_lock/notification"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_LOCK)
    client.subscribe(MQTT_TOPIC_TEMP_STATUS)
    client.subscribe(MQTT_TOPIC_NOTIFICATION)


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode())

    if msg.topic == MQTT_TOPIC_TEMP_STATUS:
        print(f"Result: {payload}")
    elif msg.topic == MQTT_TOPIC_LOCK:
        print(f"Status: {payload}")
    elif msg.topic == MQTT_TOPIC_NOTIFICATION:
        print(f"Notification: {payload}")


# Set up MQTT client
client = mqtt.Client("MobileClient")
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT loop
client.loop_start()
time.sleep(2)

# Simulate sending unlock command
# Keep the script running
try:
    while True:
        command = input("Enter a number to control the lock\n1.lock\n2.unlock\n3.activate temporary password\n4.exit: ").strip()
        if command == "3":
            password = input("Enter the password: ").strip()
            client.publish("smart_lock/activate_temp", f"{password}")
        elif command == "1":
            password = input("Enter the password: ").strip()
            client.publish("smart_lock/control", f"{password},lock")
        elif command == "2":
            password = input("Enter the password: ").strip()
            client.publish("smart_lock/control", f"{password},unlock")
        elif command == "4":
            break
        else:
            print("Invalid command")
        time.sleep(3)
        pass
except KeyboardInterrupt:
    print("Client script terminated.")
    client.disconnect()
    client.loop_stop()
