USER_FUN = ("x^2 + 3y^2 + 2xy",
            "100(y-x^2)^2 + (1-x)^2",
            "-12y + 4(x^2 + y^2) + - 4xy",
            "(x-2)^4 + (x-2y)^2",
            "4(x - 5)^2 + (y - 6)^2",
            "(y - x^2)^2 + 100(1 - x)^2",
            "2x^3 + 4xy^3 - 10xy + y^2",
            "8x^2 + 4xy + 5x^2",
            "x^3 + y^2 - 5y + 2")


def function_1(x, y):
    return x**2 + 3*y**2 + 2*x*y


def function_2(x, y):
    return 100*(y - x**2)**2 + (1 - x)**2


def function_3(x, y):
    return -12*y + 4*(x**2 + y**2) - 4*x*y


def function_4(x, y):
    return (x - 2)**4 + (x - 2 * y) ** 2


def function_5(x, y):
    return 4*(x - 5)**2 + (y - 6)**2


def function_6(x, y):
    return (y - x**2)**2 + 100*(1 - x)**2


def function_7(x, y):
    return 2*x**3 + 4*x*y**3 - 10*x*y + y**2


def function_8(x, y):
    return 8*x**2 + 4*x*y + 5*x**2


def function_9(x, y):
    return x**3 + y**2 - 5*y + 2


functions_arr = (function_1, function_2, function_3,
                 function_4, function_5, function_6,
                 function_7, function_8, function_9)
