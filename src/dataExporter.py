# dataExporter.py
"""
This module provides the base class for data export.
Classes (including widgets, etc.) should derive from it, probably along with
another class such as a Qt base class.
"""

from h5py import File

class DataExporter:
    """
    Data export base class
    """

    def __init__(self, id: int):
        """
        The combination (self.dataExportType, self.id) should be unique.
        """
        self.dataExportType = "None"  # derived class should override this
        self.id: int = id

    def exportToH5File(self, openH5File: File):
        raise NotImplementedError("Derived class needs to implement this")

    def exportToDict(self, d: dict):
        raise NotImplementedError("Derived class needs to implement this")