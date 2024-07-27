from asgiref.sync import async_to_sync
from django.http import HttpResponse

from image_creator import create_picture


def main(request):
    deck_code = request.GET.get('code')

    im = async_to_sync(create_picture)(deck_code)
    im = im.resize((im.size[0] // 2, im.size[1] // 2))

    response = HttpResponse(content_type='image/png')
    im.save(response, "PNG")
    return response

