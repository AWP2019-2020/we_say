from app.models import Theme, Poll


def getThemes(request):
    return {
        'themes':Theme.objects.all(),
    }
