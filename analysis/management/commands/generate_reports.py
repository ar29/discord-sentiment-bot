from django.core.management.base import BaseCommand
from analysis.models import DiscordMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
import smtplib
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.db.models import Count

GOOGLE_DOCS_SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']
STAKEHOLDER_EMAILS = ['aniruddha.ravi@gmail.com', 'aniruddha.mitm@gmail.com']

def create_google_doc_report(sentiment_data, report_title):
    # Authenticate using the credentials.json file
    credentials = service_account.Credentials.from_service_account_file(f"{settings.BASE_DIR}/credentials.json")
    drive_service = build('drive', 'v3', credentials=credentials)
    docs_service = build('docs', 'v1', credentials=credentials)    

    # Create a new Google Docs document
    document = docs_service.documents().create(body={
        'title': report_title
    }).execute()
    document_id = document['documentId']

    requests = [
        {'insertText': {'location': {'index': 1}, 'text': report_title + '\n\n'}},
    ]

    for sentiment, count in sentiment_data.values_list('sentiment', 'count').order_by('sentiment').distinct():
        requests.append(
            {'insertText': {
                'location': {'index': len(requests)},
                'text': f'{sentiment}: {count} messages\n'}}
        )

    docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'aniruddha.ravi@gmail.com'
    }

    # Send the permission to the Google Drive API
    drive_service.permissions().create(
        fileId=document_id,
        body=user_permission,
        fields='id'
    ).execute()

    return f'https://docs.google.com/document/d/{document_id}/edit'

def send_email_with_report(google_doc_link):
    subject = "Weekly Sentiment Report"
    body = f"Please find the sentiment analysis report at the following link: {google_doc_link}"
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=STAKEHOLDER_EMAILS,
        fail_silently=False,
    )

class Command(BaseCommand):
    help = 'Generate weekly sentiment report and send email to stakeholders.'

    def handle(self, *args, **kwargs):
        # Fetch messages from the past week
        from datetime import datetime, timedelta
        one_week_ago = datetime.now() - timedelta(days=7)
        messages = DiscordMessage.objects.filter(timestamp__gte=one_week_ago)

        # Analyze sentiment distribution
        sentiments = messages.values_list('sentiment', flat=True)
        positive = sentiments.filter(sentiment='POSITIVE').count()
        neutral = sentiments.filter(sentiment='NEUTRAL').count()
        negative = sentiments.filter(sentiment='NEGATIVE').count()

        # Generate a pie chart for sentiment distribution
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [positive, neutral, negative]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.savefig(f"{settings.BASE_DIR}/sentiment_report.png")
        plt.close() 

        sentiment_data = messages.values('sentiment').annotate(count=Count('sentiment'))
        report_title = f"Weekly Sentiment Report - {datetime.now().strftime('%Y-%m-%d')}"
        # Save report to Google Docs
        google_doc_link = create_google_doc_report(sentiment_data, report_title)
        # Send report via email 
        send_email_with_report(google_doc_link)
