#!/usr/bin/python3

import sys
import atheris

with atheris.instrument_imports():
    import sympy as sp


def generate_expr(fdp, depth, x, y):
    """
    Recursively generate a SymPy expression tree.
    """

    if depth <= 0:

        leaf_type = fdp.ConsumeIntInRange(0, 7)

        if leaf_type == 0:
            return x

        elif leaf_type == 1:
            return y

        elif leaf_type == 2:
            return sp.Integer(0)

        elif leaf_type == 3:
            return sp.Integer(1)

        elif leaf_type == 4:
            return sp.Integer(-1)

        elif leaf_type == 5:
            return sp.pi

        elif leaf_type == 6:
            return sp.E

        else:
            return sp.Integer(
                fdp.ConsumeIntInRange(-10, 10)
            )

    op = fdp.ConsumeIntInRange(0, 9)

    try:

        if op == 0:
            return (
                generate_expr(fdp, depth - 1, x, y)
                +
                generate_expr(fdp, depth - 1, x, y)
            )

        elif op == 1:
            return (
                generate_expr(fdp, depth - 1, x, y)
                *
                generate_expr(fdp, depth - 1, x, y)
            )

        elif op == 2:
            base = generate_expr(
                fdp,
                depth - 1,
                x,
                y
            )

            exponent = fdp.ConsumeIntInRange(
                0,
                4
            )

            return base ** exponent

        elif op == 3:
            return sp.sin(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )
            )

        elif op == 4:
            return sp.cos(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )
            )

        elif op == 5:
            return sp.exp(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )
            )

        elif op == 6:
            expr = generate_expr(
                fdp,
                depth - 1,
                x,
                y
            )

            return sp.log(
                expr**2 + 1
            )

        elif op == 7:
            return sp.sqrt(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )**2
                +
                1
            )

        elif op == 8:
            return sp.tan(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )
            )

        else:
            return sp.Abs(
                generate_expr(
                    fdp,
                    depth - 1,
                    x,
                    y
                )
            )

    except Exception:
        return x


@atheris.instrument_func
def TestOneInput(data):

    fdp = atheris.FuzzedDataProvider(data)

    x = sp.Symbol("x")
    y = sp.Symbol("y")

    try:

        depth = fdp.ConsumeIntInRange(
            1,
            8
        )

        expr = generate_expr(
            fdp,
            depth,
            x,
            y
        )

        #
        # Differential Oracle
        #

        r1 = sp.simplify(expr)

        r2 = sp.factor(
            sp.expand(expr)
        )

        #
        # Numerical equivalence check
        #

        v1 = (
            r1
            .subs(x, 2)
            .subs(y, 3)
            .evalf()
        )

        v2 = (
            r2
            .subs(x, 2)
            .subs(y, 3)
            .evalf()
        )

        if (
            v1.is_real
            and
            v2.is_real
        ):

            diff = abs(
                float(v1)
                -
                float(v2)
            )

            if diff > 1e-6:

                raise AssertionError(
                    f"""
Differential Failure

expr:
{expr}

simplify:
{r1}

factor(expand):
{r2}

v1={v1}
v2={v2}
"""
                )

    except (
        ValueError,
        ZeroDivisionError,
        OverflowError,
        TypeError
    ):
        pass

    except Exception:
        raise


def main():

    atheris.Setup(
        sys.argv,
        TestOneInput
    )

    atheris.Fuzz()


if __name__ == "__main__":
    main()