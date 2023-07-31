import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from services.models import Service
from .models import CustomUser as User, UserProfile, Education
from .decorators import is_service_provider, superuser_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

@login_required
def home(request):
    all_services = Service.objects.all()
    paginator = Paginator(all_services, 4)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    context = {
        'services': services, 'user': request.user.username
    }
    return render(request, 'users/home.html', context)

@login_required
@is_service_provider
def dashboard(request, id):
    profile = UserProfile.objects.get(user__id=id)
    services = Service.objects.filter(user=profile)
    return render(request, 'users/dashboard.html', {'services': services})


def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'users/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ', Already Exists. Please Try Another Email')
            return render(request, 'users/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your Username, ' + username + ', Already Exists. Please Try Another Username')
            return render(request, 'users/signup.html')

        # validate password
        if password != password1:
            messages.error(request, "Your Passwords Don't match")
            return render(request, 'users/signup.html')
        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, username=username, password=password)
        user_group = Group.objects.get(name="Users")
        user.groups.add(user_group)
        messages.success(request, "User Registration Successful")
        context = {
            'email': email, 'first_name': first_name, 'last_name': last_name, 'username': username, "password": password, "password1": password1
        }
        return render(request, 'users/success.html', context)

    return render(request, 'users/signup.html')


# view for login
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'users/login.html')
        # email is valid but does not exist
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'This email, ' + email + ', Does Not Exist...')
            return render(request, 'users/login.html')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are logged in successfully")
                    if user.groups.filter(name='Customer').exists():
                        return redirect('/users/home/')
                    elif user.groups.filter(name='Service Provider').exists():
                        return redirect('/users/dashboard/'+str(user.id)+'/')
                    else:
                        return redirect('/users/user_profile/')
                else:
                    messages.error(request, "email or password incorrect")
            else:
                messages.error(request, f"User with email '{email}' does not exist")
    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out successfully")
    return HttpResponseRedirect('/users/login/')


# list all available groups
@login_required
@superuser_required
def group_list(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'users/groups/group_list.html', context)

@login_required
@superuser_required
def view_group_users(request, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        messages.error(request, f"The group '{group_name}' does not exist")
        return render(request, 'users/groups/group_users_list.html', {'users': []})

    users = group.user_set.all()
    context = {
        'users': users,
        'group_name': group_name
    }
    return render(request, 'users/groups/group_users_list.html', context)


@login_required
@superuser_required
def add_group(request):
    if request.method == 'POST':
        name = request.POST['group_name']
        group_name = name.title()
        request_group, created = Group.objects.get_or_create(name=group_name)
        messages.success(request, f'{group_name} Group Created Successfully')
        return HttpResponseRedirect('/users/groups/')
    return render(request, 'users/groups/new_group.html')

# add users to specific groups based on user status in user profiles. check the signup view


@login_required
@superuser_required
def add_user_to_group(user, group):
    try:
        user.groups.add(group)
        user.save()
        return True
    except:
        return False

@login_required
@csrf_exempt
def add_user_education(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            qualifications = data.get('qualifications')
            if not qualifications or not isinstance(qualifications, list):
                return JsonResponse({'status': 'error', 'message': 'Invalid qualifications data'})
            
            for qualification_data in qualifications:
                school = qualification_data.get('school')
                qualification = qualification_data.get('qualification')
                course = qualification_data.get('course')
                graduation_year = qualification_data.get('graduation_year')

                if not school or not qualification or not course or not graduation_year:
                    return JsonResponse({'status': 'error', 'message': 'Incomplete qualification data'})
                
                Education.objects.create(
                    user = request.user, school=school, qualification=qualification, course=course, graduation_year=graduation_year
                )
            return JsonResponse({'status': 'success', 'message': 'User Education Qualifications Saved Successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def create_user_profile(request):
    req_user = request.user
    groups = Group.objects.all()
    g = [group.name for group in groups if group.name != "Super Admin" and group.name != "Admin" and group.name != 'Users']
    if hasattr(req_user, 'userprofile'):
        return HttpResponseRedirect('/users/view_profile')
    else:
        #messages.info(request, 'Create Your Profile')
        if request.method == 'POST':
            i_am_a = request.POST['i_am_a']
            user = req_user
            bio = request.POST['bio'] 
            phone_number = request.POST['phone_number']
            gender = request.POST['gender']
            profile_pics = request.FILES['profile_pics']
            occupation = request.POST['occupation']
            address = request.POST['address']
            user_group = Group.objects.get(name=i_am_a)
            user = User.objects.get(id=request.user.id)
            user.groups.add(user_group)
            user.save()
            try:
                profile = UserProfile(
                    i_am_a=i_am_a, user=user, bio=bio, phone_number=phone_number, gender=gender,
                    profile_pics=profile_pics, occupation=occupation, address=address
                )
                profile.save()
                educations = Education.objects.filter(user=request.user)
                for education in educations:
                    profile.highest_education.add(education)
                messages.success(request, 'Profile Created Successfully')
                if user.groups.filter(name='Customer').exists():
                    return redirect('/users/home/')
                elif user.groups.filter(name='Service Provider').exists():
                    return redirect('/users/user_profile/') # change this to dashboard for user services
                else:
                    return redirect('/users/user_profile/')
            except:
                messages.error(request, 'Failed To Create Your Profile')
                return render(request, 'users/user_profile.html')
        return render(request, 'users/user_profile.html', {'groups': g})


@login_required
def view_user_profile(request):
    user = UserProfile.objects.get(user__email=request.user.email)
    context = {
        'i_am_a': user.i_am_a, 'email': user.user.email, 'first_name': user.user.first_name, 'last_name': user.user.last_name,
        'username': user.user.username, 'gender': user.gender, 'phone_number': user.phone_number, 'profile_pics': user.profile_pics, 
        'occupation': user.occupation, 'address': user.address, 'bio': user.bio
    }
    return render(request, 'users/view_profile.html', context)


@login_required
def view_others_profile(request, id):
    user_profile = UserProfile.objects.get(user__id=id)
    return render(request, 'users/others_profile.html', {'user_profile': user_profile})


@login_required
def list_all_users(request):
    users = User.objects.all()
    return render(request, 'users/all_users.html', {'users': users})