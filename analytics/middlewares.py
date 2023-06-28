from analytics.models import Analytics


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        telegram_id = request.META.get('HTTP_TELEGRAM_ID')
        if telegram_id:
            Analytics.set_analytics(telegram_id)
        response = self.get_response(request)
        return response
