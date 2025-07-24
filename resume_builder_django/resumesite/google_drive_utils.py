from allauth.socialaccount.models import SocialToken, SocialAccount
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from django.contrib.auth import get_user_model


def upload_resume_to_drive(user, file_path, filename=None):
    # Get the user's Google OAuth token
    try:
        token = SocialToken.objects.get(account__user=user, account__provider='google')
    except SocialToken.DoesNotExist:
        return False, 'No Google account connected.'

    creds = Credentials(
        token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=token.app.client_id,
        client_secret=token.app.secret,
        scopes=['https://www.googleapis.com/auth/drive.file']
    )

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': filename or 'resume.pdf'}
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        return True, file.get('webViewLink')
    except Exception as e:
        return False, str(e) 