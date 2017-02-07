from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.constants import EMPTY_LIST_ERROR_MSG
from lists.forms import ItemForm


# /
def home_page(request: HttpRequest):
    return render(request, 'home.html', {'form': ItemForm()})


# @lists/{list_id}
def view_list(request: HttpRequest, list_id: str):
    error_msg = None
    if request.method == 'POST':
        """ Creates and adds a new item to an existing TODO list """
        form = ItemForm(data=request.POST)
        list_ = List.objects.get(id=list_id)  # TODO: Validation
        if form.is_valid():
            item = Item.objects.create(text=request.POST['text'], list=list_)

            return redirect(list_)  # :O
        else:
            return render(request, 'list.html', {'list': list_, 'form': form})

    list_: List = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_, 'error': error_msg, 'form': ItemForm()})


# @lists/new
def new_list(request: HttpRequest):
    """ Creates a new TODO list with the new item """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
