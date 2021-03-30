import csv
from django.core.files.temp import NamedTemporaryFile

# TODO: Upload file to s3 instead of using tmp directory
# TODO: Make it async and use worker
def generate_bhav_copy_csv(q: str, results: list, file_path: str = None) -> str:
    keys = results[0].keys()
    if not file_path:
        file_path = f"/tmp/bhav_copy_{q}.csv"
    with open(file_path, "w") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    return file_path