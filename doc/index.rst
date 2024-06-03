.. py:currentmodule:: lsst.ts.epm

.. _lsst.ts.epm:

###########
lsst.ts.epm
###########

.. image:: https://img.shields.io/badge/Project Metadata-gray.svg
    :target: https://ts-xml.lsst.io/index.html#index-master-csc-table-ess
.. image:: https://img.shields.io/badge/SAL\ Interface-gray.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/EPM.html
.. image:: https://img.shields.io/badge/GitHub-gray.svg
    :target: https://github.com/lsst-ts/ts_epm
.. image:: https://img.shields.io/badge/Jira-gray.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_epm

Overview
========

The EPM Commandable SAL Component (CSC) reads various PDUs and UPS-es at the Vera C. Rubin Observatory, and publishes the resulting data in EPM telemetry topics.

EPM stands for Electronical Power Manager.

.. _lsst.ts.epm-user_guide:

User Guide
==========

To run an instance of the EPM CSC::

    run_epm sal_index

The ``sal_index`` you specify must have a matching entry in the configuration you specify in the ``start`` command, else the command will fail.

This command-line script supports ``--help``.

Configuration
-------------

Configuration files are stored in `ts_config_ocs`_.

There should be one standard configuration file for each site.
Each configuration file specifies configuration for all EPM SAL indices supported at that site.
To run all EPM CSCs appropriate for a site, examine the configuration file and run one EPM CSC for each entry in it.

The EPM CSC uses "data clients" to communicate with PDUs and UPS-es via SNMP and publish the telemetry.
A CSC configuration file primarily contains of a list of sal_index: configuration for a data client.

.. _lsst.ts.epm-developer_guide:

Developer Guide
===============

Documentation for the PDUs and UPS-es is included in this project.

The EPM CSC is a subclass of the ESS CSC.
The ESS CSC defines the workings of the CSC.
A Subclass was created to override the configuration schema and to introduce deviations from the ESS CSC workings where necessary.

.. _lsst.ts.epm-api_reference:

Python API reference
--------------------

.. automodapi:: lsst.ts.epm
   :no-main-docstr:

.. _lsst.ts.epm-contributing:

Contributing
------------

``lsst.ts.epm`` is developed at https://github.com/lsst-ts/ts_epm.
You can find Jira issues for this module using `labels=ts_ess_csc <https://rubinobs.atlassian.net//issues/?jql=project%3DDM%20AND%20labels%3Dts_epm>`_.

Version History
===============

.. toctree::
    version_history
    :maxdepth: 1

.. _ts_config_ocs: https://github.com/lsst-ts/ts_config_ocs
.. _ts_ess_common: https://ts-ess-common.lsst.io
.. _ts_ess_controller: https://ts-ess-controller.lsst.io
.. _ts_ess_labjack: https://ts-ess-labjack.lsst.io
