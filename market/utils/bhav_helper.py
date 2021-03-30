import csv
import json

from django.utils import timezone
from django_redis import get_redis_connection
from jade.utils.utils import parse_str_to_int


class BhavHelper:
    def __init__(self) -> None:
        self.redis = get_redis_connection("default")
        self.first_n_items = "first_n_items"
        self.last_updated = "last_updated"
        self.total_items_count = "total_items_count"
        self.sc_name_sorted_set = "sc_name_sorted_set"
        self.sc_name_hash_stored = "sc_name_hash_stored"

    def load_bhav_data_csv(self, filepath: str) -> None:
        """[load data from bhav csv to redis]

        Args:
            filepath (str): [csv file path]
        """
        # create redis pipeline
        pipeline = self.redis.pipeline(transaction=True)
        pipeline.flushdb()
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

                pipeline.hset(
                    name=self.sc_name_hash_stored,
                    key=prefixed_sc_name,
                    value=json.dumps(data),
                )
                pipeline.zadd(
                    self.sc_name_sorted_set,
                    {prefixed_sc_name: 0},
                )
                total_items_counter += 1
            pipeline.set(self.last_updated, str(timezone.now().date()))
            pipeline.set(self.total_items_count, total_items_counter)

        # Execute
        pipeline.execute()
        return

    def get_last_updated_time(self) -> str:
        return self.redis.get(self.last_updated)

    def get_bhav_data(self, start=0, stop=14) -> list:
        name_keys = self.redis.zrange(
            name=self.sc_name_sorted_set,
            start=start,
            end=stop,
        )
        results = []

        for name_key in name_keys:
            data = json.loads(self.redis.hget(self.sc_name_hash_stored, name_key))
            data["SC_NAME"] = name_key.split(":")[1]
            results.append(data)
        return results

    def get_first_n_items(self) -> list:
        results = self.redis.get(self.first_n_items)
        if results:
            return json.loads(results)
        else:
            results = self.get_bhav_data(start=0, stop=14)
            self.redis.set(self.first_n_items, json.dumps(results))
            return results

    def get_bhav_data_count(self) -> int:
        return parse_str_to_int(self.redis.get(self.total_items_count), 0)

    def get_name_suggestions(self, q: str, max_count: int = 10) -> list:
        name_keys = self.redis.zscan_iter(
            name=self.sc_name_sorted_set,
            match=f"BHAV:{q}*",
        )
        results = []
        for key, _ in name_keys:
            if max_count == 0:
                break
            results.append(key.split(":")[1])
            max_count -= 1
        return results

    def get_bhav_data_by_extact_name(self, name: str) -> list:
        result_json = self.redis.hget(self.sc_name_hash_stored, f"BHAV:{name}")
        if result_json:
            result = json.loads(result_json)
            result["SC_NAME"] = name.split(":")[1]
            return result

    def get_bhav_data_by_prefix(self, q: str, max_count=14) -> list:
        name_keys = self.redis.zscan_iter(
            name=self.sc_name_sorted_set,
            match=f"BHAV:{q}*",
        )
        results = []
        for name_key, _ in name_keys:
            if max_count == 0:
                break
            data = json.loads(self.redis.hget(self.sc_name_hash_stored, name_key))
            data["SC_NAME"] = name_key.split(":")[1]
            results.append(data)
            max_count -= 1
        return results
