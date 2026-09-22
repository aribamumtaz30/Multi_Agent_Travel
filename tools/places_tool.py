"""
Places Tool

Uses OpenStreetMap Overpass API.


Provides:
- Hotel discovery
- Restaurant discovery
"""

import requests

from config.settings import Settings


class PlacesTool:


    def __init__(self):

        self.url = Settings.OSM_OVERPASS_URL



    def _execute_query(self, query):

        try:

            response = requests.post(
                self.url,
                data=query,
                timeout=30
            )

            response.raise_for_status()

            return response.json()


        except Exception as e:

            print(
                f"Places API failed: {e}"
            )

            return {
                "elements":[]
            }



    def search_hotels(
        self,
        destination
    ):


        query = f"""

        [out:json];

        area["name"="{destination}"]->.searchArea;

        (
          node["tourism"="hotel"]
          (area.searchArea);

          way["tourism"="hotel"]
          (area.searchArea);
        );

        out center;

        """


        data = self._execute_query(query)


        hotels=[]


        for item in data.get(
            "elements",
            []
        ):


            tags=item.get(
                "tags",
                {}
            )


            hotels.append({

                "hotel_name":
                    tags.get(
                        "name",
                        "Recommended Hotel"
                    ),

                "location":
                    destination,

                "estimated_price":
                    120,

                "rating":
                    "4-star estimate",

                "distance":
                    "Near major attractions",

                "why_recommended":
                    "Located through OpenStreetMap nearby search"

            })


        if not hotels:


            hotels.append({

                "hotel_name":
                    "Central City Hotel",

                "location":
                    destination,

                "estimated_price":
                    150,

                "rating":
                    "4-star estimate",

                "distance":
                    "City center",

                "why_recommended":
                    "Fallback recommendation"

            })


        return hotels




    def search_restaurants(
        self,
        destination
    ):


        query=f"""

        [out:json];

        area["name"="{destination}"]->.searchArea;

        (
        node["amenity"="restaurant"]
        (area.searchArea);

        way["amenity"="restaurant"]
        (area.searchArea);

        );

        out center;

        """


        data=self._execute_query(
            query
        )


        restaurants=[]


        for item in data.get(
            "elements",
            []
        ):


            tags=item.get(
                "tags",
                {}
            )


            restaurants.append({

                "name":
                    tags.get(
                        "name",
                        "Local Restaurant"
                    ),

                "location":
                    destination,

                "cuisine":
                    tags.get(
                        "cuisine",
                        "Local Cuisine"
                    ),

                "budget":
                    "Medium",

                "reason":
                    "Close to planned activities"

            })



        if not restaurants:


            restaurants.append({

                "name":
                    "Local Food Experience",

                "location":
                    destination,

                "cuisine":
                    "Local",

                "budget":
                    "Medium",

                "reason":
                    "Fallback recommendation"

            })


        return restaurants