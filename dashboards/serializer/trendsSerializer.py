from dashboards.models import Trends


class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trends
        fields = ('id', 'target_date', 'word', 'count')
