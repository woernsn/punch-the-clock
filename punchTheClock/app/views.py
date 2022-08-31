from datetime import timedelta
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

import secrets
from cryptography.fernet import Fernet

from .JsonReponse import PTCJsonResponse, PTCJsonResponseServerError, PTCJsonResponseForbidden, PTCJsonResponseNotAllowed
from .forms import ProfileForm, TimeLogForm
from .models import Profile, TimeLog


@login_required
def timelog_list(request, sorting = 'desc'):
    sortSign = '-'

    if request.method == 'GET':
        if request.GET.get('sorting', 'desc') == 'asc':
            sortSign = ''

    elif request.method == 'POST':
        if 'numDaysRange' in request.POST:
            request.session['numDays'] = request.POST['numDaysRange']

    numDays = request.session.get('numDays')

    now = timezone.now()
    pastDays = now - timedelta(days=(int(numDays) if numDays else 30))

    timelogs = TimeLog.objects.filter(user_id=request.user.id).filter(start_date__gte=pastDays).order_by(f'{sortSign}start_date')

    return render(request, 'app/timelog_list.html', {'timelog_list': timelogs, 'title': 'List', 'sortAsc': sortSign == '', 'showLastDays': numDays})


@login_required
def timelog_calendar(request):
    now = timezone.now()
    past_date_before_2months = now - timedelta(weeks=settings.WEEKS_TO_SHOW)
    timelogs = TimeLog.objects.filter(user_id=request.user.id).filter(start_date__gte=past_date_before_2months)
    return render(request, 'app/timelog_calendar.html', {'timelog_list': timelogs, 'title': 'Calendar'})


@login_required
def timelog_details(request, timelog_id):
    timelog = get_object_or_404(TimeLog, pk=timelog_id)
    if timelog.user_id != request.user:
        return HttpResponseForbidden()

    updated = False
    if request.method == 'POST':
        if 'update' in request.POST:
            form = TimeLogForm(request.POST, instance=timelog)
            if form.is_valid():
                new_timelog = form.save(commit=False)
                new_timelog.user_id = request.user
                new_timelog.save()
                updated = True
        elif 'delete' in request.POST:
            timelog.delete()
            return HttpResponseRedirect('/list')

    elif request.method == 'GET':
        form = TimeLogForm(instance=timelog)

    else:
        return HttpResponseNotAllowed(f'{request.method} not allowed!')

    return render(request, 'app/timelog_details.html', {'form': form, 'timelog_id': timelog_id, 'title': f'Details (#{timelog_id})', 'updated': updated})


@login_required
def token(request):

    generated = False

    if request.method == 'GET':
        # Show only placeholder
        form = ProfileForm()
        form['token'].initial = '*' * settings.TOKEN_LENGTH

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        isUnique = False
        while not isUnique:
            # generate token
            token = secrets.token_urlsafe(settings.TOKEN_LENGTH)

            # encrypt and store
            secret = settings.SECRET
            fernet = Fernet(secret.encode())
            encrypted_token = fernet.encrypt(token.encode())

            q = Profile.objects.filter(token=encrypted_token)
            if q.count() == 0:
                isUnique = True

        # save encrypted token to database
        user = User.objects.get(pk=request.user.id)
        user.profile.token = encrypted_token
        user.save()

        form['token'].initial = token
        generated = True

    return render(request, 'app/token.html', {'form': form, 'title': 'API Token', 'generated': generated})


@csrf_exempt
def apiPunch(request):
    if request.method != 'POST':
        return PTCJsonResponseNotAllowed(message='Only POST is allowed.')

    isRest = True
    if request.user.is_authenticated:
        user = request.user
        isRest = False

    else:
        # Handle calls coming via REST
        auth: str = request.headers.get('Authorization')
        if auth is None or not auth.startswith('Bearer'):
            return PTCJsonResponseForbidden(message='You have to be authorized!')

        # Find user for token
        token = auth.removeprefix('Bearer ')

        try:
            user = search_user_for_token(token)
        except User.DoesNotExist:
            return PTCJsonResponseForbidden()
        except User.MultipleObjectsReturned:
            return PTCJsonResponseServerError(message='Multiple users found. Please report.')

    now = timezone.now()

    # check for open time
    try:
        currentTime = TimeLog.objects.get(end_date__isnull=True, user_id=user)

    except TimeLog.MultipleObjectsReturned:
        return PTCJsonResponseServerError(message='Found too many - check in admin page!')

    except TimeLog.DoesNotExist:
        # None found - creating new one
        tl = TimeLog(start_date=now, user_id=user)
        tl.save()

        if isRest:
            return PTCJsonResponse(message='Successfully created TimeLog.', object=tl.json())
        else:
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    # Time found - updating existing one
    currentTime.end_date = now
    currentTime.save()

    if isRest:
        return PTCJsonResponse(message='Successfully updated TimeLog.', object=currentTime.json())
    else:
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.token = None
    user.save()


def search_user_for_token(token: str) -> User:
    secret = settings.SECRET
    fernet = Fernet(secret.encode())

    users = User.objects.all()
    for user in users:
        if user.profile.token is None:
            continue

        decrypted_token = fernet.decrypt(bytes(user.profile.token)).decode()  # https://code.djangoproject.com/ticket/27813
        if decrypted_token == token:
            return user

    raise User.DoesNotExist()
