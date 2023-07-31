from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)
from mayan.apps.dynamic_search.search_models import SearchModel

from .permissions import permission_cabinet_view

# Cabinet

search_model_cabinet = SearchModel(
    app_label='cabinets', model_name='CabinetSearchResult',
    permission=permission_cabinet_view,
    serializer_path='mayan.apps.cabinets.serializers.CabinetSerializer'
)
search_model_cabinet.add_proxy_model(
    app_label='cabinets', model_name='Cabinet'
)

search_model_cabinet.add_model_field(field='label')

# Cabinet documents

search_model_cabinet.add_model_field(
    field='documents__document_type__label', label=_('Document type')
)
search_model_cabinet.add_model_field(
    field='documents__label', label=_('Document label')
)
search_model_cabinet.add_model_field(
    field='documents__description', label=_('Document description')
)
search_model_cabinet.add_model_field(
    field='documents__uuid', label=_('Document UUID')
)

# Cabinet documents files

search_model_cabinet.add_model_field(
    field='documents__files__checksum', label=_('Document file checksum')
)
search_model_cabinet.add_model_field(
    field='documents__files__mimetype', label=_('Document file MIME type')
)

# Document

search_model_document.add_model_field(
    field='cabinets__label', label=_('Cabinets')
)
