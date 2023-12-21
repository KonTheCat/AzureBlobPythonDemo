from azure.identity import ChainedTokenCredential, AzureCliCredential, ManagedIdentityCredential
import datetime
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas
)

#functions start
def get_credential():
    return ChainedTokenCredential(AzureCliCredential(), ManagedIdentityCredential())

def get_blob_service_client(credential, storage_account_name):
    return BlobServiceClient(account_url = f"https://{storage_account_name}.blob.core.windows.net", credential = credential)

def set_blob_data(data, client, containerName, blobName):
    blob_service_client = client
    blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
    blob_client.upload_blob(data, blob_type = "BlockBlob", overwrite = True)

def get_blob_data(client, containerName, blobName):
    blob_service_client = client
    try:
        blob_client = blob_service_client.get_blob_client(container = containerName, blob = blobName)
        downloader = blob_client.download_blob(max_concurrency=1)
    except:
        return None
    data = downloader.readall()
    return data

def get_user_delegation_key(blob_service_client, expire_time_minutes):
    delegation_key_start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = -15)
    delegation_key_expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = expire_time_minutes)

    user_delegation_key = blob_service_client.get_user_delegation_key(
        key_start_time=delegation_key_start_time,
        key_expiry_time=delegation_key_expiry_time
    )

    return user_delegation_key

def get_user_delegation_sasurl_blob(client, user_delegation_key, container_name, blob_name, expire_time_minutes):
    # Create a SAS token that's valid for one day, as an example
    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = -15)
    expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = expire_time_minutes)
    blob_client = client.get_blob_client(container = container_name, blob = blob_name)

    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=blob_client.container_name,
        blob_name=blob_client.blob_name,
        user_delegation_key=user_delegation_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time,
        start=start_time
    )
    sas_url = f"{blob_client.url}?{sas_token}"

    return sas_url

def update_blob_tags(client, container_name, blob_name, new_tags):
    blob_client = client.get_blob_client(container=container_name, blob=blob_name)
    tags = blob_client.get_blob_tags()
    tags.update(new_tags)
    blob_client.set_blob_tags(tags)

#functions end

#config starts
testFilePath = '.\storinteractAAD_requirements.txt'
storageAccountName = 'konthecat'
blobContainerName = 'demo'
blobName = 'storinteractAAD_requirements.txt'
tags = {'Sealed': 'true', 'Date': '2022-02-01', 'Sexy': 'false'}
#config ends

#demo code beings
file = open(testFilePath, "rb")
data = file.read()
file.close()
credential = get_credential()
client = get_blob_service_client(credential, storageAccountName)
user_delegation_key = get_user_delegation_key(client, 15)
#set_blob_data(data, client, blobContainerName, blobName)
#print(get_blob_data(client, blobContainerName, blobName))
#print(get_user_delegation_sasurl_blob(client, user_delegation_key, blobContainerName, blobName, 15))
update_blob_tags(client, blobContainerName, blobName, tags)
#demo code ends