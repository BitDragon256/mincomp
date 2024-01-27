import extract_gates


if __name__ == '__main__':
    # generate.parse_circuit_file("circuits/basic_gates.circ")
    gates = extract_gates.extract()
    print(gates)
