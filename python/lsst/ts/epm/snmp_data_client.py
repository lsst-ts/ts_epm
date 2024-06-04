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

__all__ = ["SnmpDataClient"]

import asyncio
import logging
import math
import re
import types
import typing

import yaml
from lsst.ts import salobj
from lsst.ts.ess import common
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    nextCmd,
)

from .mib_tree_holder import MibTreeHolder
from .snmp_server_simulator import SnmpServerSimulator
from .utils import TelemetryItemName, TelemetryItemType

numeric_const_pattern = (
    r"[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?"
)
rx = re.compile(numeric_const_pattern, re.VERBOSE)


class SnmpDataClient(common.data_client.BaseReadLoopDataClient):
    """Read SNMP data from a server and publish it as EPM telemetry.

    SNMP stands for Simple Network Management Protocol.
    EPM stands for Electronic Power Mamnager.

    Parameters
    ----------
    config : `types.SimpleNamespace`
        The configuration, after validation by the schema returned
        by `get_config_schema` and conversion to a types.SimpleNamespace.
    topics : `salobj.Controller`
        The telemetry topics this model can write, as a struct with attributes
        such as ``tel_temperature``.
    log : `logging.Logger`
        Logger.
    simulation_mode : `int`, optional
        Simulation mode; 0 for normal operation.

    Notes
    -----
    The config is required to contain "max_read_timeouts". If it doesn't, a
    RuntimeError is raised at instantiation.
    """

    def __init__(
        self,
        config: types.SimpleNamespace,
        topics: salobj.Controller | types.SimpleNamespace,
        log: logging.Logger,
        simulation_mode: int = 0,
    ) -> None:
        super().__init__(
            config=config,
            topics=topics,
            log=log,
            simulation_mode=simulation_mode,
        )

        self.mib_tree_holder = MibTreeHolder()

        # Attributes for the SNMP requests.
        self.snmp_engine = SnmpEngine()
        self.community_data = CommunityData("public", mpModel=0)
        self.transport_target = UdpTransportTarget((self.config.host, self.config.port))
        self.context_data = ContextData()
        self.object_type = ObjectType(
            ObjectIdentity(self.mib_tree_holder.mib_tree["sysDescr"].oid)
        )

        # Keep track of the nextCmd function so we can override it when in
        # simulation mode.
        self.next_cmd = nextCmd

        # Attributes for telemetry processing.
        self.snmp_result: dict[str, str] = {}
        self.system_description = "No system description set."

    @classmethod
    def get_config_schema(cls) -> dict[str, typing.Any]:
        """Get the config schema as jsonschema dict."""
        return yaml.safe_load(
            """
$schema: http://json-schema.org/draft-07/schema#
description: Schema for SnmpDataClient.
type: object
properties:
  host:
    description: Host name of the TCP/IP interface.
    type: string
    format: hostname
  port:
    description: Port number of the TCP/IP interface. Defaults to the SNMP port.
    type: integer
    default: 161
  max_read_timeouts:
    description: Maximum number of read timeouts before an exception is raised.
    type: integer
    default: 5
  device_name:
    description: The name of the device.
    type: string
  device_type:
    description: The type of device.
    type: string
    enum:
    - pdu
    - scheiderPm5xxx
    - xups
  poll_interval:
    description: The amount of time [s] between each telemetry poll.
    type: number
    default: 1.0
  location:
    description: Device location.
    type: string
required:
  - host
  - port
  - max_read_timeouts
  - device_name
  - device_type
  - poll_interval
  - location
additionalProperties: false
"""
        )

    def descr(self) -> str:
        """Return a brief description, without the class name.

        This should be just enough information to distinguish
        one instance of this client from another.
        """
        return f"[host={self.config.host}, port={self.config.port}]"

    async def setup_reading(self) -> None:
        """Perform any tasks before starting the read loop.

        In this case the system description is retrieved and stored in memory,
        since this is not expected to change.
        """
        if self.simulation_mode == 1:
            snmp_server_simulator = SnmpServerSimulator(log=self.log)
            self.next_cmd = snmp_server_simulator.snmp_cmd

        await self.execute_next_cmd()
        # Only the sysDescr value is expected at this moment.
        sys_descr = self.mib_tree_holder.mib_tree["sysDescr"].oid + ".0"
        if len(self.snmp_result) == 1 and sys_descr in self.snmp_result:
            self.system_description = self.snmp_result[sys_descr]
        else:
            self.log.error("Could not retrieve sysDescr. Continuing.")

        # Create the ObjectType for the particular SNMP device type.
        device_type = self.config.device_type
        if device_type in self.mib_tree_holder.mib_tree:
            self.object_type = ObjectType(
                ObjectIdentity(self.mib_tree_holder.mib_tree[device_type].oid)
            )
        else:
            raise ValueError(
                f"Unknown device type {device_type!r}. "
                "Continuing querying only for 'sysDescr'."
            )

    async def read_data(self) -> None:
        """Read data from the SNMP server."""
        await self.execute_next_cmd()
        device_type = self.config.device_type
        telemetry_topic = getattr(self.topics, f"tel_{device_type}")
        telemetry_dict: dict[str, int | float | str] = {
            "systemDescription": self.system_description
        }

        telemetry_items = [
            i
            for i in vars(telemetry_topic.DataType)
            if not (
                i.startswith("private_")
                or i.startswith("_")
                or i == "salIndex"
                or i == "systemDescription"
            )
        ]

        if device_type != "pdu":
            for telemetry_item in telemetry_items:
                mib_name = TelemetryItemName(telemetry_item).name
                # TODO DM-44577 Handle list items correctly.
                # Any single value OID ends in ".0" in the SNMP response. Any
                # multiple value ends in ".1", ".2", etc. We only regard ".1"
                # for now.
                parent = self.mib_tree_holder.mib_tree[mib_name].parent
                assert parent is not None
                mib_oid = self.mib_tree_holder.mib_tree[mib_name].oid + (
                    ".0" if not parent.index else ".1"
                )
                snmp_value = await self.get_telemetry_item_value(
                    telemetry_item, mib_name, mib_oid
                )
                telemetry_dict[telemetry_item] = snmp_value
        else:
            # TODO DM-44576 Handle PDU telemetry separately.
            # TODO DM-44577 Add "systemDescription" to the PDU telemetry and
            #  handle list items correctly.
            pass

        await telemetry_topic.set_write(**telemetry_dict)
        await asyncio.sleep(self.config.poll_interval)

    async def get_telemetry_item_value(
        self, telemetry_item: str, mib_name: str, mib_oid: str
    ) -> int | float | str:
        """Get the value of a telemetry item.

        Parameters
        ----------
        telemetry_item : `str`
            The name of the telemetry item.
        mib_name : `str`
            The MIB name of the item.
        mib_oid : `str`
            The MIB OID of the item.

        Returns
        -------
        int | float | str
            The value of the item.

        Raises
        ------
        ValueError
            In case no float value could be gotten.
        """
        telemetry_type = TelemetryItemType[mib_name]
        snmp_value: int | float | str
        match telemetry_type:
            case "int":
                if mib_oid in self.snmp_result:
                    snmp_value = int(self.snmp_result[mib_oid])
                else:
                    snmp_value = 0
                    self.log.warning(
                        f"Could not find {mib_oid=} for int {telemetry_item=}"
                    )
            case "float":
                try:
                    if mib_oid in self.snmp_result:
                        snmp_value = await self._extract_float_from_string(
                            self.snmp_result[mib_oid]
                        )
                    else:
                        snmp_value = math.nan
                        self.log.warning(
                            f"Could not find {mib_oid=} for float {telemetry_item=}"
                        )
                except ValueError:
                    self.log.error(
                        f"Could not convert value {self.snmp_result[mib_oid]!r} "
                        f"for {mib_oid=} == {telemetry_item=} to float."
                    )
                    snmp_value = math.nan
            case "string":
                if mib_oid in self.snmp_result:
                    snmp_value = self.snmp_result[mib_oid]
                else:
                    snmp_value = ""
                    self.log.warning(
                        f"Could not find {mib_oid=} for str {telemetry_item=}"
                    )
            case _:
                snmp_value = self.snmp_result[mib_oid]
        return snmp_value

    async def _extract_float_from_string(self, float_string: str) -> float:
        """Extract a float value from a string.

        It is assumed here that there only is a single float value in the
        string. If no or more than one float value is found, a ValueError is
        raised.

        Parameters
        ----------
        float_string : `str`
            The string containing the float value.

        Raises
        ------
        ValueError
            In case no single float value could be extracted from the string.
        """
        try:
            float_value = float(float_string) / 10.0
        except ValueError as e:
            float_values = rx.findall(float_string)
            if len(float_values) > 0:
                float_value = float_values[0]
            else:
                raise e
        return float_value

    async def execute_next_cmd(self) -> None:
        """Execute the SNMP nextCmd command.

        Raises
        ------
        RuntimeError
            In case an SNMP error happens, for instance the server cannot be
            reached.
        """
        iterator = self.next_cmd(
            self.snmp_engine,
            self.community_data,
            self.transport_target,
            self.context_data,
            self.object_type,
            lookupMib=False,
            lexicographicMode=False,
        )

        self.snmp_result = {}
        for error_indication, error_status, error_index, var_binds in iterator:
            if error_indication:
                raise RuntimeError(
                    f"Exception contacting SNMP server with {error_indication=}"
                )
            elif error_status:
                raise RuntimeError(
                    "Exception contacting SNMP server with "
                    f"{error_status.prettyPrint()} at "
                    f"{error_index and var_binds[int(error_index) - 1][0] or '?'}"
                )
            else:
                for var_bind in var_binds:
                    self.snmp_result[var_bind[0].prettyPrint()] = var_bind[
                        1
                    ].prettyPrint()
