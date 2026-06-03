import atheris
import sys

with atheris.instrument_imports():
    import sympy as sp


@atheris.instrument_func
def TestOneInput(data):

    fdp = atheris.FuzzedDataProvider(data)

    x = sp.Symbol("x")
    y = sp.Symbol("y")

    expr = x

    num_ops = fdp.ConsumeIntInRange(1, 10)

    for _ in range(num_ops):

        if not fdp.remaining_bytes():
            break

        op = fdp.ConsumeIntInRange(0, 7)

        const = fdp.ConsumeIntInRange(-100, 100)

        try:

            if op == 0:
                expr = expr + const

            elif op == 1:
                expr = expr - const

            elif op == 2:
                expr = expr * const

            elif op == 3:
                expr = expr ** 2

            elif op == 4:
                expr = sp.sin(expr)

            elif op == 5:
                expr = sp.cos(expr)

            elif op == 6:
                expr = sp.exp(expr)

            elif op == 7:
                expr = sp.log(abs(expr) + 1)

        except Exception:
            pass

    try:
        sp.simplify(expr)
    except Exception:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()