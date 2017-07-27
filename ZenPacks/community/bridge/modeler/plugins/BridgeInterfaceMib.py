########################################################################################################################
# BridgeInterfaceMib modeler plugin
########################################################################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
# from Products.DataCollector.plugins.DataMaps import ObjectMap

__doc__ = '''BridgeInterfaceMib

BridgeInterfaceMib maps interfaces on a switch supporting the Bridge MIB

$Id: $'''

__version__ = '$Revision: $'[11:-2]


class BridgeInterfaceMib(SnmpPlugin):
    relname = 'BridgeInt'
    modname = 'ZenPacks.community.bridge.BridgeInterface'

    weight = 4

    snmpGetTableMaps = (
        GetTableMap('dot1dBasePortEntry', '.1.3.6.1.2.1.17.1.4.1',
                    {
                        '.1': 'BasePort',
                        '.2': 'BasePortIfIndex',
                    }
                    ),
        GetTableMap('dot1dTpFdbEntry', '.1.3.6.1.2.1.17.4.3.1',
                    {
                        '.1': 'RemoteAddress',
                        '.2': 'Port',
                        '.3': 'PortStatus',
                    }
                    ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing {} for device {}'.format(self.name(), device.id))
        # Collect physical port forwarding table
        getdata, tabledata = results

        log.warn("Get Data= %s", getdata)
        log.warn("Table Data= %s", tabledata)

        BaseTable = tabledata.get('dot1dBasePortEntry')
        if not BaseTable:
            log.warn('No SNMP response from {} for the {} plugin'.format(device.id, self.name()))
            log.warn('Data={}'.format(getdata))
            return

        PortTable = tabledata.get('dot1dTpFdbEntry')
        if not PortTable:
            log.warn('No SNMP response from {} for the {} plugin'.format(device.id, self.name()))
            log.warn('Data={}'.format(getdata))
            return

        rm = self.relMap()

        for oid, data in PortTable.items():
            try:
                om = self.objectMap(data)
                om.RemoteAddress = self.asmac(om.RemoteAddress)
                om.snmpindex = int(om.Port)
                for boid, bdata in BaseTable.items():
                    try:
                        if bdata['BasePort'] == om.Port:
                            om.PortIfIndex = bdata.get('BasePortIfIndex', -1)
                    except (KeyError, IndexError, AttributeError), errorInfo:
                        log.warn('Attribute error in BridgeInterfaceMib modeler plugin: {}'.format(errorInfo))
                        continue
                om.id = self.prepId('{}_{}'.format(om.Port, om.RemoteAddress))
            except AttributeError, errorInfo:
                log.warn('Attribute error in BridgeInterfaceMib modeler plugin: {}'.format(errorInfo))
                continue
            rm.append(om)
        return rm
