from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .customvision import prediction_key, prediction_resource_id, project_id, publish_iteration_name, ENDPOINT
from .models import FoodInfo, FoodCategory, FoodItem
from itertools import chain
import json
from django.views import View


from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

class UserInfoView(View):
    """Вывод персональной информации"""
    def get(self, request):
        model = FoodInfo.objects.filter(owner=request.user)
        print(model)
        information = sorted(model, key=lambda instance: instance.date, reverse=True)
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

        return render(request, 'info.html', context={'information': information, 'count_values':count_values})



class BackgroundImageAnalyze(View):
    """Распознавание объектов"""
    def post(self, request):
        print("start customvision")
        rezult = []
        names = []
        if request.FILES.get("img"):
            prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
            predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

            image_contents = request.FILES.get("img")
            results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())

            for prediction in results.predictions:
                if(prediction.probability * 100 > 30):
                    rezult.append(prediction.tag_name)
            for rez in rezult:
                try:
                    names.append(FoodItem.objects.get(visionname__iexact=rez).name)
                except:
                    names.append("Not Found")
        else:
            rezult = None
            names = None
        return HttpResponse(json.dumps({'rezult':rezult, 'names':names}))



class BackgroundFoodAnalzeView(View):
    """Возвращает список возможных блюд"""
    def post(self, request):
        foodlist_objects = request.POST.get("data").split(";")
        foodlist_names = []
        if(len(foodlist_objects) > 1):
            foodlist_objects = foodlist_objects[:-1]
            foodlist_names = [json.loads(obj)['visionname'] for obj in foodlist_objects]
            print(foodlist_names)

        ingredients = FoodItem.objects.filter(visionname__in=foodlist_names)
        rezult = []
        for dish in FoodItem.objects.filter(isDish=True):
            if set(dish.ingredients.all()).issubset(set(ingredients)):
                rezult.append(dish)

        print(rezult)
        return HttpResponse(json.dumps([ob.as_json() for ob in rezult]))


class BackgroundAddFoddView(View):
    """Сохранение выбранной еды в базу данных"""

    def post(self, request):
        foodlist_objects = request.POST.get("data").split(";")
        if(len(foodlist_objects) > 1):
            for food_obj in foodlist_objects[:-1]:
                food_json = json.loads(food_obj)
                try:
                    food = FoodItem.objects.get(name=food_json["name"])
                except:
                    return HttpResponse("error")
                try:
                    fi = FoodInfo(owner=request.user, food=food, weight=food_json["weight"])
                except:
                    fi = FoodInfo(owner=request.user, food=food, weight=100)
                print(fi)
                fi.save()
        return HttpResponse("ok")


class IndexView(View):
    """Главная страница"""
    template = "index.html"

    def get(self, request):
        model = FoodItem.objects.filter(isDish=False)
        foodlist = sorted(model, key=lambda instance: instance.name)
        dishlist = FoodItem.objects.filter(isDish=True)
        return render(request, self.template, context={'foodlist': foodlist, 'dishlist':dishlist})


class FAQView(View):
    """О нас"""
    template = "faq.html"

    def get(self, request):
        return render(request, self.template)