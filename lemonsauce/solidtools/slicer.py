from numpy import array, sum, dot, transpose, reshape
from .geom import expand_simplex

def edge_cmp(e1, e2):
    """ A comparitor which gives a unique ordering to pairs of numbers"""
    if e1[0] == e2[0]:
        if e1[1] == e2[1]:
            return 0
        else:
            return 1 if e1[1] > e2[1] else -1
    else:
        return 1 if e1[0] > e2[0] else -1


def get_edges(simplex_data: array):
    """Extracts edge data from simplex data

    Args:
        simplex_data: n-by-m Array containing m lists of indices of points forming an n-simplex

    Returns:
        List of index pairs of edges
    """

    #
    # Calculate the edges
    #

    n_simps, n_dims_plus_one = simplex_data.shape
    edge_data = []
    for i in range(n_simps):
        edge_data += expand_simplex(simplex_data[i, :])

    #
    # Remove duplicates
    #

    edge_data.sort()
    out_data = edge_data[:1]
    for i in range(1, len(edge_data)):
        if edge_cmp(edge_data[i-1], edge_data[i]) != 0:
            out_data.append(edge_data[i])

    return out_data


def slice_solid(points: array, edges: array, z: float, dir=[0, 0, 1]):
    """ Slice a 3D shape along a given z direction

    Args:
        points: list of points describing on the shape
        edges: list of index pairs to 'points' specifying the edges
        z: distance from (0,0,0) at which to slice
        dir: direction in which to measure slice (equally, signed vector normal to slice)

    Returns:
        list of points lying on a slice of the shape (does not calculate edges for them, or order them)
    """

    direction = transpose(array([array(dir, dtype=float) / sum(dir)]))
    zs = dot(points, direction).flat

    n_edges = edges.shape[0]

    output_data = []
    for i in range(n_edges):
        i0 = edges[i, 0]
        i1 = edges[i, 1]
        z1 = zs[i0]
        z2 = zs[i1]

        # Set crosser to true if the z positions straddle the input z
        crosser = False
        if z1 < z:
            if z < z2:
                crosser = True
        else:
            if z > z2:
                crosser = True

        # Find the point where it crosses the z axis,
        # this is essentially just similar triangles
        if crosser:
            f = abs(z-z1)/abs(z2-z1)
            p = f*points[i1, :] + (1-f)*points[i0, :]
            output_data.append(p)

    # print("Sliced though of %i edges (of %i total)" % (len(output_data), n_edges))

    return reshape(array(output_data), (len(output_data), points.shape[1]))




