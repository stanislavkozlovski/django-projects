from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, 'home.html')


def view_list(request: HttpRequest, list_id: str):
    list_: List = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list': list_})


def new_list(request: HttpRequest):
    """ Creates a new TODO list with the new item """
    new_item_text = request.POST['item_text']
    new_list_ = List.objects.create()
    Item.objects.create(text=new_item_text, list=new_list_)

    return redirect(f'/lists/{new_list_.id}')


def add_item(request: HttpRequest, list_id: str):
    """ Creates and adds a new item to an existing TODO list """
    new_item_text = request.POST['item_text']
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=new_item_text, list=list_)
    return redirect(f'/lists/{list_.id}')


