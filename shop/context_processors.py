from shop.models import Categorys

def menu_links(request):
    c=Categorys.objects.all()
    return {'links':c}