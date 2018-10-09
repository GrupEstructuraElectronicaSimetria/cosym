from symeess import shape, tools
from symeess.symmetry import symgroup
import numpy as np
import hashlib


class Geometry:
    def __init__(self,
                 symbols=None,
                 positions=None,
                 name=None):

        self._central_atom = None
        self._path_deviation = {}
        self._GenCoord = {}
        self._symbols = []
        self._positions = []

        if name is not None:
            self._name = name
        else:
            self._name = ' ' * 5

        for element in symbols:
            try:
                int(element)
                self._symbols.append(tools.atomic_number_to_element(int(element)))
            except (ValueError, TypeError):
                self._symbols.append(element.capitalize())
                for ida, a in enumerate(element):
                    try:
                        int(a)
                        self._symbols[-1] = self._symbols[-1][:ida]
                        break
                    except (ValueError, TypeError, IndexError):
                        pass

        try:
            float(positions[0])
            for element in positions:
                self._positions.append(float(element))
            self._positions = list(chunks(self._positions, 3))
        except (ValueError, TypeError, IndexError):
            for element in positions:
                self._positions.append([float(j) for j in element])

        self._positions = np.array(self._positions)
        self._shape = shape.Shape(self)
        self._symgroup = symgroup.Symgroup(self)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_positions(self):
        return self._positions

    def get_n_atoms(self):
        return len(self.get_positions())

    def get_symbols(self):
        return self._symbols

    def get_shape_measure(self, shape_label, central_atom=0):
        return self._shape.measure(shape_label,
                                   central_atom=central_atom)

    def get_shape_structure(self, shape_label, central_atom=0):
        return self._shape.structure(shape_label,
                                     central_atom=central_atom)

    def get_symmetry_measure(self, label, central_atom=0, multi=None):
        return self._symgroup.results(label, central_atom=central_atom, multi=multi)

    def get_path_deviation(self, shape_label1, shape_label2, central_atom):
        hash = hashlib.md5('{}{}{}'.format(shape_label1, shape_label2, central_atom).encode()).hexdigest()
        if hash not in self._path_deviation:
            Sx = self.get_shape_measure(shape_label1, central_atom)
            Sy = self.get_shape_measure(shape_label2, central_atom)
            self._path_deviation[hash] = shape.shape_tools.get_path_deviation(Sx, Sy, shape_label1, shape_label2,
                                                                              central_atom)
        return self._path_deviation[hash]

    def get_generalized_coordinate(self, shape_label1, shape_label2, central_atom):
        hash = hashlib.md5('{}{}{}'.format(shape_label1, shape_label2, central_atom).encode()).hexdigest()
        # if shape_label1+'_'+shape_label2 not in self._GenCoord:
        #     if shape_label2+'_'+shape_label1 not in self._GenCoord:
        #         labels = shape_label1+'_'+shape_label2
        #         self._GenCoord[labels] = None
        #     else:
        #         labels = shape_label2 + '_' + shape_label1
        # else:
        #     labels = shape_label1 + '_' + shape_label2
        if hash not in self._GenCoord:
            Sq = self.get_shape_measure(shape_label1, central_atom)
            self._GenCoord[hash] = shape.shape_tools.get_generalized_coordinate(Sq, shape_label1, shape_label2,
                                                                                central_atom)
        return self._GenCoord[hash]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
