import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "the_guide.settings.dev"
django.setup()
import lineage.serializers as s

print(repr(s.EdgeSerializer()))
