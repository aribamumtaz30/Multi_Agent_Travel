"""Curated destination knowledge tool.

This intentionally avoids pretending to be live web search. It gives agents compact,
reliable planning context while Open-Meteo provides the required external API/tool.
"""
from __future__ import annotations
from typing import Any

class DestinationKnowledgeTool:
    # Curated records keep core destination context compact and predictable for downstream agents.
    _DATA: dict[str, dict[str, Any]] = {
        "dubai": {
            "areas": ["Downtown Dubai", "Dubai Marina", "JBR", "Old Dubai", "Palm Jumeirah"],
            "attractions": ["Burj Khalifa", "Dubai Mall", "Museum of the Future", "Jumeirah Beach", "Dubai Marina", "Al Fahidi Historical Neighbourhood", "Desert Safari"],
            "transport": ["Dubai Metro", "RTA buses", "taxis", "Careem/Uber", "Dubai Tram"],
            "best_time": "November to March for milder outdoor weather.",
            "considerations": ["Dress respectfully in cultural/religious places", "Allow extra travel time at rush hour", "Book major attractions in advance"],
            "neighborhoods": ["Downtown for first-time sightseeing", "Marina/JBR for beach and nightlife", "Bur Dubai/Deira for heritage and value"],
            "surroundings": ["Abu Dhabi", "Sharjah", "Hatta", "Al Ain"]
        },
        "lahore": {
            "areas": ["Old Lahore", "Gulberg", "DHA", "Mall Road", "Johar Town"],
            "attractions": ["Lahore Fort", "Badshahi Mosque", "Walled City", "Shalimar Gardens", "Minar-e-Pakistan", "Lahore Museum", "Wagah Border"],
            "transport": ["Metrobus", "Orange Line Metro Train", "ride-hailing", "taxis/rickshaws"],
            "best_time": "October to March is generally more comfortable for sightseeing.",
            "considerations": ["Plan Old City sights together", "Carry cash for small vendors", "Check local opening days/times before departure"],
            "neighborhoods": ["Gulberg for central dining", "DHA for modern stays", "Mall Road for heritage access"],
            "surroundings": ["Wagah", "Sheikhupura", "Kasur", "Khewra Salt Mine"]
        },
        "islamabad": {
            "areas": ["F-6", "F-7", "Blue Area", "Saidpur", "Margalla Hills"],
            "attractions": ["Faisal Mosque", "Pakistan Monument", "Lok Virsa Museum", "Daman-e-Koh", "Trail 3", "Saidpur Village"],
            "transport": ["Metrobus", "ride-hailing", "taxis", "private car"],
            "best_time": "March-April and October-November are pleasant for outdoor plans.",
            "considerations": ["Hill trails need suitable footwear", "Keep weather flexibility for Margalla Hills", "Cluster Rawalpindi/Islamabad stops geographically"],
            "neighborhoods": ["F-6/F-7 for restaurants and central access", "Blue Area for business access"],
            "surroundings": ["Rawalpindi", "Taxila", "Murree", "Khanpur Dam", "Nathia Gali"]
        },
        "murree": {
            "areas": ["Mall Road", "Kashmir Point", "Pindi Point"],
            "attractions": ["Mall Road", "Kashmir Point", "Pindi Point chairlift", "Patriata/New Murree"],
            "transport": ["private car", "local taxis", "walking in central areas"],
            "best_time": "Spring and autumn for mild weather; winter for snow with road-condition checks.",
            "considerations": ["Traffic can be heavy on weekends", "Check road/weather conditions in winter", "Carry warm layers"],
            "neighborhoods": ["Mall Road for walkability", "Kashmir Point for quieter views"],
            "surroundings": ["Patriata", "Bhurban", "Nathia Gali", "Ayubia"]
        },
        "paris": {
            "areas": ["Le Marais", "Latin Quarter", "Saint-Germain", "Montmartre", "7th arrondissement"],
            "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame area", "Montmartre", "Seine River", "Musée d'Orsay"],
            "transport": ["Metro", "RER", "buses", "walking"],
            "best_time": "April-June and September-October balance weather and crowds.",
            "considerations": ["Reserve major museums", "Validate transit tickets", "Watch belongings in crowded tourist areas"],
            "neighborhoods": ["Le Marais for central atmosphere", "Latin Quarter for walkability", "7th for Eiffel Tower access"],
            "surroundings": ["Versailles", "Giverny", "Disneyland Paris", "Fontainebleau"]
        }
    }

    def lookup(self, destination: str) -> dict[str, Any]:
        key = destination.strip().lower()
        if key in self._DATA:
            return {"source": "curated_destination_knowledge", "destination": destination, **self._DATA[key]}
        # Generic fallback keeps the app usable for any destination; the LLM can enrich it.
        return {
            "source": "generic_destination_knowledge",
            "destination": destination,
            "areas": ["City centre", "historic district", "popular visitor district"],
            "attractions": [],
            "transport": ["public transport", "taxi/ride-hailing", "walking"],
            "best_time": "Check seasonal weather and local events for the selected dates.",
            "considerations": ["Verify opening hours", "Group nearby stops", "Keep contingency time"],
            "neighborhoods": ["Choose a central, well-connected area"],
            "surroundings": ["Ask the destination agent for nearby day-trip ideas"]
        }
