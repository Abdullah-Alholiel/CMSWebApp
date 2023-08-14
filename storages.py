
from django.conf import settings
from .settings import AZURE_SA_NAME, AZURE_SA_KEY
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = AZURE_SA_NAME
    account_key = AZURE_SA_KEY
    azure_container = 'media'
    expiration_secs = None
    
    
class AzureStaticStorage(AzureStorage):
    account_name = AZURE_SA_NAME
    account_key = AZURE_SA_KEY
    azure_container = 'static'
    expiration_secs = None