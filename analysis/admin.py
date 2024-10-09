from django.contrib import admin
from .models import DiscordMessage

# Register the DiscordMessage model with the admin site
@admin.register(DiscordMessage)
class DiscordMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'channel', 'sentiment', 'timestamp')  # Customize the fields shown in the list view
    search_fields = ('author', 'content', 'channel')  # Enable search functionality
    list_filter = ('sentiment', 'channel')  # Enable filtering by sentiment and channel
    ordering = ('-timestamp',)  # Order by created_at in descending order

