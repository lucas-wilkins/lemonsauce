from numpy import array


def write_obj(vertices: array, face_list: list, filename: str):
    """ Writes an object specified by vertices and face indices to an OBJ file

    Args:
        vertices: A n-by-3 list of vertices
        face_list: A list of the face indices (0 indexed)
        filename: Output filename

    """

    n_verts = vertices.shape[0]
    n_faces = len(face_list)

    fid = open(filename, 'w')

    for i in range(n_verts):
        fid.write("v %g %g %g\n" % (vertices[i, 0], vertices[i, 1], vertices[i, 2]))

    for i in range(n_faces):
        fid.write("f")
        for index in face_list[i]:
            fid.write(" %i" % (index+1))
        fid.write("\n")

    fid.close()
