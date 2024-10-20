def build_weather_api_url(venue_id, start_date, end_date):
    base_url = "https://api.open-meteo.com/v1/forecast"
    return f"{base_url}?venue_id={venue_id}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth"
