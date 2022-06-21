from .JsonReponse import PTCJsonResponseServerError
from .models import TimeLog


def open_timelog_processor(request):
    openTime = None

    if request.user.is_authenticated:
        # check for open time
        try:
            openTime = TimeLog.objects.get(end_date__isnull=True, user_id=request.user)

        except TimeLog.MultipleObjectsReturned:
            return PTCJsonResponseServerError(message='Found too many - check in admin page!')

        except TimeLog.DoesNotExist:
            pass

    return {
        'open_timelog': openTime
    }
