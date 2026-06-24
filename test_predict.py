from src.ml.predict_aqi import predictor

sample = {
    "pm25": 90,
    "pm10": 170,
    "no2": 55,
    "so2": 18,
    "co": 1.3,
    "o3": 42,
    "temperature": 36,
    "humidity": 45,
    "wind_speed": 5.8
}

result = predictor.predict(sample)

print("Predicted AQI:", result)