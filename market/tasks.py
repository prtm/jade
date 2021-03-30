import os
from datetime import datetime

import pytz
from celery import shared_task
from django.utils import timezone

from market.utils.generate_bhav_csv import generate_bhav_copy_csv

from .repository import MarketRepository
from .utils import unzip
from .utils.bhav_helper import BhavHelper


@shared_task
def update_bhav_data(provided_dt_utc: datetime = None) -> bool:
    """[Fetch data on specific date if given else today date will be used and redis will be updated]

    Args:
        provided_dt_utc (datetime): [date specific data will be extracted]

    Returns:
        bool: [Represents is data loaded]
    """
    dt_utc = provided_dt_utc if provided_dt_utc else timezone.datetime.now()  # utc
    dt = dt_utc.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("Asia/Calcutta")
    )  # ist
    market_repository = MarketRepository()
    bhav_helper = BhavHelper()
    url = market_repository.get_bhav_zip_url_from_datetime(dt)
    if market_repository.is_file_downloadable(url):
        response = market_repository.get_bhav_copy(dt)
        filepath = unzip.unzip_file(response.content)
        bhav_helper.load_bhav_data_csv(filepath=filepath)
        os.remove(filepath)
        # TODO: Should rename file to date specific csv and handle logic
        generate_bhav_copy_csv(
            q="",
            results=bhav_helper.get_bhav_data(start=0, stop=-1),
            file_path=os.path.join(os.getcwd(), "latest_bhav.csv"),
        )

        print("redis data loaded")
        return True
    print(f"data load failed for {dt}")
    return False
