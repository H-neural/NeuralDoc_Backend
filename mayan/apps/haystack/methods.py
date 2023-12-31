import logging
import requests
from io import BytesIO
import tempfile
from django.core.files import File

logger = logging.getLogger(name=__name__)

HAYSTACK_BASE_URL = "http://47.254.178.132:8000"


def text_to_file(text):
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
    temp_file.write(text)
    temp_file.seek(0)

    django_file = File(temp_file)

    django_file.name = 'uploaded-file.txt'

    return django_file


def method_send_ocr_to_elastic_db(content):
    logger.info("Sending OCR content to elastic search database")

    try:
        file_object = text_to_file(content)

        files = {'files': (file_object.name, file_object, 'text/plain')}
        headers = {'Accept': 'application/json', }
        data = {'meta': None}

        file_upload_url = HAYSTACK_BASE_URL + "/file-upload"
        response = requests.post(file_upload_url, headers=headers, data=data, files=files)

        response.raise_for_status()
        logger.info('Successfully uploaded file to Elasticsearch database')

        file_object.close()

    except requests.exceptions.RequestException as e:
        logger.error('Failed to upload file to Elasticsearch database: %s', e)
