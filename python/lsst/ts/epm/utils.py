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
    "MibTreeElement",
    "MibTreeElementType",
    "TelemetryItemName",
    "TelemetryItemType",
    "TelemetryItemUnit",
]

import enum
from dataclasses import dataclass


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
    fFrequency = "systemFrequency"
    lcIC = "loadCurrentC"
    lcIa = "loadCurrentA"
    lcIb = "loadCurrentB"
    lcIn = "neutralCurrent"
    midSerialNumber = "serialNumber"
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
    fFrequency = "float"
    lcIC = "float"
    lcIa = "float"
    lcIb = "float"
    lcIn = "float"
    midSerialNumber = "string"
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
    fFrequency = "Hz"
    lcIC = "A"
    lcIa = "A"
    lcIb = "A"
    lcIn = "A"
    midSerialNumber = "unitless"
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
