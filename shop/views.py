from django.shortcuts import render,redirect
from shop.models import Categorys
from shop.forms import RegisterForm
from shop.forms import LoginForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.views import View

from shop.models import Products

from shop.forms import ProductForm, CategoryForm, StockForm


class Categories(View):
    def get(self, request):
        c=Categorys.objects.all()
        context={'categories':c}
        return render(request, 'category.html',context)

class products(View):
    def get(self,request,i):
        c=Categorys.objects.get(id=i)
        context={'category':c}
        return render(request, 'products.html',context)


from shop.models import Products
class productdetail(View):
    def get(self, request,i):
        p=Products.objects.get(id=i)
        context={'product':p}
        return render(request, 'productdetail.html',context)

class UserLoginView(View):
    def get(self, request):
        form_instance = LoginForm()
        context = {'form':form_instance}
        return render(request, 'login.html',context)
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            #authenticate(username,password)
            #authnticate() checks whether a user exists or not inside db
            #if user exists Django will add the requested user into current session
            # or else it will show invalid msg
            user=authenticate(username=u,password=p)

            if user:
                login(request,user)#adds the user into session
                u=request.user
                print(u)
                return redirect('Category')
            else:
                messages.error(request, "Login Unsuccessful. Please check username and password.")
                return redirect('shop:login')

class userregister(View):
    def post(self, request):
        form_instance =RegisterForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:login')


    def get(self, request):
        form_instance=RegisterForm()
        context = {'form':form_instance}
        return render(request, 'register.html',context)

class userlogout(View):
    def get(self, request):
        logout(request)
        return redirect('shop:login')
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
@method_decorator(login_required, name='dispatch')
class AddCategory(View):
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('Category')

    def get(self, request):
        form_instance=CategoryForm()
        context={'form':form_instance}
        return render(request, 'addcategory.html',context)

@method_decorator(login_required, name='dispatch')
class AddProduct(View):
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():

            form_instance.save()
            return redirect('Category')
    def get(self, request):
        form_instance=ProductForm()
        context={'form':form_instance}
        return render(request, 'addproduct.html',context)
@method_decorator(login_required, name='dispatch')
class AddStock(View):
    def post(self,request,i):
        p=Products.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)
        if form_instance.is_valid():

            form_instance.save()
            return redirect('Category')
    def get(self, request,i):
        p=Products.objects.get(id=i)
        form_instance=StockForm(instance=p)
        context={'form':form_instance}
        return render(request, 'addstock.html',context)
