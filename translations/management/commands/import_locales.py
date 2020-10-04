import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from translations.models import Language, Source, Translation


class Command(BaseCommand):
    help = 'Initial dataimport command'

    def add_arguments(self, parser):
        parser.add_argument('locales_path', type=str)

    def process_locale(self, locale_name, path_to_locale):
        usr = User.objects.first()
        lang = Language.objects.filter(code=locale_name).first()
        count = 0
        for (dirpath, dirnames, filenames) in os.walk(path_to_locale):
            for f in filenames:
                if not f.endswith(".json"):
                    continue

                with open(os.path.join(path_to_locale, f)) as fp:
                    input_data = json.load(fp)

                for k, v in input_data.items():
                    if not k or not v:
                        continue

                    src = Source.objects.filter(value=k).first()
                    if not src:
                        # print("Value {} not found in source".format(k))
                        continue

                    try:
                        Translation.objects.create(
                            author=usr,
                            language=lang,
                            source=src,
                            value=v,
                        )
                        count += 1
                    except IntegrityError:
                        # print("Duplicate translation lang={}, source={} value={}".format(lang.code, src.value, v))
                        continue
        return count

    def handle(self, *args, **options):
        locales_path = options['locales_path']

        for (dirpath, dirnames, filenames) in os.walk(locales_path):
            for locale in dirnames:
                if len(locale) != 2:
                    print("Skip {}".format(locale))

                print("Processing {} locale...".format(locale))
                added = self.process_locale(locale, os.path.join(locales_path, locale))
                print("Added {} new records".format(added))
