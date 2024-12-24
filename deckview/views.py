from asgiref.sync import async_to_sync
from django.http import HttpResponse, HttpResponseNotFound

from image_creator import create_picture


def main(request):
    try:
        deck_code = request.GET.get('code').replace(" ", '+')
        im = async_to_sync(create_picture)(deck_code)

        if im is None:
            return HttpResponseNotFound('insufficient code')

        im = im.resize((im.size[0] // 2, im.size[1] // 2))

        response = HttpResponse(content_type='image/png')
        im.save(response, "PNG")
        return response
    except Exception as e:
        print("\n\n\n\n\n______ERROR_____\n\n\n\n", e)
        return HttpResponseNotFound('insufficient code')
