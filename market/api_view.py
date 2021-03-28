from datetime import datetime
from typing import Any

from jade.utils.utils import parse_str_to_int
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .repository import MarketRepository
from .utils.bhav_helper import BhavHelper
from .utils import unzip

# Create your views here.


class MarketAPIView(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.market_repository = MarketRepository()
        self.bhav_helper = BhavHelper()

    def load_data(self, dt: datetime) -> bool:
        """[load data based on specific datetime]

        Args:
            dt (datetime): [date specific data will be extracted]

        Returns:
            bool: [Represents is data loaded]
        """
        dt = datetime(2021, 3, 25)
        url = self.market_repository.get_bhav_zip_url_from_datetime(dt)
        if self.market_repository.is_file_downloadable(url):
            response = self.market_repository.get_bhav_copy(dt)
            filepath = unzip.unzip_file(response.content)
            self.bhav_helper.load_bhav_data_csv(filepath=filepath)
            print("redis data loaded")
            return True
        print("data load failed for {dt}")
        return False

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Search by name
        """
        q = self.request.query_params.get("q", "").upper()
        if not q or len(q) < 3:
            return Response({"error": "query must contains aleast 3 letters"})
        results = self.bhav_helper.search_bhav_data_by_name(name=q)
        if not results:
            results = []
        return Response(
            {
                "results": results,
            }
        )

    @action(detail=False, methods=["get"], url_path="search-suggestions")
    def search_suggestions(self, request):
        """
        Search by name suggestions
        """
        q = self.request.query_params.get("q", "").upper()
        if not q or len(q) < 3:
            return Response({"error": "query must contains aleast 3 letters"})
        bhav_name_suggestions = self.bhav_helper.search_bhav_data_by_name_suggestions(
            q=q
        )
        return Response(
            {
                "results": bhav_name_suggestions,
            }
        )

    def list(self, request):
        """
        Get top 10 bhav items data
        """
        self.load_data()
        start = self.request.query_params.get("start")
        stop = self.request.query_params.get("stop")
        if not start and not stop:
            results = self.bhav_helper.get_first_10_items()
        else:
            start = parse_str_to_int(start, default=0)
            stop = parse_str_to_int(stop, default=9)
            results = self.bhav_helper.get_bhav_data(start=start, stop=stop)

        return Response(
            {
                self.bhav_helper.last_updated: self.bhav_helper.get_last_updated_time(),
                "count": self.bhav_helper.get_bhav_data_count(),
                "results": results,
            }
        )
