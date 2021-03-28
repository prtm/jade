import pytz
from celery import shared_task
from django.utils import timezone

from .repository import MarketRepository
from .utils import unzip
from .utils.bhav_helper import BhavHelper


@shared_task
def update_bhav_data() -> bool:
    """[Fetch data on specific date and update redis]

    Args:
        dt (datetime): [date specific data will be extracted]

    Returns:
        bool: [Represents is data loaded]
    """
    dt_utc = timezone.datetime.now()  # utc
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
        print("redis data loaded")
        return True
    print("data load failed for {dt}")
    return False
