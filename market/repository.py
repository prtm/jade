from datetime import datetime
import requests
from requests.models import Response
from jade.utils import scraper_headers
from django.utils import timezone


class MarketRepository:
    """
    Repository for market interaction
    """

    def __init__(self) -> None:
        self.base_equity_url = "https://www.bseindia.com/download/BhavCopy/Equity/"

    def is_file_downloadable(self, url):
        response = requests.head(url, headers=scraper_headers.browser_headers)
        return (
            response.status_code == 200
            and response.headers["content-type"] == "application/x-zip-compressed"
        )

    def get_bhav_zip_url_from_datetime(self, dt: datetime) -> str:
        day = str(dt.day).zfill(2)
        month = dt.strftime("%m")
        year = dt.strftime("%y")
        return f"{self.base_equity_url}EQ{day}{month}{year}_CSV.ZIP"

    def get_bhav_copy(self, dt: datetime) -> Response:
        return requests.get(
            self.get_bhav_zip_url_from_datetime(dt),
            headers=scraper_headers.browser_headers,
        )

    def get_latest_bhav_copy(self) -> Response:
        return self.get_bhav_copy(timezone.now())
