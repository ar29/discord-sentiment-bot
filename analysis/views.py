from django.shortcuts import render
from analysis.models import DiscordMessage
from django.db.models import Count

def sentiment_dashboard(request):
    # Aggregate sentiment data
    sentiment_data = DiscordMessage.objects.values('sentiment').annotate(count=Count('sentiment'))

    return render(request, 'dashboard.html', {'sentiment_data': sentiment_data})
