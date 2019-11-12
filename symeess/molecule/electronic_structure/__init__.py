import numpy as np


class ElectronicStructure:
    def __init__(self,
                 charge=0,
                 multiplicity=1,
                 basis=None,
                 orbital_coefficients=None):

        self._charge = charge
        self._multiplicity = multiplicity
        self._basis = basis
        # self._Ca = [float(x) for x in orbital_coefficients[0]]
        self._Ca = np.array(orbital_coefficients[0], dtype=np.float64)
        if not orbital_coefficients[1]:
            self._Cb = None
        else:
            self._Cb = np.array(orbital_coefficients[1], dtype=np.float64)

    @property
    def charge(self):
        return self._charge

    @property
    def multiplicity(self):
        return self._multiplicity

    @property
    def basis(self):
        return self._basis

    @property
    def coefficients_a(self):
        return self._Ca

    @property
    def coefficients_b(self):
        return self._Cb
