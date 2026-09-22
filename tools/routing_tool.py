"""
Routing Tool

Uses OSRM (Open Source Routing Machine).



Used by:
- Itinerary Agent

Purpose:
- Estimate distance
- Estimate travel time
- Help group nearby activities
"""


import requests

from config.settings import Settings



class RoutingTool:


    def __init__(self):

        self.base_url = Settings.OSRM_BASE_URL



    def calculate_route(
        self,
        start_lat,
        start_lon,
        end_lat,
        end_lon
    ):


        try:


            url = (
                f"{self.base_url}/route/v1/driving/"
                f"{start_lon},{start_lat};"
                f"{end_lon},{end_lat}"
            )


            response = requests.get(

                url,

                params={
                    "overview":"false"
                },

                timeout=20

            )


            data=response.json()


            route=data.get(
                "routes",
                []
            )


            if route:

                return {

                    "distance_km":
                    round(
                        route[0]["distance"]/1000,
                        2
                    ),


                    "duration_minutes":
                    round(
                        route[0]["duration"]/60,
                        2
                    )

                }



        except Exception as e:


            print(
                f"Routing error: {e}"
            )


        return {

            "distance_km":
            "unknown",

            "duration_minutes":
            "unknown"

        }



    def calculate_routes(
        self,
        activities
    ):


        """
        Creates route summary.

        If coordinates exist,
        OSRM calculates travel time.

        Otherwise fallback is returned.
        """


        routes=[]


        for index in range(
            len(activities)-1
        ):


            first=activities[index]

            second=activities[index+1]


            if (
                "latitude" in first
                and
                "latitude" in second
            ):


                result=self.calculate_route(

                    first["latitude"],

                    first["longitude"],

                    second["latitude"],

                    second["longitude"]

                )


            else:


                result={

                    "distance_km":
                    "estimated nearby",

                    "duration_minutes":
                    "estimated transfer"

                }


            routes.append({

                "from":
                first.get(
                    "name"
                ),

                "to":
                second.get(
                    "name"
                ),

                **result

            })



        return routes