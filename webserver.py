from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import RPi.GPIO as GPIO
import time
import os

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

register_openers()

app = Flask(__name__)

# Template rendering example
@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
  return render_template('hello.html', name=name)

# JSON response example
@app.route("/json")
def json():
  return jsonify(first_name='John', last_name='Wayne')

#
# LED examples
#

LED_PIN = 24 # Set pin number we are using on the GPIO
ALARM_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT) # Configure the pin to be used as an output
GPIO.setup(ALARM_PIN, GPIO.OUT)
led_on = False
GPIO.output(LED_PIN, GPIO.LOW) # Initialize the pin with LOW (0=off)
GPIO.output(ALARM_PIN, GPIO.LOW)
upload_running = False

@app.route("/led/on")
def led_on():
  global led_on
  led_on = True
  GPIO.output(LED_PIN, GPIO.HIGH)
  return jsonify(led_on=led_on)

@app.route("/led/off")
def led_off():
  global led_on
  led_on = False
  GPIO.output(LED_PIN, GPIO.LOW)
  return jsonify(led_on=led_on)

@app.route("/led/toggle")
def led_toggle():
  global led_on
  led_on = not led_on
  GPIO.output(LED_PIN, GPIO.HIGH if led_on else GPIO.LOW)
  return jsonify(led_on=led_on)

@app.route("/file/upload")
def upload_picture():
  filename = request.args.get("filename")
  if not filename:
    return jsonify(message="Filename is missing")
  else:
    datagen, headers = multipart_encode({"image1": open(filename, "rb")})
    req = urllib2.Request("http://t8.azurewebsites.net/Files/upload", datagen, headers)
    urllib2.urlopen(req)
    os.remove(filename)
    return jsonify(message="File uploaded")

@app.route("/alarm/new")
def new_alarm():
  GPIO.output(ALARM_PIN, GPIO.HIGH)
  req = urllib2.Request('http://t8.azurewebsites.net/Alarms/Add')
  urllib2.urlopen(req)
  GPIO.output(ALARM_PIN, GPIO.LOW)
  return jsonify(message="Alarm created")

if __name__ == "__main__":
  # This will enable hot reloading, so you don't need to restart each time
  # after making a change
  # MAKE SURE TO DISABLE IN PRODUCTION
  app.debug = True

  app.run(host='0.0.0.0')

