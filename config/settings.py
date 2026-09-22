"""
Central configuration loader.

Single source of truth for:
- Groq LLM
- External APIs
- Application settings
- Agent/tool compatibility

Loads values from .env
"""


import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()



class Settings:


    # =====================================================
    # Groq LLM
    # =====================================================

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_BASE_URL = os.getenv(
        "GROQ_BASE_URL",
        "https://api.groq.com/openai/v1"
    )

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )



    # =====================================================
    # Web Search
    # =====================================================

    # Tavily optional.
    # Current project uses curated destination knowledge.

    TAVILY_API_KEY = os.getenv(
        "TAVILY_API_KEY",
        ""
    )



    # =====================================================
    # OpenStreetMap
    # =====================================================

    OSM_OVERPASS_URL = os.getenv(
        "OSM_OVERPASS_URL",
        "https://overpass-api.de/api/interpreter"
    )


    OSM_NOMINATIM_URL = os.getenv(
        "OSM_NOMINATIM_URL",
        "https://nominatim.openstreetmap.org"
    )



    # =====================================================
    # Routing
    # =====================================================

    OSRM_BASE_URL = os.getenv(
        "OSRM_BASE_URL",
        "https://router.project-osrm.org"
    )



    # =====================================================
    # Weather
    # =====================================================

    WEATHER_API_URL = os.getenv(
        "WEATHER_API_URL",
        "https://api.open-meteo.com/v1/forecast"
    )


    GEOCODING_API_URL = os.getenv(
        "GEOCODING_API_URL",
        "https://geocoding-api.open-meteo.com/v1/search"
    )



    # =====================================================
    # Currency
    # =====================================================

    CURRENCY_API_URL = os.getenv(
        "CURRENCY_API_URL",
        "https://api.frankfurter.app"
    )



    # =====================================================
    # Application Controls
    # =====================================================

    MAX_REVISION_ATTEMPTS = int(
        os.getenv(
            "MAX_REVISION_ATTEMPTS",
            "4"
        )
    )


    REQUEST_TIMEOUT_SECONDS = int(
        os.getenv(
            "REQUEST_TIMEOUT_SECONDS",
            "30"
        )
    )


    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "WARNING"
    )



    # =====================================================
    # Compatibility Properties
    # Used by existing agents/services
    # =====================================================


    @property
    def groq_api_key(self):

        return self.GROQ_API_KEY



    @property
    def groq_base_url(self):

        return self.GROQ_BASE_URL



    @property
    def groq_model(self):

        return self.GROQ_MODEL



    @property
    def request_timeout_seconds(self):

        return self.REQUEST_TIMEOUT_SECONDS


    @property
    def max_revision_attempts(self):
        return self.MAX_REVISION_ATTEMPTS

    
    @property
    def has_llm(self):

        """
        Determines if Groq LLM is available.
        """

        return bool(
            self.GROQ_API_KEY
        )



    @property
    def tavily_api_key(self):

        return self.TAVILY_API_KEY



    @property
    def osrm_base_url(self):

        return self.OSRM_BASE_URL



    @property
    def weather_api_url(self):

        return self.WEATHER_API_URL



    @property
    def geocoding_api_url(self):

        return self.GEOCODING_API_URL



    @property
    def currency_api_url(self):

        return self.CURRENCY_API_URL




# =====================================================
# Shared settings instance
# =====================================================

_settings = Settings()



def get_settings():

    """
    Returns singleton Settings object.

    Used by:
    - LLMService
    - Agents
    - Tools
    """

    return _settings