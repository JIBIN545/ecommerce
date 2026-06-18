from django.shortcuts import render

from django.views import View
from shop.models import Products
from django.db.models import Q
class SearchView(View):
    def get(self, request):
        # print(request.GET)
        query = request.GET.get('q')
        # if query:
        #   print(query)

        p = Products.objects.filter(Q(name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(price__icontains=query) )

        context = {'products':p}

        return render(request, 'search.html', context)

