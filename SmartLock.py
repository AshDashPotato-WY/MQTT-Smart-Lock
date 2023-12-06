import paho.mqtt.client as mqtt

# Define MQTT settings
MQTT_BROKER = "localhost"  # broker server's IP
MQTT_PORT = 1883
MQTT_TOPIC_LOCK = "smart_lock/control"
MQTT_TOPIC_ACTIVE_TEMP = "smart_lock/activate_temp"

# Initial state (locked)
# locked = 0, unlocked = 1
lock_state = 0

# Define permanent password and temporary password
perm_passwd = "123456"
temp_passwd = "98765"
temp_passwd_state = False  # initial temporary password state


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_LOCK)
    client.subscribe(MQTT_TOPIC_ACTIVE_TEMP)


def on_message(client, userdata, msg):
    global lock_state, temp_passwd_state
    payload = msg.payload.decode()

    if msg.topic == MQTT_TOPIC_LOCK:
        password, command = payload.split(',')
        if password == perm_passwd or (password == temp_passwd and temp_passwd_state):
            if command == "unlock":
                lock_state = 1
                client.publish("smart_lock/status", "Unlock successful")
            elif command == "lock":
                lock_state = 0
                client.publish("smart_lock/status", "Lock successful")
            else:
                client.publish("smart_lock/status", "Invalid command")
        elif password != perm_passwd and not (password == temp_passwd and temp_passwd_state):
            client.publish("smart_lock/status", "Invalid password")
    elif msg.topic == MQTT_TOPIC_ACTIVE_TEMP:
        if payload == perm_passwd:
            temp_passwd_state = True  # activate temporary password
            client.publish("smart_lock/temp_status", "Temporary password activated successfully")
        else:
            client.publish("smart_lock/temp_status", "Invalid password")


# Set up MQTT client
client = mqtt.Client("SmartLock")
client.on_connect = on_connect
client.on_message = on_message

# Last Will Testament (LWT)
client.will_set("smart_lock/notification", "the lock is broken", 0, False)

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT loop
client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Smart Lock script terminated.")
    client.disconnect()
    client.loop_stop()
