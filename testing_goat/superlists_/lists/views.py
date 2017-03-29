from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List
from accounts.models import User
from lists.constants import EMPTY_LIST_ERROR_MSG
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

# /
def home_page(request: HttpRequest):
    return render(request, 'home.html', {'form': ItemForm()})


# @lists/{list_id}
def view_list(request: HttpRequest, list_id: str):
    error_msg = None
    if request.method == 'POST':
        """ Creates and adds a new item to an existing TODO list """
        list_ = List.objects.get(id=list_id)  # TODO: Validation
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()

            return redirect(list_)  # :O
        else:
            return render(request, 'list.html', {'list': list_, 'form': form})

    list_: List = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_, 'form': ExistingListItemForm(for_list=list_)})


# @lists/new
# def new_list(request: HttpRequest):
#     """ Creates a new TODO list with the new item """
#     form = ItemForm(data=request.POST)
#     if form.is_valid():
#         list_ = List()
#         if request.user.is_authenticated:
#             list_.owner = request.user
#         list_.save()
#         form.save(for_list=list_)
#         return redirect(list_)
#     else:
#         return render(request, 'home.html', {'form': form})


def new_list(request: HttpRequest):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)

    return render(request, 'home.html', {'form': form})

# @lists/user/my_lists
def my_lists(request: HttpRequest, user_email: str):
    """ Shows the User all of his lists"""
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return redirect('/')
    return render(request, 'my_lists.html', {'owner': user})
