# 2025-03-31 Uploaded file

import random
import time


def get_temp_rand():
    return round(random.uniform(18, 25), 2)


def get_humidity_rand():
    return round(random.uniform(30, 60), 2)


def get_co2_rand():
    return round(random.uniform(400, 1000), 2)


def get_matter_rand():
    return round(random.uniform(0, 12), 2)


def get_light_rand():
    return round(random.uniform(100, 500), 2)


def run_data_set():
    while True:
        print(f"Temperature: {get_temp_rand()} C")
        print(f"Humidity: {get_humidity_rand()} %")
        print(f"CO2: {get_co2_rand()} ppm")
        print(f"Particulate Matter: {get_matter_rand()} ug/m2")
        print(f"Light Intensity: {get_light_rand()} lux")
        print("-" * 30)  # Separator for readability
        time.sleep(2)


run_data_set()

# TO END SCRIPT CRTL+C in the terminal
