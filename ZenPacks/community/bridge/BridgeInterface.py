########################################################################################################################
# BridgeInterface
########################################################################################################################

# from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('BridgeInterface')

__doc__ = '''BridgeInt

BridgeInt is a component of BridgeDevice

$Id: $'''

__version__ = '$Revision: $'[11:-2]


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

    _relations = (
        ('BridgeDev', ToOne(ToManyCont, 'ZenPacks.community.bridge.BridgeDevice', 'BridgeInt')),
        )

    factory_type_information = (
        {
            'id':             'BridgeInterface',
            'meta_type':      'BridgeInterface',
            'description':    'Bridge Interface Info',
            'product':        'bridge',
            'immediate_view': 'viewBridgeInterface',
            'actions':        (
                {'id':          'status',
                 'name':        'Bridge Interface Graphs',
                 'action':      'viewBridgeInterface',
                 'permissions': (ZEN_VIEW, ),
                 },
                {'id':          'perfConf',
                 'name':        'Bridge Interface Template',
                 'action':      'objTemplates',
                 'permissions': (ZEN_CHANGE_SETTINGS,),
                 },
                {'id':          'viewHistory',
                 'name':        'Modifications',
                 'action':      'viewHistory',
                 'permissions': (ZEN_VIEW,),
                 },
            )
        }
    )

    isUserCreatedFlag = True

    def isUserCreated(self):
        """
        Returns the value of isUserCreated. True adds SAVE & CANCEL buttons to Details menu
        """
        return self.isUserCreatedFlag

    def viewName(self):
        """
        Pretty version human readable version of this object
        :return:
        """
        if self.RemoteAddress == '00:00:00:00:00:00' or self.Port == '-1':
            return 'Unknown'
        else:
            return str(self.Port)+'-'+self.RemoteAddress

    titleOrId = name = viewName

    def primarySortKey(self):
        """
        Sort by port number then remote AC
        :return:
        """
        return '{}{}'.format(self.Port, self.RemoteAddress)

    def device(self):
        return self.BridgeDev()

    def monitored(self):
        """
        If a bridge channel is exists, start monitoring it
        :return:
        """
        return True

    def getRemoteInterface(self):
        """
        return html snippets used in the UI to display links to remote interfaces for a MAC and their
        associated IP addresses
        :return:
        """
        interfaces = []
        # noinspection SpellCheckingInspection
        for intobj in self._getInterfaces():
            ipaddrs = [ip.urlLink() for ip in intobj.getIpAddressObjs()]
            interfaces.append('<p> style="padding:0.5em">{}: {}</p>'.format(intobj.urlLink(), ', '.join(ipaddrs)))
        return interfaces

    def getRemoteDevice(self):
        """
        return the remote device object for this bridge port. If any are returned based on the MAC query, wes take the
        first one assuming that MACs are unique to devices
        :return:
        """
        intobj = self._getInterfaces()
        if intobj and intobj[0].device():
            return intobj[0].device().urlLink()

    def _getInterfaces(self):
        """
        return a list of interfaces that match a MAC address from the layer2 index. There can be many interfaces per
        MAC because logical interfaces on one physical port share the same MAC
        :return:
        """
        intobjs = []
        for brain in self.dmd.ZenLinkManager.layer2_catalog(macaddress=self.RemoteAddress):
            try:
                intobjs.append(brain.getObject())
            except KeyError, e:
                log.error('Object {} not found from layer2 index, the index needs to be rebuilt'.
                          format(self.RemoteAddress))
        return intobjs


InitializeClass(BridgeInterface)
