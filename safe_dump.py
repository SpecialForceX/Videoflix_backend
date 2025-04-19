import os
import json
import django
from django.apps import apps
from django.core.serializers import serialize

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_hub.settings")
django.setup()

output_file = 'all_data.json'
all_data = []

for model in apps.get_models():
    try:
        queryset = model.objects.all()
        serialized = serialize('json', queryset)
        all_data.extend(json.loads(serialized))
    except Exception as e:
        print(f"⚠️ Fehler beim Serialisieren von {model.__name__}: {e}")

# 💡 Schreibe als latin-1, damit du keine Decode-Fehler bekommst:
with open(output_file, 'w', encoding='latin-1') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Daten erfolgreich exportiert nach: {output_file}")
