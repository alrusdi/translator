from django.db import models


class Source(models.Model):
    value = models.TextField(
        unique=True,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Language(models.Model):
    code = models.CharField(
        max_length=6,
        unique=True,
        db_index=True
    )

    title = models.CharField(
        max_length=255,
        unique=True
    )


class Translation(models.Model):
    author = models.ForeignKey(
        "auth.User",
        null=True,
        on_delete=models.SET_NULL
    )
    language = models.ForeignKey(
        to=Language,
        on_delete=models.PROTECT
    )
    source = models.ForeignKey(
        to=Source,
        on_delete=models.PROTECT
    )
    value = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("source", "language", "value",)


class Suggestion(models.Model):
    author = models.ForeignKey(
        "auth.User",
        null=True,
        on_delete=models.SET_NULL
    )
    target = models.ForeignKey(
        to=Translation,
        on_delete=models.CASCADE
    )
    value = models.TextField(default="TBD")
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("target", "author")
