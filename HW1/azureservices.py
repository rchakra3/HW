# from azure import *
from azure.servicemanagement import ServiceManagementService
from azure.servicemanagement import OSVirtualHardDisk
from azure.servicemanagement import LinuxConfigurationSet
from azure.servicemanagement import PublicKey
from azure.servicemanagement import SSH
from azure.servicemanagement import KeyPair
from azure.servicemanagement import ConfigurationSet
from azure.servicemanagement import ConfigurationSetInputEndpoint
from azure.storage.blob import BlobService
import string
import random
import base64
from customparser import ConfigReader

config_reader = ConfigReader('config.ini')
config_params = config_reader.get_config_section_map("azure")

# from http://stackoverflow.com/a/2257449
def name_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


subscription_id = config_params["subscription_id"]
certificate_path = config_params["mgmt_cert_path"]

sms = ServiceManagementService(subscription_id, certificate_path)

# Because the name has to be unique in Their cloud :/
hosted_service_name = name_generator()
label = 'devOps test'
desc = 'Service for basic nginx server'
location = 'Central US'

# image_list = sms.list_os_images()

result = sms.create_hosted_service(hosted_service_name, label, desc, location)
operation_result = sms.get_operation_status(result.request_id)

storage_acc_name = name_generator()
label = 'mystorageaccount'
location = 'Central US'
desc = 'My storage account description.'

result = sms.create_storage_account(storage_acc_name, desc, label,
                                    location=location)

operation_result = sms.get_operation_status(result.request_id)
print('Operation status: ' + operation_result.status)

print "The following services are now up:"

result = sms.list_hosted_services()

for hosted_service in result:
    print('Service name: ' + hosted_service.service_name)
    print('Management URL: ' + hosted_service.url)
    print('Location: ' + hosted_service.hosted_service_properties.location)
    print('')


print "The following storage accounts are now up:"

result = sms.list_storage_accounts()


for account in result:
    print('Account Service name: ' + account.service_name)
    print('Storage account url: ' + account.url)
    print('Location: ' + account.storage_service_properties.location)
    print('Storage Account Keys:')
    storageServiceObj = sms.get_storage_account_keys(account.service_name)
    print storageServiceObj.storage_service_keys.primary
    print storageServiceObj.storage_service_keys.secondary
    print('')
    if account.service_name == storage_acc_name:
        storageServiceObj = sms.get_storage_account_keys(account.service_name)
        storage_acc_key = storageServiceObj.storage_service_keys.primary


# cert_path = "/home/rohan/temp2/myCert.pem"

cert_path = config_params["vm_cert_path"]

with open(cert_path, "rb") as bfile:
    # decode to make sure this is a str and not a bstr
    cert_data = base64.b64encode(bfile.read()).decode()
    cert_format = 'pfx'
    cert_password = ''
    cert_res = sms.add_service_certificate(service_name=hosted_service_name,
                                           data=cert_data,
                                           certificate_format=cert_format,
                                           password=cert_password)
    operation_result = sms.get_operation_status(cert_res.request_id)


# Create a container
blob_service = BlobService(account_name=storage_acc_name,
                           account_key=storage_acc_key)

container_name = "vm-container"

result = blob_service.create_container(container_name)

container_url_template = "http://{}.blob.core.windows.net/{}"

container_url = container_url_template.format(storage_acc_name, container_name)

image_name = "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04-LTS-amd64-server-20140414-en-us-30GB"

blob_url = container_url + "/ubuntu.vhd"

os_hd = OSVirtualHardDisk(image_name, blob_url)

vm_name = name_generator()

linux_config = LinuxConfigurationSet(vm_name, 'rohan', 'qwerty12#', True)

SERVICE_CERT_THUMBPRINT = config_params["vm_cert_thumbprint"]

vm_public_key_path = config_params["vm_pub_key_path"]

pk = PublicKey(SERVICE_CERT_THUMBPRINT, vm_public_key_path)

pair = KeyPair(SERVICE_CERT_THUMBPRINT, vm_public_key_path)


linux_config.ssh = SSH()

linux_config.ssh.key_pairs.key_pairs.append(pair)
linux_config.ssh.public_keys.public_keys.append(pk)

endpoint_config = ConfigurationSet()
endpoint_config.configuration_set_type = 'NetworkConfiguration'

ssh_endpoint = ConfigurationSetInputEndpoint(name='ssh', protocol='tcp',
                                             port='22', local_port='22',
                                             load_balanced_endpoint_set_name=None,
                                             enable_direct_server_return=False)
http_endpoint = ConfigurationSetInputEndpoint(name='http', protocol='tcp',
                                              port='80', local_port='80',
                                              load_balanced_endpoint_set_name=None,
                                              enable_direct_server_return=False)
endpoint_config.input_endpoints.input_endpoints.append(ssh_endpoint)
endpoint_config.input_endpoints.input_endpoints.append(http_endpoint)

result = sms.create_virtual_machine_deployment(service_name=hosted_service_name,
                                               deployment_name=hosted_service_name,
                                               deployment_slot='production',
                                               label=hosted_service_name,
                                               role_name=hosted_service_name,
                                               system_config=linux_config,
                                               network_config=endpoint_config,
                                               os_virtual_hard_disk=os_hd,
                                               role_size='Small')

operation_result = sms.get_operation_status(result.request_id)

print "Created VM with name:" + hosted_service_name

host_entry = hosted_service_name + ".cloudapp.net"
host_entry += " ansible_ssh_user=rohan"
host_entry += " ansible_ssh_private_key_file="
host_entry += config_params["vm_pvt_key_path"] + "\n"

with open("inventory", "a") as inventory_file:
    inventory_file.write(host_entry)
