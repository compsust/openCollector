# 2025-03-31 Uploaded file

import random


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


def get_mock_value(record_id: str) -> float:
    print(record_id)
    if record_id == "temperature":
        return get_temp_rand()
    elif record_id == "humidity":
        return get_humidity_rand()
    elif record_id == "CO2":
        return get_co2_rand()
    elif record_id == "lux":
        return get_light_rand()
    elif record_id == "PM1.0" or record_id == "PM2.5" or record_id == "PM10":
        return get_matter_rand()
    else:
        raise ValueError("Invalid record ID")
