from symeess.molecule.geometry import Geometry
from symeess.molecule.electronic_structure import ElectronicStructure
# import symmetry


class Molecule:

    def __init__(self, geometry, ee=None):

        if not geometry:
            print('No geometry found in the input file, check out for possible errors')
            exit()
        self._geometry = geometry
        self._name = geometry.get_name()
        if ee is not None:
            self._electronic_structure = ee

    def get_name(self):
        return self._name


    @property
    def geometry(self):
        return self._geometry

    @property
    def electronic_structure(self):
        return self._electronic_structure

    # def calculate_pointgroup(self):
    #     symmetry.get_pointgroup(self._geometry.get_symbols(), self._geometry.get_positions())