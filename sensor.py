import json
from os import execv
import sys
from time import sleep

from Adafruit_ADS1x15 import ADS1015
from redis import StrictRedis
import requests
from RPi import GPIO

import constval
from logger import Logger


class Sensor:
    def __init__(self):
        self._gpio_pos = constval.GPIO_POS
        self._adc = ADS1015()
        self._moist = -1
        self._converted_moist = 0
        self._redis = StrictRedis(host='localhost', port=6379, db=0)
        self._logger = Logger('sensor.py')
        self._url = constval.URL
        self._field_capacity = constval.SOIL_FIELD_CAPACITY

    def _range_map(self, x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

    def _clear_gpio(self):
        GPIO.output(self._gpio_pos, GPIO.HIGH)
        GPIO.cleanup()

    def _shutdown(self):
        self._logger.log_info("Shutting down...")
        self._clear_gpio()
        sys.exit()

    def _restart(self):
        self._logger.log_info("Restarting...")
        self._clear_gpio()
        execv(sys.executable, ['python3'] + sys.argv)
        sys.exit()

    def _mprint(self):
        self._logger.log_info("Current plant moisture: [" + str(self._converted_moist) + " (" + str(self._moist) + ")]")

    def _http_post(self):
        try:
            headers = {"Content-Type": "application/json", "level": self._converted_moist}
            payload = {"level": self._converted_moist}
            r = requests.post(self._url, data=json.dumps(payload), headers=headers)
            self._logger.log_info(str(r))
            r2 = requests.get(url=constval.MAIN_URL + "sensor?action=get_field_capacity")
            # print(r)
            data = r2.json()
            field_capacity = data['field_capacity']
            self._logger.log_info("Field Capacity: " + str(field_capacity))
            self._field_capacity = field_capacity
            sleep(0.25)
        except requests.exceptions.ConnectionError as e:
            self._logger.log_error(str(e))
        except requests.exceptions.HTTPError as e:
            self._logger.log_error(str(e))
        except requests.exceptions.Timeout as e:
            self._logger.log_error(str(e))
        except requests.exceptions.TooManyRedirects as e:
            self._logger.log_error(str(e))
        except requests.exceptions.RequestException as e:
            self._logger.log_error(str(e))

    def _get_moist(self):
        self._moist = self._adc.read_adc(0, gain=constval.GAIN)
        self._converted_moist = str(self._range_map(self._moist, constval.TOTALLY_DRY, constval.TOTALLY_WET, constval.DRY, constval.WET)) + '%'
        self._redis.set('moist', self._converted_moist)
        self._http_post()

    def _open_pump(self):
        GPIO.output(self._gpio_pos, GPIO.HIGH)
        self._get_moist()
        self._mprint()
        sleep(0.5)

    def _close_pump(self):
        GPIO.output(self._gpio_pos, GPIO.LOW)
        self._get_moist()
        self._mprint()

    def _check_moisture_level_on_loop(self):
        self._get_moist()
        self._mprint()
        while True:
            self._get_moist()
            # self._mprint()
            if self._moist <= self._field_capacity: # constval.SOIL_FIELD_CAPACITY: # constval.SOIL_WILTING_POINT:
                self._get_moist()
                # self._mprint()
                # print("debug_a")
            elif self._moist > self._field_capacity: # constval.SOIL_FIELD_CAPACITY: # >= constval.SOIL_WILTING_POINT:
                self._mprint()
                self._logger.log_info("Plant needs water! Watering...")
                self._open_pump()
                # print("debug_b")
                while True:
                    self._get_moist()
                    self._mprint()
                    if self._moist <= self._field_capacity: # constval.SOIL_FIELD_CAPACITY: # or self._moist < constval.SOIL_WILTING_POINT - 50:
                        self._close_pump()
                        # print("debug_c")
                        self._mprint()
                        self._logger.log_info("Plant okay!")
                        break
                    sleep(1)
            sleep(1)

    def _configure_gpio(self):
        self._logger.log_info("Configuring GPIO")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._gpio_pos, GPIO.OUT)
        self._close_pump()

    def main(self):
        self._logger.log_info("Starting up...")
        try:
            self._configure_gpio()
            self._check_moisture_level_on_loop()
        except KeyboardInterrupt:
            self._shutdown()
        except OSError as exception:
            self._logger.log_error(str(exception))
            self._restart()


if __name__ == "__main__":
    sensor = Sensor()
    sensor.main()

