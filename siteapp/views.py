from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from .customvision import *
from .models import IngredientInfo, DishInfo, IngredientItem, DishItem
from itertools import chain
import json
from django.views import View


from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

class UserInfoView(View):

    def get(self, request):
        model1 = IngredientInfo.objects.filter(owner=request.user)
        model2 = DishInfo.objects.filter(owner=request.user)
        information = sorted(list(chain(model1, model2)), key=lambda instance: instance.date, reverse=True)
        count_values = {
            'nProteins':0,
            'nFats':0,
            'nCarbohydrates':0,
        }
        for item in information:
            print(item)
            item.food.calories *= item.weight / 100
            item.food.fats *= item.weight / 100
            item.food.carbohydrates *= item.weight / 100
            item.food.proteins *= item.weight / 100
            count_values['nProteins'] += item.food.proteins
            count_values['nFats'] += item.food.fats
            count_values['nCarbohydrates'] += item.food.carbohydrates

        return render(request, 'index2.html', context={'information': information, 'count_values':count_values})


class BackgroundImageAnalyze(View):
    def post(self, request):
        rezult = []
        if request.FILES.get("img"):
            prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
            predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

            image_contents = request.FILES.get("img")
            results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())

            for prediction in results.predictions:
                if(prediction.probability * 100 > 30):
                    rezult.append(prediction.tag_name)
        else:
            rezult = None
        return HttpResponse(json.dumps({'rezult':rezult}))


class BackgroundAddView(View):
    def post(self, request):
        for jsontiem in request.POST.get("data").split(";"):
            print(json.loads(jsontiem))
        return HttpResponse("ok")

class IndexView(View):
    template = "index.html"

    def get(self, request):
        model1 = IngredientItem.objects.all()
        model2 = DishItem.objects.all()

        foodlist = sorted(list(chain(model1, model2)), key=lambda instance: instance.name)
        return render(request, self.template, context={'foodlist': foodlist})