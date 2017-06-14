""" Geometry helper functions """

from numpy import array, eye, argmax, concatenate


def sort_pair(a, b):
    if a > b:
        return [b, a]
    else:
        return [a, b]


def expand_simplex(simplex: array):
    """Takes a list of indices representing a simplex and returns all the edges

    Args:
        simplex: Array (or list) of indices describing a simplex e.g. array([1,2,6]) for a triangle

    Returns:
        Ordered edges ([smallest, biggest]) in the simplex as a list e.g. [[1,2],[1,6],[2,6]]

    """

    n = len(simplex)

    if n > 1:
        start = simplex[0]
        out = []
        for i in range(1, n):
            out.append(sort_pair(start, simplex[i]))

        return out + expand_simplex(simplex[1:])
    else:
        return []


# Key mapping used for removing duplicates
# It means that all permutations are equivalent
def simplex_duplicate_key(simplex: array):
    return tuple(sorted(simplex))

def remove_duplicates(simplex_list: list):
    """ Remove duplicate simplicies from a list of indices

    """

    # if we can put the indices into canonical order, then we just have to sort
    # We could use list(set()), but that would loose the ordering

    s = sorted(simplex_list, key=simplex_duplicate_key)

    out = [s[0]]
    last_key = simplex_duplicate_key(s[0])

    for entry in s:
        this_key = simplex_duplicate_key(entry)
        if this_key != last_key:
            out.append(entry)
            last_key = this_key

    return out


def lower_simplex_order(simplex: array):
    """ Converts a n-simplex to its n+1 component (n-1)-simplices

    For example, it will convert a tetrahedron (a 3-simplex) into 4 triangles (2-simplices)

    Args:
        simplex (array): an array containing n+1 references describing an n simplex
    Returns:
        a list of (n-1)-simplices described by length n arrays

    """

    # Simply skip each entry in turn
    return [concatenate((simplex[:i], simplex[i+1:]))
            for i in range(len(simplex))]


def implicit_line(p: array, q: array):
    """ Get an implicit representation of line of the form Ax=b


    It takes two points, p and q as input.
    The parametric form of the line being x = p + k(q-p) = p + kr


    Algorithm works as follows
    ==========================

    The parametric form can be written like this (3D example)

      / 1 0 0 \ / x_0 \     / p_0 \     / r_0 \
      | 0 1 0 | | x_1 |  =  | p_1 | + k | r_1 |
      \ 0 0 1 / \ x_2 /     \ p_2 /     \ r_2 /

    Then, we pick a row for which (r_i) is non-zero (choose the biggest magnitude)
    and then solve for k. For it to describe a line, at least one entry must be non-zero
    Call the chosen row the pivot row.

      k = (x_pivot - p_pivot) / (r_pivot)

    The rows of the right hand side of the parametric form become

       x_pivot (r_i / r_pivot) + p_i - (p_pivot / r_pivot) r_i
      \______________________/  \____________________________/
          x_pivot term                constant term

    We can see that when i=pivot, the x_pivot term has a coefficient of 1 and
    the constant term is zero. Thus the x_pivot row is now clearly
    redundant being

       x_pivot = 1 x_pivot + 0

    So, we remove the pivot row from the equation. For example, if the pivot row is
    at index 1 then, we have

        / 1 0 0 \ / x_0 \     x_1 (r_0 / r_1) + p_0 - (p_1 / r_1) r_0
        | - - - | | x_1  |  =                  ---
        \ 0 0 1 / \ x_2 /     x_1 (r_2 / r_1) + p_2 - (p_1 / r_1) r_2

    The final step, then, is to move the x_pivot term from the right into the matrix.

        / 1 (r_0 / r_1) 0 \   / x_0 \     / p_0 - (p_1 / r_1) r_0 \
        \ 0 (r_2 / r_1) 1 /   | x_1 |  =  \ p_2 - (p_1 / r_1) r_2 /
                              \ x_2 /

    We apply a general formula to this effect.

    Args:
        p (array_like): one point on the line
        q (array_like): another point on the line

    Returns:
        The tuple (A, b), matrix and vector, for the equation Ax=b describing the line
    """

    if len(p.shape) != 1:
        raise ValueError("p should be a vector")

    if len(q.shape) != 1:
        raise ValueError("q should be a vector")

    n_dims = len(p)

    if len(q) != n_dims:
        raise ValueError("p and q should have the same size")

    # Find the pivot row
    r = q - p
    pivot = argmax(abs(r))

    if r[pivot] == 0:
        raise ValueError("p and q do not describe a line, because p=q.")

    # Create the matrix
    A = eye(n_dims)
    A[:, pivot] = -r / r[pivot]
    A = concatenate((A[:pivot, :], A[pivot+1:, :]), axis=0)

    # Create the vector
    b = p - ((p[pivot] / r[pivot]) * r)
    b = concatenate((b[:pivot], b[pivot+1:]))

    return A, b


if __name__ == "__main__":
    # Test the implicit_line function

    from numpy import arange, dot

    p = array([1, 2, 3, 4], dtype=float)
    q = array([3, 5, 8, 3], dtype=float)

    other = array([9, 1, 1, 2], dtype=float)

    A, b = implicit_line(p, q)

    def check(x, y):
        if x >= y:
            raise Exception("Expected %s < %s" % (str(x), str(y)))

    for k in arange(0, 3, 0.3):
        x = p + k*(q - p)
        test_value = dot(A, x) - b
        check(sum(abs(test_value)), 1e-10)

    for k in arange(0, 3, 0.3):
        x = other + k * (q - p)
        test_value = dot(A, x) - b
        check(1e-10, sum(abs(test_value)))

    for k in arange(1, 4, 0.3):
        x = p + k * (other - p)
        test_value = dot(A, x) - b
        check(1e-10, sum(abs(test_value)))
