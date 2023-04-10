import aiohttp
import asyncio
import json
import os

from dotenv import load_dotenv

load_dotenv()


async def fetch_weatherapi_temperature(api_key, latitude, longitude, aqi):
	url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}&aqi={aqi}"
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 200:
				data = await response.text()
				weather_data = json.loads(data)
				c_temp = weather_data['current']['temp_c']
				return c_temp
			else:
				return None


async def weather_1():
	api_key = os.getenv("KEY_WEATHERAPI")
	latitude = 46.481534
	longitude = 30.735441
	aqi = "no"

	weather_weatherapi = await fetch_weatherapi_temperature(api_key, latitude, longitude, aqi)
	if weather_weatherapi:
		print(weather_weatherapi)
		return weather_weatherapi
	else:
		print("Error")


async def fetch_m3o_temperature(api_token, latitude, longitude):
	url = 'https://api.m3o.com/v1/weather/Now'
	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {api_token}'
	}
	location = f'{latitude},{longitude}'
	payload = {
		'location': location
	}

	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=headers, json=payload) as response:
			if response.status == 200:
				data = await response.text()
				weather_data = json.loads(data)
				temp_c = weather_data["temp_c"]
				return temp_c
			else:
				return None


async def weather_2():
	api_token = os.getenv("KEY_M30")
	latitude = 46.481534
	longitude = 30.735441

	weather_m3o = await fetch_m3o_temperature(api_token, latitude, longitude)
	if weather_m3o:
		print(weather_m3o)
		return weather_m3o

	else:
		print("Failed to fetch weather forecast")


async def fetch_foreca_temperature(api_key, location):
	url = f'https://pfa.foreca.com/api/v1/forecast/15minutely/{location}'
	headers = {
		'Authorization': f'Bearer {api_key}'
	}

	async with aiohttp.ClientSession() as session:
		async with session.get(url, headers=headers) as response:
			if response.status == 200:
				data = await response.text()
				weather_data = json.loads(data)
				temp_c = weather_data["forecast"][0]["temperature"]
				return temp_c
			else:
				return None


async def weather_3():
	api_key = os.getenv("KEY_FORECA")
	location = '30.735441, 46.481534'

	weather_foreca = await fetch_foreca_temperature(api_key, location)
	if weather_foreca:
		print(weather_foreca)
		return weather_foreca
	else:
		print("Error fetching Foreca current weather data")


async def main():
	tasks = [weather_1(), weather_2(), weather_3()]
	results = await asyncio.gather(*tasks)

	if all(result is not None for result in results):
		average_temperature = sum(results) / len(results)
		print(f"Average temperature: {average_temperature:.2f}°C")
	else:
		print("Error: Unable to calculate the average temperature due to missing data from one or more APIs")


if __name__ == "__main__":
	asyncio.run(main())