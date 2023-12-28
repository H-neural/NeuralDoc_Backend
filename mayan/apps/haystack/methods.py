import logging
import requests
from io import BytesIO

logger = logging.getLogger(name=__name__)

HAYSTACK_BASE_URL = "http://47.254.178.132:8000"


def method_send_ocr_to_elastic_db(content):
    logger.info("Sending OCR content to elastic search database")

    try:
        with BytesIO(content.encode('utf-8')) as file_like_object:
            file_like_object.name = 'uploaded-file.txt'

            files = {'files': file_like_object}
            headers = {'Accept': 'application/json', }
            data = {'meta': None}

            file_upload_url = HAYSTACK_BASE_URL + "/file-upload"
            response = requests.post(file_upload_url, headers=headers, data=data, files=files)

            response.raise_for_status()

            logger.info('Successfully uploaded file to Elasticsearch database')
    except requests.exceptions.RequestException as e:
        logger.error('Failed to upload file to Elasticsearch database: %s', e)
