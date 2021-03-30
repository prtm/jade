import csv

# TODO: Upload file to s3 instead of using tmp directory
# TODO: Make it async and use worker
def generate_bhav_copy_csv(query: str, results: list) -> str:
    keys = results[0].keys()
    file_path = f"/tmp/bhav_copy_{query}.csv"
    with open(file_path, "w") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    return file_path