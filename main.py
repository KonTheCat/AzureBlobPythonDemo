from helper import (
    get_credential,
    get_credentialChain, 
    get_blob_data, 
    set_blob_data, 
    get_primary_storage_account_key, 
    download_blob, 
    get_blob_userDelegationSASUrl,
    get_blob_sasURL
) 
import os

#config starts
testFilePath = 'requirements.txt'
storageAccountName = 'enter your storage account name here'
blobContainerName = 'enter your container name here'
blobName = 'requirements.txt'
imagePath = '.\cat.jpg'
newImageName = 'catFromBlob.jpg'
# this method of getting the subscription ID works in Web Apps and derived services such as Azure Functions.
# make sure that you enter your own subscription ID below. 
try:
    subscriptionID = os.getenv('WEBSITE_OWNER_NAME').split('+')[0]
except: 
    subscriptionID = 'enter your subscription ID here'
#config ends

#demo code starts
file = open(testFilePath, "rb")
data = file.read()
file.close()
credential = get_credential()
credentialChain = get_credentialChain()
set_blob_data(data, storageAccountName, credential, blobContainerName, blobName)
print(get_blob_data(storageAccountName, credential, blobContainerName, blobName))

file = open(imagePath, "rb")
data = file.read()
file.close()
set_blob_data(data, storageAccountName, credential, blobContainerName, newImageName)
download_blob(storageAccountName, credential, blobContainerName, newImageName, newImageName)

# WARNING: this next line of code will return the primary storage account key to the console. Unless you are deleting the storage account
# shortly after, rotate the storage account key. This is intended as a demonstration. 
# This requires having an Azure AD Role Assignment that includes the Microsoft.Storage/storageAccounts/listKeys/action.
# "Reader and Data Access" is a good least-privilege option. This should be used only in scenarios where for whatever reason
# Azure AD is not a workable authentication/authorization mechanism. Storage Account keys or connection strings should never 
# need to be stored in Key Vaults or environment variables especially when working within Azure, just get the key from the resource.   
print("Writing primary storage account key below:")
storageAccountKey = get_primary_storage_account_key(storageAccountName, subscriptionID, credential)
print(storageAccountKey)

print("Writing URL with SAS Token signed by primary storage account key below:")
print(get_blob_sasURL(storageAccountName, storageAccountKey, blobContainerName, blobName))

print("Writing URL with SAS Token signed by user delegation key (Entra ID) below:") 
print(get_blob_userDelegationSASUrl(storageAccountName, credential, blobContainerName, blobName))

#demo code ends

