import email
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
# Create your views here.


            ### đăng kí #####
def registerForm(request):
   return render(request,"register.html")

def registerMember(request):
    name = request.POST['name']
    sdt = request.POST['sdt']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username,email, password)
    user.save()
    customerr = customer.objects.create(user=user,name=name,phoneNumber=sdt)
    customerr.save()
    return render(request,'login.html',{"error":"register successfully","color":"green"})



##  đăng nhập ##
class loginn(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return HttpResponse("<h1><a  style='margin-left:45%;text-decoration:none' href='/admin'> vào trang admin</a></h1><h1><a  style='margin-left:45%;text-decoration:none' href='/login'> đăng xuất</a></h1>")
            else:
                return redirect('home')
        else:
            
            return render(request,'login.html',{"error":"invalid username or password","color":"red"})
        
 #############log out  ################# 

    
def logoutUser(request):
    logout(request)
    return redirect('home')



##############################Home######################### 
def homePage(request):
    123
    
    search=''
    if(request.GET.get('s') == 'Search'):
        search=request.GET.get('search')    
    book = Book.objects.filter(name__icontains=search).order_by('-id')
    p=Paginator(book,10)
    page = request.GET.get('page')
    book_list = p.get_page(page)
    if request.user.is_authenticated:
        customerr = request.user.customer           # lấy ra trường khách hàng trùng với người đăng nhập
        order,created = Cart.objects.get_or_create(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó
        
        items = order.orderitem_set.all() #get các item nằm trong cart
        
        context = {'nt': "logout",'b':True,'books':book,'user':customerr,'items':items,'order':order,'book_list':book_list}
    else :
        context = {'nt': "login",'b':False,'books':book,'book_list':book_list}
    
    
    return render(request,'store.html',context)




############################## giỏ hàng ##########
@login_required(login_url='/login/')
def cart(request):
    
    customerr = request.user.customer           # lấy ra trường khách hàng trùng với người đăng nhập
    order,created = Cart.objects.get_or_create(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó
    items = order.orderitem_set.all() #get các item nằm trong cart
    context = {'nt': "logout",'b':True,'user':customerr,'items':items,'order':order}
    return render(request,'cart.html',context)


def upItem(request,userId,bookId):
    user = customer.objects.get(id=int(userId))
    order = Cart.objects.get(customer=user,complete=False)
    book = Book.objects.get(id=int(bookId))
    item,created = OrderItem.objects.get_or_create(product=book,order=order)
    item.quantity = item.quantity+1
    item.save()
    return redirect('cart')


def downItem(request,userId,bookId):
    user = customer.objects.get(id=int(userId))
    order = Cart.objects.get(customer=user,complete=False)
    book = Book.objects.get(id=int(bookId))
    item,created = OrderItem.objects.get_or_create(product=book,order=order)
    item.quantity = item.quantity-1
    
    item.save()
    if(item.quantity==0):
        item.delete()
    return redirect('cart')


@login_required(login_url='/login/')
def UpdateItemCart(request,userId,bookId):
    user = customer.objects.get(id=int(userId))
    order = Cart.objects.get(customer=user,complete=False)
    book = Book.objects.get(id=int(bookId))
    item,created = OrderItem.objects.get_or_create(product=book,order=order)
    item.quantity = item.quantity+1
    item.save()
    return redirect('home')
############################## checkOut ###############

@login_required(login_url='/login/')
def checkout(request):
    customerr = request.user.customer
    order,created = Cart.objects.get_or_create(customer=customerr,complete=False)
    n = order.get_cart_items
    bool = True
    if(n==0):
        bool=False
    items = order.orderitem_set.all()
    context = {'nt': "logout",'b':True,'user':customerr,'items':items,'order':order,'bool':bool}
    return render(request,'checkout.html',context)


  
def ordered(request,userId):
    
    address = request.POST['address']
    city = request.POST['city']
    user = customer.objects.get(id=int(userId))
    order = Cart.objects.get(customer=user,complete=False)
    
    order.address=address
    order.city = city
    order.complete=True
    order.save()
    return redirect('home')




########## LICH SỬ ĐƠN HÀNG ###################
@login_required(login_url='/login/')
def history(request):
    customerr = request.user.customer
    order = Cart.objects.get(customer=customerr,complete=False)
    orders = Cart.objects.filter(customer=customerr,complete=True).order_by('-id')

    context = {'nt': "logout",'b':True,'user':customerr,'orders':orders,'order':order}
    return render(request,'history.html',context)


@login_required(login_url='/login/')
def detail(request,orderID):
    customerr = request.user.customer           # lấy ra trường khách hàng trùng với người đăng nhập
    order1 = Cart.objects.get(customer=customerr,complete=False)
    
    order = Cart.objects.get(pk=orderID) #trả về or tạo mới 1 cart của khách hàng đó
    items = order.orderitem_set.all() #get các item nằm trong cart
    context = {'nt': "logout",'b':True,'user':customerr,'items':items,'orderr':order,'order':order1}

    return render(request,'historydetail.html',context)




####### PROFILE ###############
@login_required(login_url='/login/')
def profile(request):
    customerr = request.user.customer
    order= Cart.objects.get(customer=customerr,complete=False)
    context = {'nt': "logout",'b':True,'user':customerr,'order':order}
    return render(request,'profile.html',context)

@login_required(login_url='/login/')
def UpdateProfileForm(request):
    customerr = request.user.customer
    order = Cart.objects.get(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó
    context = {'nt': "logout",'b':True,'user':customerr,'order':order}
    return render(request,'updateprofile.html',context)

def UpdateProfile(request):
    name = request.POST['name']
    sdt = request.POST['sdt']
    customerr = request.user.customer
    customerr.name=name
    customerr.phoneNumber=sdt
    customerr.save()
    return redirect('profile')

def changepassForm(request):
    customerr = request.user.customer
    order = Cart.objects.get(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó  
    context = {'nt': "logout",'b':True,'user':customerr,'order':order}
    return render(request,'changepass.html',context)

def changePass(request):
    customerr = request.user.customer
    order = Cart.objects.get(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó  
    context = {'nt': "logout",'b':True,'user':customerr,'order':order,'error':"đổi mật khẩu thất bại"}
    user = request.user
    oldP = request.POST['old']
    newP = request.POST['new']
    confirm = request.POST['confirm']
    if(check_password(oldP,user.password)):
        if(confirm==newP):
            user.set_password(newP)
            user.save()
            login(request,user)
            return redirect('profile')
        else:
            return render(request,'changepass.html',context)
    else:
       return render(request,'changepass.html',context)
        


def detailProduct(request,bookID):
    book = Book.objects.get(id=int(bookID))
    cmt  = book.comment_set.all()
    if request.user.is_authenticated:
        customerr = request.user.customer
        order = Cart.objects.get(customer=customerr,complete=False) #trả về or tạo mới 1 cart của khách hàng đó  
        
        context = {'nt': "logout",'b':True,'user':customerr,'order':order,'book':book,'comments':cmt}
    else:
        context = {'nt': "login",'b':False,'book':book,'comments':cmt}
        
    return render(request,'detailProduct.html',context)

def feedbackForm(request,bookID):
    book = Book.objects.get(id=int(bookID))
    customerr = request.user.customer
    order = Cart.objects.get(customer=customerr,complete=False)    
    context = {'nt': "logout",'b':True,'user':customerr,'order':order,'book':book}
    return render(request,'feedback.html',context)

def feedback(request,bookID):
    customerr = request.user.customer
    
    bookk = Book.objects.get(id=int(bookID))
   
    cmt = request.POST['cmt']
    comment.objects.create(customer=customerr,book=bookk,review=cmt)
    
    
    return redirect('home')