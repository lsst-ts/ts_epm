# This file is part of ts_epm.
#
# Developed for the Vera Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the Vera Rubin Observatory
# Project (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["SnmpServerSimulator", "SIMULATED_SYS_DESCR"]

import logging
import typing

from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    Integer,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
)
from pysnmp.proto.rfc1155 import ObjectName
from pysnmp.proto.rfc1902 import OctetString

from .mib_tree import mib_tree
from .utils import TelemetryItemType

SIMULATED_SYS_DESCR = "SnmpServerSimulator"
SYS_DESCR = [
    (
        ObjectName(value=str(mib_tree["sysDescr"])),
        OctetString(value=SIMULATED_SYS_DESCR),
    )
]


class SnmpServerSimulator:
    """SNMP server simulator."""

    def __init__(self, log: logging.Logger) -> None:
        self.log = log.getChild(type(self).__name__)

    def snmp_cmd(
        self,
        snmp_engine: SnmpEngine,
        auth_data: CommunityData,
        transport_target: UdpTransportTarget,
        context_data: ContextData,
        *var_binds: typing.Any,
        **options: typing.Any,
    ) -> typing.Iterator:
        """Handle all SNMP commands."""

        assert snmp_engine is not None
        assert auth_data is not None
        assert transport_target is not None
        assert context_data is not None
        assert len(options) == 2

        # The pysnmp API is a mess so we need to access "private" members to
        # get the info we want. The noinspection comments keep PyCharm happy.
        assert isinstance(var_binds[0], ObjectType)
        # noinspection PyProtectedMember
        assert isinstance(var_binds[0]._ObjectType__args[0], ObjectIdentity)
        # noinspection PyProtectedMember
        object_identity = var_binds[0]._ObjectType__args[0]._ObjectIdentity__args[0]

        if object_identity == str(mib_tree["sysDescr"]):
            # Handle the getCmd call for the system description.
            return iter([[None, Integer(0), Integer(0), SYS_DESCR]])
        else:
            oid_branch = [t for t in mib_tree if str(mib_tree[t]) == object_identity]
            if len(oid_branch) != 1:
                return iter(
                    [[f"Unknown OID {object_identity}.", Integer(0), Integer(0), ""]]
                )

            snmp_items = []
            for oid in mib_tree:
                if str(mib_tree[oid]).startswith(object_identity):
                    try:
                        match TelemetryItemType[oid]:
                            case "int":
                                value = Integer(1)
                            case "float":
                                value = Integer(101)
                            case "string":
                                value = OctetString(value="Random string.")
                            case _:
                                value = Integer(0)
                                self.log.error(
                                    f"Unknown telemetry item type {TelemetryItemType[oid]} for {oid=}"
                                )
                        snmp_items.append(
                            [
                                None,
                                Integer(0),
                                Integer(0),
                                [(ObjectName(value=str(mib_tree[oid])), value)],
                            ]
                        )
                    except KeyError:
                        # Deliberately ignored.
                        pass
            return iter(snmp_items)
