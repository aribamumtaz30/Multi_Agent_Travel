"""
Currency Conversion Tool

Uses Frankfurter API.

No API key required.

Example:
USD -> EUR
USD -> AED
USD -> PKR
"""


import requests

from config.settings import Settings



class CurrencyTool:


    def __init__(self):

        self.url = Settings.CURRENCY_API_URL



    def convert(
        self,
        amount,
        from_currency,
        to_currency
    ):


        try:


            response=requests.get(

                f"{self.url}/latest",

                params={

                    "amount":amount,

                    "from":
                    from_currency,

                    "to":
                    to_currency

                },

                timeout=20

            )


            data=response.json()


            return {

                "amount":
                amount,


                "from":
                from_currency,


                "to":
                to_currency,


                "converted":
                data.get(
                    "rates",
                    {}
                ).get(
                    to_currency
                )

            }


        except Exception as e:


            return {

                "error":
                str(e),

                "converted":
                None

            }