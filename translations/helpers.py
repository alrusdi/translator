from translations.models import Source, Translation, Suggestion, Language


def get_translation_sources_info():
    sources = Source.objects.prefetch_related("translation_set").order_by("value")
    ret = []
    for src in sources:
        new_item = {
            "id": src.id,
            "value": src.value,
            "translations": []
        }

        for trans in src.translation_set.all():
            new_item["translations"].append({
                "lang": trans.language.code,
                "value": trans.value
            })

        ret.append(new_item)
    return ret


def save_translation_suggestion(data, user):
    lang = Language.objects.get(code=data["lang"])
    new_value = data["value"].strip()
    trans, created = Translation.objects.get_or_create(
        source_id=data["source_id"],
        language=lang,
    )
    if user.is_staff:
        trans.value = new_value
        trans.save(update_fields=["value"])
        return

    sug, created = Suggestion.objects.get_or_create(
        target=trans,
        author=user
    )

    sug.value = new_value
    sug.save(update_fields=["value"])
