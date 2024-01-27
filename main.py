import pickle

import extract_gates


def extract_and_save_gates(filename):
    gates = extract_gates.extract()
    with open(filename, "wb") as file:
        pickle.dump(gates, file)


def load_gates(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


gate_file = "gates01.ming"


if __name__ == '__main__':
    # generate.parse_circuit_file("circuits/basic_gates.circ")
    extract_and_save_gates(gate_file)
