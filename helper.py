from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

#functions start
def get_credential():
    default_credential = DefaultAzureCredential()
    return default_credential

def set_blob_data(data, storageAccountName, credential, containerName, blobName):
    blob_service_client = BlobServiceClient(account_url = f"https://{storageAccountName}.blob.core.windows.net", credential = credential)
    blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
    blob_client.upload_blob(data, blob_type = "BlockBlob", overwrite = True)

def get_blob_data(storageAccountName, credential, containerName, blobName):
    blob_service_client = BlobServiceClient(account_url = f"https://{storageAccountName}.blob.core.windows.net", credential = credential)
    try:
        blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
        downloader = blob_client.download_blob(max_concurrency=1, encoding='UTF-8')
    except:
        return None
    data = downloader.readall()
    return data

def download_blob(storageAccountName, credential, containerName, blobName, destinationPath):
    blob_service_client = BlobServiceClient(account_url = f"https://{storageAccountName}.blob.core.windows.net", credential = credential)
    blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
    with open(destinationPath, mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())

def get_primary_storage_account_key(storageAccountName, subscriptionID, credential):
    resource_client = ResourceManagementClient(credential, subscriptionID)
    resourceList = resource_client.resources.list()
    for item in resourceList:
        if(item.type == 'Microsoft.Storage/storageAccounts' and item.name == storageAccountName):
            resource_group_name = (item.id).split('/')[4]
    storageClient = StorageManagementClient(credential, subscriptionID)
    keys = storageClient.storage_accounts.list_keys(resource_group_name, storageAccountName)
    primaryKey = keys.keys[0].value
    return primaryKey

#functions end