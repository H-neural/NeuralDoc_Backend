from django.utils.translation import ugettext_lazy as _

from .events import event_file_metadata_document_file_submitted
from .tasks import task_process_document_file


def method_document_file_metadata_submit(self, user=None):
    latest_file = self.file_latest
    # Don't error out if document has no file.
    if latest_file:
        latest_file.submit_for_file_metadata_processing(user=user)


def method_document_file_metadata_submit_single(self, user=None):
    event_file_metadata_document_file_submitted.commit(
        action_object=self.document, actor=user, target=self
    )

    if user:
        user_id = user.pk
    else:
        user_id = None

    task_process_document_file.apply_async(
        kwargs={
            'document_file_id': self.pk, 'user_id': user_id
        }
    )


def method_get_document_file_file_metadata(self, dotted_name):
    parts = dotted_name.split('__', 1)

    if len(parts) < 2:
        return

    driver_internal_name = parts[0]
    key = parts[1].replace('.', '_')

    try:
        document_driver = self.file_metadata_drivers.get(
            driver__internal_name=driver_internal_name
        )
    except self.file_metadata_drivers.model.DoesNotExist:
        return
    else:
        try:
            return document_driver.entries.get(key=key).value
        except document_driver.entries.model.DoesNotExist:
            return


method_get_document_file_file_metadata.help_text = _(
    'Return the specified document file file metadata entry.'
)
