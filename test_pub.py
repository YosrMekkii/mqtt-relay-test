import paho.mqtt.publish as publish

publish.single("rfid/scan", '{"tag_id":"TEST123","timestamp":1234567890}', hostname="localhost", port=1884)
print("Message publié sur Mosquitto")