from datetime import date, datetime
from typing import Any

from django.utils import dateparse
from jade.utils.utils import parse_str_to_int
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import tasks
from .repository import MarketRepository
from .utils.bhav_helper import BhavHelper

# Create your views here.


class MarketAPIView(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.market_repository = MarketRepository()
        self.bhav_helper = BhavHelper()

    @action(detail=False, methods=["get"], url_path="search-by-extract-name")
    def search_by_extact_name(self, request):
        """
        get data by extract name
        """
        q = self.request.query_params.get("q", "").upper()
        if not q or len(q) < 2:
            return Response({"error": "query must contains aleast 2 letters"})
        results = self.bhav_helper.get_bhav_data_by_extact_name(name=q)
        if not results:
            results = []
        return Response(
            {
                "results": results,
            }
        )

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Search by name
        """
        q = self.request.query_params.get("q", "").upper()
        if not q or len(q) < 2:
            return Response({"error": "query must contains aleast 2 letters"})
        results = self.bhav_helper.get_bhav_data_by_prefix(q=q)
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
        get name suggestions
        """
        q = self.request.query_params.get("q", "").upper()
        if not q or len(q) < 2:
            return Response({"error": "query must contains aleast 2 letters"})
        bhav_name_suggestions = self.bhav_helper.get_name_suggestions(q=q)
        return Response(
            {
                "results": bhav_name_suggestions,
            }
        )

    @action(detail=False, methods=["post"], url_path="load-bhav-data")
    def load_bhav_data(self, request):
        """
        Manual update bhav data of specific date
        """
        date_str = self.request.data.get("date")
        try:
            parsed_date = dateparse.parse_date(date_str)
        except:
            return Response({"message": "enter valid date"})

        if not parsed_date:
            return Response({"message": "check date format"})

        return Response(
            {
                "success": tasks.update_bhav_data(
                    datetime.combine(parsed_date, datetime.min.time())
                ),
            }
        )

    def list(self, request):
        """
        Get fist n bhav items data
        """
        # tasks.update_bhav_data(datetime(2021, 3, 25))
        start = self.request.query_params.get("start")
        stop = self.request.query_params.get("stop")
        if not start and not stop:
            results = self.bhav_helper.get_first_n_items()
        else:
            start = parse_str_to_int(start, default=0)
            stop = parse_str_to_int(stop, default=14)
            results = self.bhav_helper.get_bhav_data(start=start, stop=stop)

        return Response(
            {
                self.bhav_helper.last_updated: self.bhav_helper.get_last_updated_time(),
                "count": self.bhav_helper.get_bhav_data_count(),
                "results": results,
            }
        )
