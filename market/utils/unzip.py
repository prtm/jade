import io
import os
import zipfile


def unzip_file(content: bytes) -> str:
    # Todo: extract in tmp directory with same file name every time
    z = zipfile.ZipFile(io.BytesIO(content))
    z.extractall('bhavcopy')
    csv_file_name = z.namelist()[0]
    return os.path.join(os.getcwd(), 'bhavcopy', csv_file_name)
