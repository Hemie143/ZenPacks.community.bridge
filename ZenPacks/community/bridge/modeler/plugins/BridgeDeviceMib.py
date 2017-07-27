########################################################################################################################
# BridgeDeviceMib modeler plugin
########################################################################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

__doc__ = '''BridgeDeviceMib

BridgeDeviceMib gets number of ports and base MAC address for switch supporting Bridge MIB

$Id: $'''

__version__ = '$Revision: $'[11:-2]

class BridgeDeviceMib(SnmpPlugin):

    modname = 'ZenPacks.community.bridge.BridgeDevice'

    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.17.1.1.0': 'setHWSerialNumber',
        '.1.3.6.1.2.1.17.1.2.0': 'setHWTag',
    })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing {} for device {}'.format(self.name(), device.id))
        # Collect physical port forwarding table
        getdata, tabledata = results

        try:
            om = self.objectMap(getdata)
            om.setHWSerialNumber = self.asmac(om.setHWSerialNumber)
            om.setHWtag = 'Number of ports = {}'.format(om.setHWtag)
            return om
        except:
            log.warn(' Error in getting data for BridgeDeviceMib modeler plugin')
