# dataExporter.py
"""
This module provides the base class for data export.
Classes (including widgets, etc.) should derive from it, probably along with
another class such as a Qt base class.
"""

from pynwb import NWBFile

class DataExporter:
    """
    Data export base class
    """

    def __init__(self):
        self.dataExportType = "None"  # derived class should override this

    def exportToNWBFile(self, nwbFile: NWBFile) -> NWBFile:
        raise NotImplementedError("Derived class needs to implement this")

    def exportToDict(self, d: dict):
        raise NotImplementedError("Derived class needs to implement this")