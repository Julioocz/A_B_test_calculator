from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import ab_calculator


# Create your views here.
@csrf_exempt
def index(request):
    """
    Index and main view of the A/B split test calculator app. It renders the calculator index on 
    any GET request. It also calculates the significance and if the result is significant for 
    POST request.
    
    POST request params:
        visitors[control]: number of visitors for the control version of the experiment
        conversions[control]: number of conversions for the control version of the experiment
        visitors[variant]: number of visitors for the variant version for the experiment
        conversions[variant]: number of conversions for the variant version of the experiment
    """
    if request.method == 'GET':
        return render(request, 'calculator/index.html')

    elif request.method == 'POST':
        visitors_control = float(request.POST['visitors[control]'])
        visitors_variant = float(request.POST['visitors[variant]'])
        conversions_control = float(request.POST['conversions[control]'])
        conversions_variant = float(request.POST['conversions[variant]'])

        significance = ab_calculator.significance(visitors_control, conversions_control,
                                                  visitors_variant, conversions_variant)

        if significance < settings.MAX_SIGNIFICANCE_LEVEL:
            significant = True

        else:
            significant = False

        return JsonResponse({'significance': significance, 'significant': significant})

    else:
        return HttpResponseBadRequest()
