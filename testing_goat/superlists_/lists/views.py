from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List


# /
def home_page(request: HttpRequest):
    return render(request, 'home.html')


# @lists/{list_id}
def view_list(request: HttpRequest, list_id: str):
    error_msg = None
    if request.method == 'POST':
        """ Creates and adds a new item to an existing TODO list """
        new_item_text = request.POST['item_text']
        list_ = List.objects.get(id=list_id)
        item = Item.objects.create(text=new_item_text, list=list_)

        try:
            item.full_clean()
            item.save()

            return redirect(list_)  # :O
        except ValidationError as e:
            item.delete()
            error_msg = "You can't have an empty list item!"

    list_: List = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_, 'error': error_msg})


# @lists/new
def new_list(request: HttpRequest):
    """ Creates a new TODO list with the new item """
    new_item_text = request.POST['item_text']
    new_list_ = List.objects.create()
    item = Item.objects.create(text=new_item_text, list=new_list_)

    try:
        item.full_clean()
        item.save()
    except ValidationError as e:
        new_list_.delete()
        return render(request, 'home.html', {'error': "You can't have an empty list item!" })

    return redirect(new_list_)



