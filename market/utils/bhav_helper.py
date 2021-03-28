import csv
import json

from django.utils import timezone
from django_redis import get_redis_connection
from jade.utils.utils import parse_str_to_int


class BhavHelper:
    def __init__(self) -> None:
        self.redis = get_redis_connection("default")
        self.first_10_items = "first_10_items"
        self.last_updated = "last_updated"
        self.total_items_count = "total_items_count"
        self.sc_name_sorted_set = "sc_name_sorted_set"

    def load_bhav_data_csv(self, filepath: str) -> None:
        """[load data from bhav csv to redis]

        Args:
            filepath (str): [csv file path]
        """
        # create redis pipeline
        pipeline = self.redis.pipeline(transaction=True)
        pipeline.flushdb()
        first_10_items_list = []
        first_10_items_counter = 0
        total_items_counter = 0
        with open(filepath, "r") as csv_file:
            csv_dict_reader = csv.DictReader(csv_file)
            for row in csv_dict_reader:
                prefixed_sc_name = f'BHAV:{row["SC_NAME"].strip()}'
                data = {
                    "SC_CODE": row["SC_CODE"],
                    "OPEN": row["OPEN"],
                    "CLOSE": row["CLOSE"],
                    "HIGH": row["HIGH"],
                    "LOW": row["LOW"],
                }
                data_with_name = dict(data)
                data_with_name.update(
                    {
                        "SC_NAME": row["SC_NAME"].strip(),
                    }
                )
                if first_10_items_counter < 10:
                    first_10_items_list.append(data_with_name)
                    first_10_items_counter += 1

                pipeline.set(prefixed_sc_name, json.dumps(data))
                pipeline.zadd(
                    self.sc_name_sorted_set,
                    {json.dumps(data_with_name): total_items_counter},
                )
                total_items_counter += 1
            pipeline.set(self.first_10_items, json.dumps(first_10_items_list))
            pipeline.set(self.last_updated, str(timezone.now().date()))
            pipeline.set(self.total_items_count, total_items_counter)

        # Execute
        pipeline.execute()
        return

    def get_last_updated_time(self) -> str:
        return self.redis.get(self.last_updated)

    def get_bhav_data(self, start=0, stop=9) -> list:
        result_list = self.redis.zrangebyscore(
            self.sc_name_sorted_set, min=start, max=stop
        )

        return [json.loads(r) for r in result_list]

    def get_first_10_items(self) -> list:
        results = self.redis.get(self.first_10_items)
        if results:
            return json.loads(results)

    def get_bhav_data_count(self) -> int:
        return parse_str_to_int(self.redis.get(self.total_items_count), 0)

    def search_bhav_data_by_name_suggestions(self, q: str) -> list:
        result_list = self.redis.keys(f"BHAV:{q}*")

        return [key.split(":")[1] for key in result_list]

    def search_bhav_data_by_name(self, name: str) -> list:
        result_str = self.redis.get(f"BHAV:{name}")
        if result_str:
            result = json.loads(result_str)
            result["SC_NAME"] = name
            return result
