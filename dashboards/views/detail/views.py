from rest_framework.response import Response
from rest_framework.views import APIView
from dashboards.models.trends import Trends


class TrendsDetailView(APIView):

    def get(self, request, day, format=None):
        trends = Trends.objects.get(target_date=day)

        lists = [{
            "name": trend.word
            , "val": trend.count
        } for trend in trends]

        return Response(lists)
