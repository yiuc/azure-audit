[Subprocess management](https://docs.python.org/3/library/subprocess.html)

```python
from subprocess import call   
call(["az", "vm", "list", "-g", "rgName"])
```

`az login --service-principal -u http://sample-cli-login -p Test1234 --tenant 54826b22-38d6-4fb2-bad9-b7b93a3e9c5a`

```python
from azure.cli.core import get_default_cli
get_default_cli().invoke(['vm', 'list', '-g', 'groupname'])
```

[How to run Azure CLI commands using python?](https://stackoverflow.com/questions/51546073/how-to-run-azure-cli-commands-using-python#comment90060017_51546073)
[get_default_cli](https://github.com/Azure/azure-cli/blob/dev/src/azure-cli/azure/cli/__main__.py)


# Set up authentication from SDK
```
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.compute import ComputeManagementClient

client = get_client_from_cli_profile(ComputeManagementClient)
```

# Installation Step
`conda create -n peak python=3.6`
`pip install azure-cli`

[How to save the output of Azure-cli commands in a variable](https://stackoverflow.com/questions/52340497/how-to-save-the-output-of-azure-cli-commands-in-a-variable)
``` python
login_successfull = get_default_cli().invoke(['login',
                                                          '--tenant', tenant,
                                                          '--username', self.username,
                                                          '--password', self.password]) == 0
tenant = 'mytenant.onmicrosoft.com'
cmd = AzureCmd('login', 'mypassword')
cmd.login(tenant)
cmd.list_vm(tenant)
```

## General
### List account
`az account list -o table`

### Set subsrabtion
`az account set $SUBSCRIPTION_ID`

## KeyVault
### Show
`az keyvault list -o table`

### List
`az keyvault network-rule list --name <kv name> -o table`

## DDOS
### List
`az network ddos-protection list`

## NSG
### List
`az network nsg list -o table`

### Show
`az network nsg rule list --nsg-name <nsg-name> -g <RG>`

## [Storage Account](https://docs.microsoft.com/en-us/rest/api/storagerp/storageaccounts/storageaccounts_getproperties)
### Show
`az storage account list -o table`

### List
`az storage account network-rule list --account-name <accountname>`

[Reference](https://docs.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest)
[Power Shell Audit Resources](https://github.com/Merlus/powershell/blob/master/azure/Audit%20Resources/AuditNsgs.ps1)