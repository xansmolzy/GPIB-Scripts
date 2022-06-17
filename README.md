# GPIB-Scripts
GPIB script repository for logging various things

## How to install?
This repository is mainly designed to work with fenrir-naru GPIB adapter. https://github.com/fenrir-naru/gpib-usbcdc
This adapter has as of writing and to my knowledge issues interfacing with PyVisa thus a very similar library is used here https://github.com/Decee1/GPIBprologix
Further plotly-dash is used for visualization of data.
This all is designed to run in a raspberry pi, so BME280 sensor can be used if I2C is enabled.

1) follow installation instructions of https://github.com/Decee1/GPIBprologix
2) pip install plotly bme280 smbus pandas matplotlib statistics os time datetime csv
