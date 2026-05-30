from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .services import get_weekly_insights, get_monthly_insights

class WeeklyInsightsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request):
        # Utilisation d'une vue asynchrone (les appels DB doivent être dans sync_to_async)
        from asgiref.sync import sync_to_async
        # user = await sync_to_async(lambda: request.user)()
        # insights = await sync_to_async(get_weekly_insights)(user)
        insights = get_weekly_insights(request.user)
        return Response(insights)

class MonthlyInsightsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request):
        from asgiref.sync import sync_to_async
        # user = await sync_to_async(lambda: request.user)()
        # insights = await sync_to_async(get_monthly_insights)(user)
        insights = get_monthly_insights(request.user)
        return Response(insights)