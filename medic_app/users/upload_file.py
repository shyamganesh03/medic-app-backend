from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from decouple import config

# Scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

google_drive_config={
    "type": "service_account",
    "project_id": config('GOOGLE_DRIVE_PROJECT_ID'),
    "private_key_id": config('GOOGLE_DRIVE_PRIVATE_KEY_ID'),
    "private_key": config('GOOGLE_DRIVE_PRIVATE_KEY').replace('\\n', '\n'), 
    "client_email": config('GOOGLE_DRIVE_CLIENT_EMAIL'),
    "client_id": config('GOOGLE_DRIVE_CLIENT_ID'),
    "auth_uri": config('AUTH_URI'),
    "token_uri": config('TOKEN_URI'),
    "auth_provider_x509_cert_url": config('AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": config('GOOGLE_DRIVE_CLIENT_CERT_URL'),
    "universe_domain": config('UNIVERSE_DOMAIN')
}

# Authenticate using service account
credentials = service_account.Credentials.from_service_account_info(google_drive_config,scopes=SCOPES)

# Initialize Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

# ID of the shared folder you created in Google Drive
FOLDER_ID = config('GOOGLE_DRIVE_FOLDER_ID')

def delete_file_by_name_in_folder(fileId: str) -> bool:
       try:
        drive_service.files().delete(fileId=fileId).execute()
       except Exception as e:
           return False


def file_exists_in_folder(file_name: str, folder_id: str):
    query = (
        f"name = '{file_name}' and "
        f"'{folder_id}' in parents and "
        f"trashed = false"
    )

    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()

    files = results.get('files', [])
    if files:
        return {'file_id': files[0]['id'], 'hasFile': True}
    else:
        return {'file_id': None, 'hasFile': False}


def get_or_create_user_folder(user_id:str):
    # Search for a folder named as the user_id
    query = f"name = '{user_id}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if FOLDER_ID:
        query += f" and '{FOLDER_ID}' in parents"

    response = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = response.get('files', [])

    if folders:
        return folders[0]['id']  # Folder already exists

    # Create folder
    folder_metadata = {
        'name': user_id,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if FOLDER_ID:
        folder_metadata['parents'] = [FOLDER_ID]

    folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()
    return folder['id']

def upload_photo(file_path:str,uid:str,category_type:str):
    user_folder_id = get_or_create_user_folder(uid)
    already_exist_file_details = file_exists_in_folder(category_type,user_folder_id)
    print(already_exist_file_details)
    if already_exist_file_details['hasFile']:
        delete_file_by_name_in_folder(already_exist_file_details['file_id'])
    file_metadata = {
        'name': category_type,
        'parents': [user_folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='image/jpeg')

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()


    return uploaded_file
