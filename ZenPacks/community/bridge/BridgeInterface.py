########################################################################################################################
# BridgeInterface
########################################################################################################################

__doc__ = '''BridgeInt

BridgeInt is a component of BridgeDevice

$Id: $'''

__version__ = '$Revision: $'[11:-2]


from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getlogger('BridgeInterface')

class BridgeInterface(DeviceComponent, ManagedEntity):
    # Bridge Interface

    portal_type = meta_type = 'BridgeInterface'

    # Custom data Variables here from modeling
    RemoteAddress = '00:00:00:00:00:00'
    Port = '-1'
    PortIfIndex = 2
    PortStatus = '4'
    PortComment = 'This is a comment'

    _properties = (
        {'id': 'RemoteAddress', 'type': 'string', 'mode': ''},
        {'id': 'Port',          'type': 'string', 'mode': ''},
        {'id': 'PortIfIndex',   'type': 'int',    'mode': ''},
        {'id': 'PortStatus',    'type': 'string', 'mode': ''},
        {'id': 'PortComment',   'type': 'string', 'mode': ''},
    )

    _relations = Device._relations + (
        ('BridgeDev', ToOne(ToManyCont, 'ZenPacks.community.bridge.BridgeDevice', 'BridgeInt')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(BridgeDevice)
