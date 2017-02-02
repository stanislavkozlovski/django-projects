from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from lists.models import Item


def home_page(request: HttpRequest):
    new_item_text = request.POST.get('item_text', '')
    if request.method == 'POST':
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request, 'home.html',
                  {'items': Item.objects.all()})
