"""
Signal handlers related to discussions.
"""
from django.dispatch import receiver
from opaque_keys.edx.locator import LibraryLocator

from django_comment_common import tasks
from xmodule.modulestore.django import SignalHandler


@receiver(SignalHandler.course_published)
def update_discussions_on_course_publish(sender, course_key, **kwargs):  # pylint: disable=unused-argument
    """
    Catches the signal that a course has been published in the module
    store and creates/updates the corresponding cache entry.
    Ignores publish signals from content libraries.
    """
    if isinstance(course_key, LibraryLocator):
        return

    context = {
        'course_id': unicode(course_key),
    }
    tasks.update_discussions_map.apply_async(
        args=[context],
        countdown=settings.DISCUSSION_SETTINGS['COURSE_PUBLISH_TASK_DELAY'],
    )
