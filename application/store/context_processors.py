from .models import *

def categories_processor(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return {'categories': categories}
