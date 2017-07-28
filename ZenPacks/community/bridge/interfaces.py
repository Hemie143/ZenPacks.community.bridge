from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.form import schema
# from Products.Zuul.utils import ZuulMessageFactory as _t

__doc__ = '''interfaces

describes the form field to the user interface.

$Id: interfaces.py, $'''


class IBridgeInterfaceInfo(IComponentInfo):
    """
    Info adapter for Bridge Interface component
    """
    Port            = schema.Text(title=u'Port',             readonly=True, group='Details')
    RemoteAddress   = schema.Text(title=u'Remote MAC',       readonly=True, group='Details')
    RemoteInterface = schema.Text(title=u'Remote Interface', readonly=True, group='Details')
    RemoteDevice    = schema.Text(title=u'Remote Device',    readonly=True, group='Details')
    PortStatus      = schema.Text(title=u'Port Status',      readonly=True, group='Details')
    PortComment     = schema.Text(title=u'Port Comment',     readonly=True, group='Details')

