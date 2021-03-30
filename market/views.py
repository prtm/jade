import os

from django.conf import settings
from django.http import HttpResponse
from django.http.response import Http404

from .utils.generate_bhav_csv import generate_bhav_copy_csv
from .utils.bhav_helper import BhavHelper


def download_bhav_csv(request):
    bhav_helper = BhavHelper()
    q = request.GET.get("q", "").upper()
    delete_file = False
    if q and len(q) >= 2:
        results = bhav_helper.get_bhav_data_by_prefix(q, max_count=-1)
        file_path = generate_bhav_copy_csv(q, results)
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        delete_file = True
    else:
        file_path = os.path.join(os.getcwd(), "latest_bhav.csv")

    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            # TODO: Can cause memory
            csv_content = fh.read()
            if delete_file:
                # TODO: Can reuse this file
                os.remove(file_path)
            response = HttpResponse(
                csv_content, content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    raise Http404
