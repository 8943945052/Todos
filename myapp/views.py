from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from myapp.forms import TodoForm,RegistrationForm,LoginForm

from django.contrib.auth import authenticate,login,logout

from myapp.models import Todo

from django.contrib import messages

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator

@method_decorator(signin_required,name='dispatch')
class TodoCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TodoForm(user=request.user)

        return render(request,'todo_add.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=TodoForm(request.POST,user=request.user)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Todo.objects.create(**data,owner=request.user)

            # form_instance.save()

            return redirect('todo-all')
        
        return render(request,'todo_add.html',{'form':'form_instance'})


@method_decorator(signin_required,name='dispatch')

class TodoListView(View):

    def get(self,request,*args,**kwargs):

        qs=Todo.objects.filter(owner=request.user)

        return render(request,'todo_list.html',{'todos':qs})

@method_decorator(signin_required,name='dispatch')
class TodoUpdateView(View):

    def get(self,request,*args,**kwargs):


        id=kwargs.get('pk')

        todo_object=Todo.objects.get(id=id)

        form_instance=TodoForm(instance=todo_object,user=request.user)

        return render(request,'todo_edit.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        todo_obj=Todo.objects.get(id=id)

        form_instance=TodoForm(request.POST,instance=todo_obj,user=request.user)

        if form_instance.is_valid():

            form_instance.save()

            # data=form_instance.cleaned_data

            # Todo.objects.filter(id=id).update()

            return redirect('todo-all')
        
        return render(request,'todo_edit.html',{'form':form_instance})

@method_decorator(signin_required,name='dispatch')
class TodoDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')
        
        Todo.objects.get(id=id).delete()

        return redirect('todo-all')



class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,'registration.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print('account is created successfully')

            messages.success(request,'account is created successfully')

            return redirect('signin')
        else:

            print('failed to create')

            messages.error(request,'failed to create account')

            return render(request,'registration.html',{'form':form_instance})


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,'login.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():
            
            data=form_instance.cleaned_data

            u_name=data.get('username')

            pwd=data.get('password')

            user_obj=authenticate(request,username=u_name,password=pwd)

            if user_obj:
                
                login(request,user_obj)

                print('login successfully')

                messages.success(request,'login successfully')

                return redirect('todo-home')
        
        print('login failed')

        messages.error(request,'login failed')

        return render(request,'login.html',{'form':form_instance})



class LogOutview(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')


# home page

class HomeView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'home.html')
