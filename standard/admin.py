from django.contrib import admin
from .models import Standard   # ✅ correct (Capital S)

admin.site.register(Standard)