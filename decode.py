def decode_visibility(code):
    vis_table = {
        "90": "Less than 50 m",
        "91": "50 m",
        "92": "200 m",
        "93": "500 m",
        "94": "1 km",
        "95": "2 km",
        "96": "4 km",
        "97": "10 km",
        "98": "20 km",
        "99": "Greater than 50 km"
    }

    if code in vis_table:
        return vis_table[code]

    num = int(code)

    if num <= 50:
        return f"{num/10:.1f} km"

    return "Unknown"


def decode_synop(station_id, year, month, day, hour, minute, synoptic_message):

    groups = synoptic_message.split()

    # Visibility
    vis_code = groups[3][3:5]
    visibility = decode_visibility(vis_code)

    # Wind
    wind_group = groups[4]
    wind_direction = int(wind_group[1:3]) * 10
    wind_speed = int(wind_group[3:5])

    # Temperature
    temp_group = groups[5]
    temperature = int(temp_group[2:]) / 10

    if temp_group[1] == "1":
        temperature = -temperature

    # Dew Point
    dew_group = groups[6]
    dew_point = int(dew_group[2:]) / 10

    if dew_group[1] == "1":
        dew_point = -dew_point

    # Station Pressure
    pressure_group = groups[7]
    station_pressure = int(pressure_group[1:]) / 10

    if station_pressure < 100:
        station_pressure += 1000
    else:
        station_pressure += 900

    # Sea Level Pressure
    slp_group = groups[8]
    sea_level_pressure = int(slp_group[1:]) / 10

    if sea_level_pressure < 100:
        sea_level_pressure += 1000
    else:
        sea_level_pressure += 900

    return {
        "station": str(station_id),
        "date": f"{year:04d}-{month:02d}-{day:02d}",
        "time": f"{hour:02d}:{minute:02d}",
        "visibility": visibility,
        "wind": f"{wind_direction:03d}° at {wind_speed} m/s",
        "temperature": f"{temperature:.1f}°C",
        "dew_point": f"{dew_point:.1f}°C",
        "station_pressure": f"{station_pressure:.1f} hPa",
        "sea_level_pressure": f"{sea_level_pressure:.1f} hPa"
    }


# ------------------------
# TEST DATA
# ------------------------

synoptic_message = "AAXX 01004 43150 31996 20503 10216 20181 30061 40137"

decoded = decode_synop(
    "43150",
    2000,
    1,
    1,
    0,
    0,
    synoptic_message
)

print("Station:", decoded["station"])
print("Date:", decoded["date"])
print("Time:", decoded["time"])
print("Visibility:", decoded["visibility"])
print("Wind:", decoded["wind"])
print("Temperature:", decoded["temperature"])
print("Dew Point:", decoded["dew_point"])
print("Station Pressure:", decoded["station_pressure"])
print("Sea Level Pressure:", decoded["sea_level_pressure"])