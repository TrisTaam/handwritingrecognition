import base64
import os
import random
import re
import string

import numpy as np
import requests
from PIL import Image
from cntk.ops.functions import load_model
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader


def index_view(request):
    template = loader.get_template('api/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def convert_image(image_data, filename):
    img_str = re.search(r'base64,(.*)', str(image_data)).group(1)
    img = base64.b64decode(img_str)
    with open(filename + '.png', 'wb') as output:
        output.write(img)


def predict_use_cognitive_service(image_file_name):
    api_key = settings.API_KEY
    endpoint = settings.ENDPOINT
    url = endpoint + "computervision/imageanalysis:analyze"

    with open(image_file_name, "rb") as ouput:
        image_data = ouput.read()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': api_key
    }
    params = {
        'features': 'read',
        'model-version': 'latest',
        'language': 'en',
        'api-version': '2024-02-01'
    }
    response = requests.post(url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    result = response.json()
    data = ""
    try:
        for line in result['readResult']['blocks'][0]['lines']:
            data += (line['text'] + "\n")
    except IndexError:
        data = ""
    return data.rstrip()


def predict_use_cntk_model(image_file_name):
    model = load_model(os.path.join(settings.BASE_DIR, "model/cntk.model"))
    image = Image.open(image_file_name).convert('1')
    image.thumbnail((28, 28), Image.LANCZOS)
    image_np = np.array(image.getdata()).astype(int)
    image_np_expanded = np.expand_dims(image_np, axis=0)

    predicted_label_probs = model.eval({model.arguments[0]: image_np_expanded})
    data = np.argmax(predicted_label_probs, axis=1)
    return str(data[0])


def predict_view(request):
    post_data = request.POST.items()
    pd = [p for p in post_data]
    image_data = pd[0][0].replace(" ", "+")
    image_data += "===="
    filename = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(32)])
    convert_image(image_data, filename)
    data = predict_use_cognitive_service(filename + '.png')
    print(data)
    return JsonResponse({"data": data})
