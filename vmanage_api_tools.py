#########################################################################
# Created by robhugh on 9 February 2022, on behalf of Cisco Systems, Inc.
#########################################################################

from vmanage.api.authentication import Authentication
from vmanage.api.device import Device
from vmanage.data.template_data import TemplateData
from vmanage.api.device_templates import DeviceTemplates
from vmanage.api.feature_templates import FeatureTemplates
from certificate import Certificate
from smart_account import SmartAccount
import pprint
import time
import copy
from threading import Thread


def generate_host_and_username(pod_number):
    if pod_number < 10:
        vmanage_host = 'demo-lab-pod' + str(pod_number) + '.sdwan.cisco.com'
        vmanage_username = 'pod-0' + str(pod_number)
        return vmanage_host, vmanage_username
    else:
        vmanage_host = 'demo-lab-pod' + str(pod_number) + '.sdwan.cisco.com'
        vmanage_username = 'pod-' + str(pod_number)
        return vmanage_host, vmanage_username


def vmanage_auth(pod_number):
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    auth = Authentication(host=vmanage_host, user=vmanage_username, password='Cisco123$').login()
    return auth


def show_all_cgws():
    for pod_number in range(9, 9 + 1):
        print('Pod ' + str(pod_number) + ':')
        pp = pprint.PrettyPrinter(indent=2)

        auth = vmanage_auth(pod_number)
        vmanage_host, vmanage_username = generate_host_and_username(pod_number)
        vmanage_device = Device(auth, vmanage_host)
        device_config_list = vmanage_device.get_device_config_list('all')
        for device in device_config_list:
            if device['deviceModel'] == 'cellular-gateway-CG418-E':
                pp.pprint(device)
        print('\n')


def show_feature_templates(pod_number):
    auth = vmanage_auth(pod_number)
    pp = pprint.PrettyPrinter(indent=2)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    template_data = TemplateData(auth, vmanage_host)
    exported_feature_template_list = template_data.feature_templates.get_feature_template_list()
    pp.pprint(exported_feature_template_list)


def detach_device_templates(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    device_templates = DeviceTemplates(auth, vmanage_host)

    device_templates_list = device_templates.get_device_template_list()
    device_template_ids = []
    for device_template in device_templates_list:
        device_template_ids.append(device_template['templateId'])
    for device_template_id in device_template_ids:
        attached_devices = device_templates.get_attachments(device_template_id)
        if len(attached_devices) != 0:
            devices = Device(auth, vmanage_host)
            for attached_device in attached_devices:
                device_status = devices.get_device_status(attached_device, key='host-name')
                DeviceTemplates.detach_from_template(device_templates, uuid=device_status['uuid'],
                                                     device_ip=device_status['system-ip'], device_type='vedge')


def delete_device_template(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    device_templates = DeviceTemplates(auth, vmanage_host)

    device_templates_list = device_templates.get_device_template_list()
    device_template_id = ''
    for device_template in device_templates_list:
        if device_template['deviceType'] == "cellular-gateway-CG418-E":
            device_template_id = device_template['templateId']
    if device_template_id != '':
        attached_device = device_templates.get_attachments(device_template_id)
        if len(attached_device) != 0:
            devices = Device(auth, vmanage_host)
            device_status = devices.get_device_status(attached_device[0], key='host-name')
            DeviceTemplates.detach_from_template(device_templates, uuid=device_status['uuid'],
                                                 device_ip=device_status['system-ip'], device_type='vedge')
            time.sleep(60)
        DeviceTemplates.delete_device_template(device_templates, device_template_id)


def delete_feature_templates(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    feature_templates = FeatureTemplates(auth, vmanage_host)

    feature_templates_list = feature_templates.get_feature_template_list()
    for feature_template in feature_templates_list:
        FeatureTemplates.delete_feature_template(feature_templates, feature_template['templateId'])


def invalidate_certificate(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    devices = Device(auth, vmanage_host)
    devices_data = devices.get_device_list(category='vedges')
    pass


def sync_smart_account(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    smart_acct = SmartAccount(auth, vmanage_host)
    smart_acct.sync_smart_account('CiscoLiveUser13810', 'Cisco123$')


def delete_all_devices(starting_pod, ending_pod):
    pass


def show_device_templates(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    device_templates = DeviceTemplates(auth, vmanage_host)
    pp = pprint.PrettyPrinter(indent=2)
    exported_device_template_list = device_templates.get_device_template_list()
    pp.pprint(exported_device_template_list)


def device_template_map(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    device_templates = DeviceTemplates(auth, vmanage_host)
    devices = Device(auth, vmanage_host)
    device_templates_list = device_templates.get_device_template_list()
    for device_template in device_templates_list:
        attached_devices = device_templates.get_attachments(device_template['templateId'])
        if len(attached_devices) != 0 and attached_devices[0] != '--':
            print('template name: ' + device_template['templateName'])
            for attached_device in attached_devices:
                device_status = devices.get_device_status(attached_device, key='host-name')
                print('attached device: ' + attached_device)
                print(device_status['uuid'])
                print('site id: ' + device_status['site-id'])
                print('system ip: ' + device_status['system-ip'] + '\n')


def device_template_maps():
    for pod_number in range(1, 8 + 1):
        print('Pod ' + str(pod_number) + ':\n')
        device_template_map(pod_number)
        print('\n')


def clean_up_one_pod(pod_number):
    delete_device_template(pod_number)
    delete_device_template(pod_number)
    delete_feature_templates(pod_number)
    print(f'Pod {pod_number} completed.')


def clean_up_controller_lab(starting_pod, ending_pod):
    threads = []
    for pod_number in range(starting_pod, ending_pod + 1):
        t = Thread(target=clean_up_one_pod, args=(pod_number,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def test_certificate(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    certificate = Certificate(auth, vmanage_host)
    certificate.get_vedge_list()


def get_feature_template(pod_number):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    template_data = TemplateData(auth, vmanage_host)
    exported_feature_template_list = template_data.feature_templates.get_feature_template_list()
    feature_template = exported_feature_template_list[2]
    return feature_template


def push_feature_template(pod_number, feature_template):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    feature_templates = FeatureTemplates(auth, vmanage_host)
    feature_templates.add_feature_template(feature_template)


def push_device_template(pod_number, device_template):
    auth = vmanage_auth(pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(pod_number)
    device_templates = DeviceTemplates(auth, vmanage_host)
    device_templates.add_device_template(device_template)


def clone_feature_templates(source_pod_number, destination_pod_number):
    delete_device_template(destination_pod_number)
    auth = vmanage_auth(source_pod_number)
    vmanage_host, vmanage_username = generate_host_and_username(source_pod_number)
    source_feature_templates = FeatureTemplates(auth, vmanage_host)
    source_feature_templates_list = source_feature_templates.get_feature_template_list()

    for feature_template in source_feature_templates_list:
        push_feature_template(destination_pod_number, feature_template)


def traverse_subtemplates(template_list, source_to_destination_feature_templateId_dict):
    if 'subTemplates' in template_list:
        for subTemplate in template_list['subTemplates']:
            subTemplate['templateId'] = source_to_destination_feature_templateId_dict[subTemplate['templateId']]
            traverse_subtemplates(subTemplate, source_to_destination_feature_templateId_dict)


def clone_device_templates(source_pod_number, destination_pod_number):
    source_auth = vmanage_auth(source_pod_number)
    source_vmanage_host, source_vmanage_username = generate_host_and_username(source_pod_number)
    destination_auth = vmanage_auth(destination_pod_number)
    destination_vmanage_host, destination_vmanage_username = generate_host_and_username(destination_pod_number)

    source_device_templates = DeviceTemplates(source_auth, source_vmanage_host)
    source_feature_templates = FeatureTemplates(source_auth, source_vmanage_host)
    source_device_templates_list = source_device_templates.get_device_template_list()
    source_feature_templates_list = source_feature_templates.get_feature_template_list(factory_default=True)

    destination_feature_templates = FeatureTemplates(destination_auth, destination_vmanage_host)
    destination_feature_templates_dict = destination_feature_templates.get_feature_template_dict(factory_default=True)

    source_to_destination_feature_templateId_dict = {}
    for source_feature_template in source_feature_templates_list:
        source_templateId = source_feature_template['templateId']
        source_templateName = source_feature_template['templateName']
        source_to_destination_feature_templateId_dict[source_templateId] = \
            destination_feature_templates_dict[source_templateName]['templateId']

    destination_device_templates_list = source_device_templates_list
    for destination_device_template in destination_device_templates_list:
        for generalTemplate in destination_device_template['generalTemplates']:
            generalTemplate['templateId'] = source_to_destination_feature_templateId_dict[generalTemplate['templateId']]
            traverse_subtemplates(generalTemplate, source_to_destination_feature_templateId_dict)

    for destination_device_template in destination_device_templates_list:
        push_device_template(destination_pod_number, destination_device_template)


if __name__ == '__main__':
    clone_feature_templates(1, 4)
    clone_device_templates(1, 4)
