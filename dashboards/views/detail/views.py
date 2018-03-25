import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboards.models.trends import Trends


class TrendsDetailView(APIView):

    def get(self, request, day, format=None):
        d = datetime.datetime.strptime(day, '%Y%m%d')
        trends = Trends.objects.filter(target_date=d.strftime('%Y-%m-%d'))

        lists = [{
            "name": str(trend.count) + ":" + trend.word
            , "val": trend.count
        } for trend in trends]
        response = {"children": lists}

        return Response(response)
