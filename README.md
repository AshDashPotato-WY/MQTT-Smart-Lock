# MQTT-Smart-Lock

This repo simulates smart lock control by mobile phone users via MQTT protocols and Mosquitto server.

Functionalities of the Lock:
  1. Lock & unlock if given the correct password (permanent or temporary)
  2. Activate or deactivate the temporary password (assume the temporary password won’t change):
     • use the permanent password to activate/deactivate the temporary password
     • Once used to unlock the door, the temporary password should be disabled automatically.
  3. Send notifications if someone breaks the lock (LWT).
  4. After an operation, send the result back to the client

Both smart lock and mobile client are publisher and subscriber. 
Therefore, smart lock and mobile clients will process the commands sent from others and take actions.

Smart Lock topic model:
  1. topics SmartLock publishes and MobileClient subscribes:
     • "smart_lock/status": get lock status and result after mobile client sends command and correct password
     • "smart_lock/temp_status": activate temporary password
     • "smart_lock/notification": broadcast an alert about broken lock
  2. topics MobileClient publishes and SmartLock subscribes:
     • "smart_lock/control": receive commands and correct password from mobile client
     • "smart_lock/activate_temp": activate temporary password

     
################################################ 

Tips about using MAC computer as MQTT broker:
  1. install Homebrew: "/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  2. install Mosquitto: "brew install mosquitto"
  3. start Mosquitto: "/usr/local/opt/mosquitto/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf"
  4. stop Mosquitto: command key + dot key
  5. unstall Mosquitto: "brew uninstall moquitto"

If Mosquitto isn't stopped properly last time, then the error will show port 1883 is in use when the server starts again.
Solution:
  1. get PID of running process: ps ax | grep mosq
  2. kill the process: sudo kill -9 PID

Testing server and clients on different devices:
  1. add lines in configuration file:
        allow_anonymous true
        listener 1883 0.0.0.0
  2. restart Mosquitto :
       sudo service mosquitto restart
     or
       mosquitto --verbose --config-file /etc/mosquitto/conf.d/mosquitto.conf
