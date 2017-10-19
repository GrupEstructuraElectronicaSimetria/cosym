import os
import sys
from itertools import islice
from molecule import Molecule


def read(input_name):

    file_name, file_extension = os.path.splitext(input_name)
    method_name = 'read_file_' + file_extension[1:]
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % method_name)

    return method(input_name)


def read_file_xyz(file_name):
    with open(file_name, mode='r') as lines:
        molecules = []

        while True:
            try:
                input_molecule = []
                n_atoms = int(lines.readline())
                name = lines.readline().split()[0]
                for line in list(islice(lines, n_atoms)):
                    input_molecule.append(line.split())
                molecules.append(Molecule(structure=input_molecule, name=name))
            except ValueError:
                return molecules


def read_file_cor(file_name):
    with open(file_name, mode='r') as lines:
        input_molecule = []
        molecules = []
        name = lines.readline().split()[0]
        for line in lines:
            try:
                float(line.split()[1])
                input_molecule.append(line.split()[:-1])
            except ValueError:
                molecules.append(Molecule(structure=input_molecule, name=name))
                input_molecule = []
                name = line.split()[0]
        molecules.append(Molecule(structure=input_molecule, name=name))

        return molecules


# def write(output_name, data):
#
#     output = open(output_name, 'w') if output_name else sys.stdout
#
#     output.write('-'*40 + '\n')
#     output.write('{}'.format('END of CALCULATION'.rjust(26)))
#     output.close()


def write_shape(output_name, data, shape_label, molecule_names):

    output = open(output_name, 'w') if output_name else sys.stdout
    options = sorted(list(data[0][shape_label[0]].keys()))

    output.write('-'*40 + '\n')
    output.write('Shape measure/s \n')
    output.write('-'*40 + '\n')

    if 'measure' in options:
        output.write("{} {}\n".format('measure'.upper(),'   '.join(shape_label)))
        for idx, molecule in enumerate(data):
            output.write('{}'.format(molecule_names[idx]))
            for label in shape_label:
                output.write(' {:4.3f}'.format(molecule[label]['measure']))
            output.write('\n')
        output.write('\n')

    if 'ideal_structure' in options:
        output.write("{}\n".format('ideal_structure'.upper()))
        for idx, molecule in enumerate(data):
            output.write('\n')
            output.write('{}'.format(molecule_names[idx]))
            n = 18
            for label in shape_label:
                output.write('{}'.format(label.rjust(n)))
                n += 21
            output.write('\n')

            for idn, symbol in enumerate(molecule['symbols']):
                output.write('{:3s}'.format(molecule['symbols'][idn]))
                for label in shape_label:
                    array = molecule[label]['ideal_structure'][idn]
                    output.write(' {:11.7f} {:11.7f} {:11.7f} |'.format(array[0], array[1], array[2]))
                output.write('\n')

        output.write('\n')

    if 'test_structure' in options:
        output.write("{}\n".format('test_structure'.upper()))
        n = 21
        for label in shape_label:
            output.write('{}'.format(label.rjust(n)))
            n += 18
        output.write('\n')

        for idx in list(range(len(data[0]['symbols']))):
            for label in shape_label:
                array = data[0][label]['test_structure'][idx]
                output.write(' {:11.7f} {:11.7f} {:11.7f} |'.format(array[0], array[1], array[2]))
            output.write('\n')

    output.write('-'*40 + '\n')
    output.write('-'*40 + '\n')
    output.close()
