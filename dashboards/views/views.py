import calendar
from datetime import datetime
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboards.models.trends import Trends


class TrendsView(APIView):

    def get(self, request, format=None):
        s, e = calendar.monthrange(int(datetime.now().strftime("%Y")), int(datetime.now().strftime("%m")))
        start_date = datetime.now().strftime("%Y-%m-01")
        end_date = datetime.now().strftime("%Y-%m-" + str(e))
        list = Trends.objects\
            .filter(target_date__range=(start_date, end_date))\
            .values('target_date')\
            .annotate(total=Sum('count'))

        print(list)

        dict = [{
            "id": i
            , "title": item['target_date'].strftime("%Y-%m-%d")
            , "url": 'dashboard/' + item['target_date'].strftime("%Y-%m-%d")
            , "class": "event-important"
            , 'start': 1000
            , "end": 5000
        } for i, item in enumerate(list)]

        response = {
            "success": 1,
            "result": dict
        }

        print(response)

        return Response(response)
