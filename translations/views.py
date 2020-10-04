import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from translations.helpers import get_translation_sources_info, save_translation_suggestion
from translations.models import Language


@login_required
def get_translations_info(request):
    sources = get_translation_sources_info()

    data = {
        "langs": [{"code": l.code, "title": l.title} for l in Language.objects.order_by("code")],
        "sources": sources
    }
    response = JsonResponse(data)
    return response

@csrf_exempt
@login_required
def suggest_translation(request):
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({
            "result": "Error",
            "message": "Can't parse your json"
        })

    try:
        save_translation_suggestion(data, request.user)
        result = {
            "result": "Ok"
        }
    except:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            "result": "Error",
            "message": "Can't save suggestion"
        })

    response = JsonResponse(result)
    return response
