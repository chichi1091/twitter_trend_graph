import calendar
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboards.models.trends import Trends


class TrendsView(APIView):

    def get(self, request, format=None):
        s, e = calendar.monthrange(int(datetime.now().strftime("%Y")), int(datetime.now().strftime("%m")))
        start_date = datetime.now().strftime("%Y-%m-01")
        end_date = datetime.now().strftime("%Y-%m-" + str(e))
        list = Trends.objects.filter(target_date__range=(start_date, end_date))

        dict = map((lambda x: {
            "id": x.id
            , "title": x.target_date
            , "uel": 'http://hoge.com'
            , "class": ""
            , 'start': 0
            , "end": 0
        }), list)

        response = {
            "success": 1,
            "result": dict
        }

        print(response)

        return Response(response)