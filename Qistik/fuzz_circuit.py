#!/usr/bin/python3
import sys
import atheris

with atheris.instrument_imports():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator


@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    # 1~3 qubits
    num_qubits = fdp.ConsumeIntInRange(1, 3)

    qc = QuantumCircuit(num_qubits)

    # 1~5 operations
    num_ops = fdp.ConsumeIntInRange(1, 5)

    for _ in range(num_ops):

        if fdp.remaining_bytes() == 0:
            break

        gate_type = fdp.ConsumeIntInRange(0, 7)

        qubit = fdp.ConsumeIntInRange(0, num_qubits - 1)

        try:

            # X
            if gate_type == 0:
                qc.x(qubit)

            # Y
            elif gate_type == 1:
                qc.y(qubit)

            # Z
            elif gate_type == 2:
                qc.z(qubit)

            # H
            elif gate_type == 3:
                qc.h(qubit)

            # RX
            elif gate_type == 4:
                theta = fdp.ConsumeFloat()
                qc.rx(theta, qubit)

            # RY
            elif gate_type == 5:
                theta = fdp.ConsumeFloat()
                qc.ry(theta, qubit)

            # CX
            elif gate_type == 6 and num_qubits >= 2:

                control = fdp.ConsumeIntInRange(
                    0,
                    num_qubits - 1
                )

                target = fdp.ConsumeIntInRange(
                    0,
                    num_qubits - 1
                )

                if control != target:
                    qc.cx(control, target)

            # CZ
            elif gate_type == 7 and num_qubits >= 2:

                control = fdp.ConsumeIntInRange(
                    0,
                    num_qubits - 1
                )

                target = fdp.ConsumeIntInRange(
                    0,
                    num_qubits - 1
                )

                if control != target:
                    qc.cz(control, target)

        except Exception:
            pass

    simulator = AerSimulator()

    try:
        simulator.run(qc).result()
    except Exception:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()