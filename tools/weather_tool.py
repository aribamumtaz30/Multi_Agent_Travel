"""
Weather Tool

Uses Open-Meteo.
No API key required.
"""

import requests

from config.settings import Settings



class OpenMeteoWeatherTool:


    def geocode(
        self,
        city
    ):


        try:

            response=requests.get(

                Settings.GEOCODING_API_URL,

                params={

                    "name":city,

                    "count":1,

                    "format":"json"

                },

                timeout=20

            )


            data=response.json()


            result=data.get(
                "results",
                []
            )


            if result:

                return {

                    "latitude":
                    result[0]["latitude"],

                    "longitude":
                    result[0]["longitude"]

                }


        except Exception as e:

            print(
                f"Geocoding failed {e}"
            )


        return {}




    def get_weather(
        self,
        city
    ):


        coordinates=self.geocode(
            city
        )


        if not coordinates:

            return {

                "status":
                "Weather unavailable"

            }



        try:

            response=requests.get(

                Settings.WEATHER_API_URL,

                params={

                "latitude":
                coordinates["latitude"],


                "longitude":
                coordinates["longitude"],


                "current_weather":
                True

                },

                timeout=20

            )


            data=response.json()


            return {

                "temperature":
                data.get(
                    "current_weather",
                    {}
                ).get(
                    "temperature"
                ),

                "wind_speed":
                data.get(
                    "current_weather",
                    {}
                ).get(
                    "windspeed"
                )

            }


        except Exception as e:


            return {

                "status":
                f"Weather error {e}"

            }