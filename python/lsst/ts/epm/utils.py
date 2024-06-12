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

from __future__ import annotations

__all__ = [
    "FREQUENCY_OID_LIST",
    "PDU_HEX_OID_LIST",
    "SCHNEIDER_FLOAT_AS_STRING_OID_LIST",
    "MibTreeElement",
    "MibTreeElementType",
    "TelemetryItemName",
    "TelemetryItemType",
    "TelemetryItemUnit",
]

import enum
from dataclasses import dataclass

# List of OIDs for which the frequency value is given in tens of Hz.
FREQUENCY_OID_LIST = [
    "1.3.6.1.4.1.534.1.3.1.0",
    "1.3.6.1.4.1.534.1.4.2.0",
    "1.3.6.1.4.1.534.1.5.1.0",
]

# List of PDU OIDs for which a float value is given as a hexidecimal encoded
# string.
PDU_HEX_OID_LIST = [
    "1.3.6.1.4.1.21728.3.3.2.0",
    "1.3.6.1.4.1.21728.3.3.3.0",
    "1.3.6.1.4.1.21728.3.3.4.0",
    "1.3.6.1.4.1.21728.3.3.5.0",
]

# List of Schneider UPS OIDs for which a float value is given as a plain text
# string.
SCHNEIDER_FLOAT_AS_STRING_OID_LIST = [
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.1.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.2.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.3.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.5.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.6.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.5.7.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.3.1.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.3.2.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.3.3.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.3.4.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.2.1.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.1.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.2.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.3.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.5.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.6.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.7.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.9.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.10.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.11.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.1.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.2.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.3.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.5.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.6.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.7.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.4.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.8.8.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.4.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.8.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.7.12.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.10.2.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.10.6.0",
    "1.3.6.1.4.1.3833.1.100.1.3.1.3.10.10.0",
]


@dataclass
class MibTreeElement:
    """MIB Tree Element.

    A Tree Element can either be a BRANCH or a LEAF.
    """

    name: str
    description: str
    oid: str
    parent: MibTreeElement | None
    type: str
    index: str | None = None

    def __repr__(self) -> str:
        return self.oid


class MibTreeElementType(enum.StrEnum):
    """MIB Tree Element Type."""

    BRANCH = "BRANCH"
    LEAF = "LEAF"


class TelemetryItemName(enum.StrEnum):
    aeActiveEDelivered = "activeEnergyDelivered"
    aeApparentEDelivered = "apparentEnergyDelivered"
    aeReactiveEDelivered = "reactiveEnergyDelivered"
    aeResetDateTime = "resetDateTime"
    currentDrawMax1 = "acMaxDraw"
    currentDrawStatus1 = "acCurrentDraw"
    fFrequency = "systemFrequency"
    lcIC = "loadCurrentC"
    lcIa = "loadCurrentA"
    lcIb = "loadCurrentB"
    lcIn = "neutralCurrent"
    midSerialNumber = "serialNumber"
    outletStatus = "powerOutletStatus"
    pActivePa = "activePowerA"
    pActivePb = "activePowerB"
    pActivePc = "activePowerC"
    pActivePtot = "totalActivePower"
    pApparentPa = "apparentPowerA"
    pApparentPb = "apparentPowerB"
    pApparentPc = "apparentPowerC"
    pApparentPtot = "totalApparentPower"
    pReactivePa = "reactivePowerA"
    pReactivePb = "reactivePowerB"
    pReactivePc = "reactivePowerC"
    pReactivePtot = "totalReactivePower"
    pfPfDisplacementA = "displacementPowerFactorA"
    pfPfDisplacementB = "displacementPowerFactorB"
    pfPfDisplacementC = "displacementPowerFactorC"
    pfPfDisplacementTotal = "totalDisplacementPowerFactor"
    pfPfa = "powerFactorA"
    pfPfb = "powerFactorB"
    pfPfc = "powerFactorC"
    pfPftot = "totalPowerFactor"
    sysDescr = "systemDescription"
    vVab = "measuredLineVoltageVab"
    vVan = "measuredLineVoltageVan"
    vVbc = "measuredLineVoltageVbc"
    vVbn = "measuredLineVoltageVbn"
    vVca = "measuredLineVoltageVca"
    vVcn = "measuredLineVoltageVcn"
    xupsBatCapacity = "batteryCapacity"
    xupsBatCurrent = "batteryCurrent"
    xupsBatTimeRemaining = "batteryTimeRemaining"
    xupsBatVoltage = "batteryVoltage"
    xupsBatteryAbmStatus = "batteryAbmStatus"
    xupsBypassFrequency = "bypassFrequency"
    xupsBypassTable = "bypassTable"
    xupsEnvAmbientTemp = "envAmbientTemp"
    xupsInputFrequency = "inputFrequency"
    xupsInputTable = "inputTable"
    xupsInputVoltage = "inputVoltage"
    xupsOutputFrequency = "outputFrequency"
    xupsOutputLoad = "outputLoad"
    xupsOutputTable = "outputTable"


class TelemetryItemType(enum.StrEnum):
    aeActiveEDelivered = "float"
    aeApparentEDelivered = "float"
    aeReactiveEDelivered = "float"
    aeResetDateTime = "string"
    currentDrawMax1 = "float"
    currentDrawStatus1 = "float"
    fFrequency = "float"
    lcIC = "float"
    lcIa = "float"
    lcIb = "float"
    lcIn = "float"
    midSerialNumber = "string"
    outletStatus = "int"
    pActivePa = "float"
    pActivePb = "float"
    pActivePc = "float"
    pActivePtot = "float"
    pApparentPa = "float"
    pApparentPb = "float"
    pApparentPc = "float"
    pApparentPtot = "float"
    pReactivePa = "float"
    pReactivePb = "float"
    pReactivePc = "float"
    pReactivePtot = "float"
    pfPfDisplacementA = "float"
    pfPfDisplacementB = "float"
    pfPfDisplacementC = "float"
    pfPfDisplacementTotal = "float"
    pfPfa = "float"
    pfPfb = "float"
    pfPfc = "float"
    pfPftot = "float"
    sysDescr = "string"
    vVab = "float"
    vVan = "float"
    vVbc = "float"
    vVbn = "float"
    vVca = "float"
    vVcn = "float"
    xupsBatCapacity = "float"
    xupsBatCurrent = "float"
    xupsBatTimeRemaining = "float"
    xupsBatVoltage = "float"
    xupsBatteryAbmStatus = "int"
    xupsBypassFrequency = "float"
    xupsBypassTable = "string"
    xupsEnvAmbientTemp = "float"
    xupsInputFrequency = "float"
    xupsInputTable = "string"
    xupsInputVoltage = "float"
    xupsOutputFrequency = "float"
    xupsOutputLoad = "float"
    xupsOutputTable = "string"


class TelemetryItemUnit(enum.StrEnum):
    aeActiveEDelivered = "J"
    aeApparentEDelivered = "J"
    aeReactiveEDelivered = "J"
    aeResetDateTime = "unitless"
    currentDrawMax1 = "A"
    currentDrawStatus1 = "A"
    fFrequency = "Hz"
    lcIC = "A"
    lcIa = "A"
    lcIb = "A"
    lcIn = "A"
    midSerialNumber = "unitless"
    outletStatus = "unitless"
    pActivePa = "kW"
    pActivePb = "kW"
    pActivePc = "kW"
    pActivePtot = "kW"
    pApparentPa = "kW"
    pApparentPb = "kW"
    pApparentPc = "kW"
    pApparentPtot = "kW"
    pReactivePa = "kW"
    pReactivePb = "kW"
    pReactivePc = "kW"
    pReactivePtot = "kW"
    pfPfDisplacementA = "unitless"
    pfPfDisplacementB = "unitless"
    pfPfDisplacementC = "unitless"
    pfPfDisplacementTotal = "unitless"
    pfPfa = "unitless"
    pfPfb = "unitless"
    pfPfc = "unitless"
    pfPftot = "unitless"
    sysDescr = "unitless"
    vVab = "V"
    vVan = "V"
    vVbc = "V"
    vVbn = "V"
    vVca = "V"
    vVcn = "V"
    xupsBatCapacity = "unitless"
    xupsBatCurrent = "A"
    xupsBatTimeRemaining = "s"
    xupsBatVoltage = "V"
    xupsBatteryAbmStatus = "unitless"
    xupsBypassFrequency = "Hz"
    xupsBypassTable = "unitless"
    xupsEnvAmbientTemp = "deg_C"
    xupsInputFrequency = "Hz"
    xupsInputTable = "unitless"
    xupsInputVoltage = "V"
    xupsOutputFrequency = "Hz"
    xupsOutputLoad = "unitless"
    xupsOutputTable = "unitless"
