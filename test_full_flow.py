"""测试完整的 devices tab 数据流和 XML 生成."""

import sys

sys.path.insert(0, 'D:/codehub/py_tools')

from model.vm_model.core.vm_config import VMConfig
from utils.xml_generator import LibvirtXMLGenerator

# 1. 模拟 devices tab 的 to_xml 方法返回的配置
print('=' * 60)
print('步骤 1: Devices Tab to_xml() 输出')
print('=' * 60)

devices_tab_xml = {
    'disks': [
        {
            'type': 'file',
            'device': 'disk',
            'bus': 'virtio',
            'driver_type': 'qcow2',
            'target_dev': 'vda',
            'source': '/path/to/image.qcow2',
            'source_file': '/path/to/image.qcow2',
            'readonly': False,
            'boot_order': '',
        },
    ],
    'graphics': [
        {
            'type': 'vnc',
            'port': '-1',
            'autoport': True,
            'listen': '0.0.0.0',
            'keymap': 'en-us',
            'passwd': '',
        },
    ],
    'videos': [
        {
            'model': 'qxl',
            'vram': '16384',
            'heads': '1',
            'accel3d': False,
        },
    ],
    'controllers': [
        {
            'type': 'scsi',
            'model': 'virtio-scsi',
            'index': '0',
        },
    ],
}

for key, value in devices_tab_xml.items():
    print(f'  {key}: {len(value)} 项')

# 2. 模拟 vm_config.update_from_tab()
print('\n' + '=' * 60)
print("步骤 2: VMConfig.update_from_tab('devices', ...)")
print('=' * 60)

vm_config = VMConfig()
vm_config.update_from_tab('devices', devices_tab_xml)

print(f'  vm_config.devices.disk: {len(vm_config.devices.disk)} 项')
print(f'  vm_config.devices.graphic: {len(vm_config.devices.graphic)} 项')
print(f'  vm_config.devices.controller: {len(vm_config.devices.controller)} 项')

# 3. 模拟 vm_config.to_dict()
print('\n' + '=' * 60)
print('步骤 3: VMConfig.to_dict()')
print('=' * 60)

config_dict = vm_config.to_dict()
devices_in_dict = config_dict.get('devices', {})
for key, value in devices_in_dict.items():
    if isinstance(value, list):
        print(f'  {key}: {len(value)} 项')
    else:
        print(f'  {key}: {value}')

# 4. 生成 XML
print('\n' + '=' * 60)
print('步骤 4: LibvirtXMLGenerator.generate()')
print('=' * 60)

test_config = {
    'name': 'test-vm',
    'devices': devices_in_dict,
}

generator = LibvirtXMLGenerator()
try:
    xml_output = generator.generate(test_config)
    print('XML 生成成功!')
    print('\nXML 预览:')
    print('-' * 60)
    # 只显示 devices 部分
    in_devices = False
    for line in xml_output.split('\n'):
        if '<devices>' in line:
            in_devices = True
        if in_devices:
            print(line)
        if '</devices>' in line:
            in_devices = False
            print('  ... (省略其他内容)')
            break
except Exception as e:
    print(f'XML 生成失败：{e}')
    import traceback

    traceback.print_exc()
