from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import gettext_lazy as _
from uuslug import slugify


class CustomTag(TagBase):

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        app_label = "taggit"

    def slugify(self, tag, i=None):
        slug = slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug


class TaggedWhatever(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
