# Azure Blob Python Demo
This is intended to demonstrate working with Azure Blob Storage to people moderately familiar with Azure and not necessarily with Python.
Many demos I have seen make use of the storage account key - this is not a great security or operational practice, you should use a storage account
key only if you have absolutely no other options. This demo uses Azure AD authentication. This is derived from and is intended as a demo version of the
relevant Microsoft documentation which is just not 100% friendly to an administrator attempting to enable developers without having a development background themselves. 

## Setup
1. Install Python. Version choice matters - if you are working with Azure Functions for example, you should use the most recent version supported for
that. At time of writing that is 3.10.https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-configuration#python-version
2. Install Azure CLI (or you can do the equivalents in Azure PowerShell, we are only using this to log in during local testing): 
3. Probably install Git, or download this repository to wherever you will be working on it from.
4. Probably install VSCode, if using VSCode install the Azure and Python extensions.
5. Ensure that in Azure you have a storage account and a container. Ensure that you have made the choices you intend to make as far as network access to that storage account.
6. Review the sample code, adding your own values where needed. Make sure you understand what the code intends and review the warning about the storage account key code.

## Discussion of Blob Storage Permissions

Blob storage implements two different authentication and authorization mechanisms:
1. Storage Account Key-based. The Storage Account key provides complete access to storage account functionality, it must not be given out and used lightly. Security initiatives will be made happier if it is not used at all.
    1. SAS URIs are a way to provide more restricted access. https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview
    2. Policies are a way to introduce a layer between the key and the SAS URI, so you can remove an individual policy and expire the SAS URIs using that policy, rather than having to roll the storage account key and expire all SAS URIs. https://learn.microsoft.com/en-us/rest/api/storageservices/define-stored-access-policy
2. Azure Active Directory. This is what we will be using. Identities (users, groups, apps, managed identities) need to be given special roles that provide data access - this works in the same way that Azure RBAC for Key Vaults works. https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access?tabs=portal
    1. For this example I would recommend using "Storage Blob Data Contributor" - this role can read and write. Assignment can be done on the level of the an individual container. No other access is required.

## Discussion of Authentication To Azure

Authentication is handled using DefaultAzureCredential. This approach will attempt several different authentication mechanisms in sequence. Please either ensure that you only have the needed mechanisms in play or that you modify the get_credential function according to your requirements which is covered in the second link below. 
https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential
https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#define-a-custom-authentication-flow-with-chainedtokencredential

## Running the Code
1. After you have installed Azure CLI and configured permissions you may log in with "az login".
2. Run "pip install -r .\requirements.txt" in the directory containing the code. This will install the needed Python packages. 
3. Running "python .\main.py" when in the directory containing the repo code should do. 