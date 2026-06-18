from django.shortcuts import render,redirect

from django.views import View

from cart.models import Cart
from shop.models import Products
import razorpay

from cart.models import Order
from cart.models import Order_items
from django.contrib.auth.decorators import login_required


class AddtoCart(View):
    def get(self,request,i):
        u=request.user  # logged in user
        p=Products.objects.get(id=i)  #product selected by user

        try:
            c=Cart.objects.get(user=u,products=p)  #checks whether the products is already added
                                        # to cart table

            c.quantity+=1
            c.save()

        except:
             c=Cart.objects.create(user=u,products=p,quantity=1)
             c.save()
        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        c=Cart.objects.all()
        total=0
        for i in c:
            total=total+i.subtotal()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

class Cartdecrement(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
        else:
            c.delete()

        return redirect('cart:cartview')

class Cartremove(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)

        c.delete()
        return redirect('cart:cartview')
import uuid
from cart.forms import Checkoutform
@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def post(self,request):
        form_instance=Checkoutform(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c=Cart.objects.get(user=u)
            total=0
            for i in c:
                total=total+i.subtotal()
            o.amount=total
            o.save()

            if(o.payment_method=='ONLINE'):
                #razorpay client connection
                client=razorpay.Client(auth=('rzp_test_T1okqbUjYaJXvX','wgZU8a2JVTVqwcrfzkZmGI6Q'))
                print(client)
                #create an order using client
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)

                o.order_id=response_payment['order_id']
                o.save()

                context = {'payment': response_payment}
                return redirect('payment.html', context)

            else:
                id='ord_cod'+uuid.uuid4().hex[:14]
                o.order_id=id
                o.is_ordered = True
                o.save()

                c = Cart.objects.get(user=request.user)
                for i in c:
                    item = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                    item.save()
                    item.produts.stock = item.quantity
                    item.products.save()
                c.delete()
                return render(request, 'payment.html')



    def get(self,request):
        form_instance=Checkoutform()
        context={'form':form_instance}
        return render(request,'checkout.html',context)

class Payment(View):
    def get(self,request):
        return render(request,'payment.html')
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt,name='dispatch')
@method_decorator(login_required, name='dispatch')
class PaymentSuccess(View):
    def post(self,request):
        print(request.POST)
        id=request.POST.get('razorpay_order_id')
        o=Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()
        c=Cart.objects.get(user=request.user)
        for i in c:
            item=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
            item.save()
            item.produts.stock=item.quantity
            item.products.save()
        c.delete()
        return render(request,'paymentsuccess.html')

class ordersummary(View):
    def get(self,request):
        o=Order.objects.filter(user=request.user,is_ordered=True)
        context={'order':o}
        return render(request,'ordersummary.html',context)


