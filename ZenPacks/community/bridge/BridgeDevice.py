########################################################################################################################
# BridgeDevice
########################################################################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
# from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class BridgeDevice(Device):
    # Bridge Device

    _relations = Device._relations + (
        ('BridgeInt', ToManyCont(ToOne, 'ZenPacks.community.bridge.BridgeInterface', 'BridgeDev')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(BridgeDevice)
