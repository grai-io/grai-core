import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'the_guide.settings'
django.setup()
import lineage.serializers as s

print(repr(s.EdgeSerializer()))
