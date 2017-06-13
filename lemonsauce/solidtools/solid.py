import warnings

from numpy import array, zeros, ones, eye, any, concatenate, dot, arange, cross, interp, transpose, sum, sqrt
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
from .geom import implicit_line
from .obj import write_obj

from .slicer import slice_solid, get_edges

# Maximum number of points that hull calculation can be called on without pausing/warning
MAX_POINTS = 50

# This is used to interpret errors from scipy.optimize.linprog
opt_status_lookup = {
    0: "Optimization terminated successfully",
    1: "Iteration limit reached",
    2: "Problem appears to be infeasible",
    3: "Problem appears to be unbounded"
}

def extend(data: array, point: array):
    """Extends the colour solid in the direction we choose."""
    return concatenate((data, data + point), axis=0)


def compress(data: array):
    """ Returns only the points on the convex hull of the points given."""
    hull = ConvexHull(data)
    vertices = hull.vertices

    return hull.points[vertices, :]


def loop(data1d: array):
    """ make data into a loop """

    first = array([data1d[0]])

    return concatenate((data1d, first))


class ColourSolid:
    def __init__(self, curves: array, wavelengths: array = None, simplify_tolerance: float = 0.05, force_calculate: bool = False):
        """ A Colour Solid

        Args:
            curves (array): Fractional yield functions (sensitivity * illumination, need not be normalised)
            wavelengths (array or None): Specify the _wavelengths for the input curves, needed for calculating vividness
            simplify_tolerance (float): Pool groups of wavelength entries that add up to less than this value
            force_calculate (bool): Automatically calculate the values
        """

        # Expects a 2D array
        self.base_n_entries, self.n_dims = curves.shape
        self.base_curves = curves.copy()
        self._wavelengths = wavelengths

        if wavelengths is not None:
            if len(wavelengths) != self.base_n_entries:
                raise ValueError("Expected length of wavelengths (%i) to be the same as the input curves (%i)"
                                 % (len(wavelengths), self.base_n_entries))

        # normalise each curve to sum to one
        for i in range(self.n_dims):
            self.base_curves[:, i] /= sum(self.base_curves[:, i])

        # Create simplified version, where we take all parts
        # smaller than the tolerance and add them to the next bit
        # this will make the calculations much faster

        current_total = self.base_curves[0, :].copy()
        simplified_curves = []
        for i in range(1, self.base_n_entries):
            if any(current_total > simplify_tolerance):
                simplified_curves.append(current_total)
                current_total = self.base_curves[i, :].copy()
            else:
                current_total += self.base_curves[i, :]
        simplified_curves.append(current_total)

        self.curves = array(simplified_curves)
        self.n_points = len(simplified_curves)

        # Make sure this is declared
        self._hull_data = None


    @property
    def wavelengths(self):
        """ Wavelengths for which the fractional yield functions are specified"""
        return self._wavelengths

    @property
    def hull_data(self):
        """ Get the ConvexHull object representing the colour solid

        If it is a one dimensional solid, it will return None

        """

        if self._hull_data is None:

            if self.n_points > MAX_POINTS:
                warnings.warn("There are more than %i points in the fractional yield curves (%i). " % (
                MAX_POINTS, self.n_points) +
                              "\nLarge numbers can result in very long calculations" +
                              "\nEvaluation of the solid geometry is delayed until " +
                              "requested (via .calculate(), or though plot_on). " +
                              "\nThe geometry is not needed to calculate vividness." +
                              "\nConsider increasing the tolerance, " +
                              "or using a different method to calculate the solid.")

            self.calculate()

        return self._hull_data

    def calculate(self):
        """Calculate the solid"""

        print("Calculating %i-D solid from %i points (simplified from %i)" %
              (self.n_dims, self.n_points, self.base_n_entries))

        if self.n_dims == 1:
            return

        # Create the initial parallelepiped
        solid_data = zeros((1,self.n_dims), dtype=float)
        for i in range(self.n_dims):
            solid_data = extend(solid_data, self.curves[i, :])

        # Grow the solid, pruning using convex hull
        for i in range(self.n_dims, self.n_points):
            solid_data = extend(solid_data, self.curves[i, :])
            solid_data = compress(solid_data)

            # If there is lots of points, print the level
            if (self.n_points > MAX_POINTS):
                print(i)

        # Set the data
        self._hull_data = ConvexHull(solid_data)

    def write_obj(self, filename):
        """Write the solid to a file

        Args:
            filename (str): The file to output to
        """

        if self.n_dims == 2:

            # For 2D we need to pad the last dimension with zeros
            solid = self.hull_data
            verts = solid.points[solid.vertices, :]
            zero_row = zeros((len(verts), 1), dtype=float)

            verts = concatenate((verts, zero_row), axis=1)

            # There is one face, solid.points[solid.vertices, :] has put them in a circular order
            # the face indices are therefore just a list of the indices 0 to n-1
            faces = [[i for i in range(len(verts))]]

            # Now we can write the data
            write_obj(verts, faces, filename)

        elif self.n_dims == 3:
            # Reduce the points to vertices on the hull
            solid = self.hull_data
            hull_points = solid.points[solid.vertices, :]
            simplified_hull = ConvexHull(hull_points)

            verts = simplified_hull.points

            # We need to make sure the faces have the correct orientation
            # We use the fact that [0.5,0.5,0.5] is always in the middle
            centre = array([0.5, 0.5, 0.5])
            faces = []
            for face in simplified_hull.simplices:
                i1 = face[0]
                i2 = face[1]
                i3 = face[2]

                p1 = verts[i1, :]
                p2 = verts[i2, :]
                p3 = verts[i3, :]

                normal = cross(p1 - p3, p2 - p3)

                if dot(normal, p1-centre) > 0:
                    faces.append([i1, i2, i3])
                else:
                    faces.append([i3, i2, i1])

            # Now we can write the data
            write_obj(verts, faces, filename)

        else:
            raise ValueError("Only 2D and 3D solids can be writtoen to obj files.")

    def vividness(self, reflectance: array, wavelengths: array = None):
        """ Calculate the vividness of a given reflectance spectrum using this solid

        If _wavelengths are given, the reflectance will be linearly interpolated using them,
        otherwise, it is required that 'reflectance' be correspond to the same _wavelengths
        as the input curves.

        Args:
            reflectance (array): 1D array of reflectance values
            wavelengths (array): 1D array of _wavelengths or None

        Returns:
            the vividness of the reflectance according to this visual system
        """

        colour = self.colour(reflectance, wavelengths)

        return self.vividness_from_colour(colour)

    def colour(self, reflectance: array, wavelengths: array = None):
        """ Calculate normalised (fractional) quantum catches of a given reflectance.

        If _wavelengths are given, the reflectance will be linearly interpolated using them,
        otherwise, it is required that 'reflectance' be correspond to the same _wavelengths
        as the input curves.

        Args:
            reflectance (array): 1D array of reflectance values
            wavelengths (array): 1D array of _wavelengths or None

        Return:
            an array array containing normalised quantum catches associated with a reflectance
        """

        if wavelengths is None:
            if len(reflectance) != self.base_n_entries:
                raise ValueError(
                    "Reflectance should have the same number of entries as the curves (%i should be %i)"
                    % (len(reflectance), self.base_n_entries))

            r = reflectance

        else:
            if self._wavelengths is None:
                raise ValueError("No _wavelengths in Solid._wavelengths to interpolate with, "
                                 "either specify some when the solid is constructed, or, to "
                                 "avoid the interpolation attempt, do not specify them when"
                                 "calling Solid.vividness.")

            r = interp(wavelengths, self.wavelengths, reflectance)

        # Use the checked/calculated reflectance value to calculate the fractional catches
        catches = [dot(r, self.base_curves[:, i]) for i in range(self.n_dims)]

        return array(catches)

    def vividness_from_colour(self, colour):
        """ Calculate the vividness for normalised quantum catches,
        this uses a linear programming approach to find the points on the edge.

        Args:
            colour: an array of the normalised quantum catches representing a colour

        Returns:
            the vividness of the colour
        """

        d1 = sqrt(sum((colour-0.5)**2))
        d2 = self.boundary_distance(colour)

        return d1 / d2

    def boundary_distance(self, colour: array):
        """ Calculate distance for the centre of the solid to the boundary in the direction of a given colour

        Args:
            A colour for which the corresponding boundary point is to be found

        Returns:
            the distance to the boundary in the direction of the given colour

        """

        if sum(abs(colour - 0.5)) == 0:
            return 0.0

        boundary = self.boundary_colour(colour)
        return sqrt(sum((boundary - 0.5)**2))

    def boundary_colour(self, colour: array):
        """ Calculate the boundary colour associated with a point in the solid

        Args:
            colour (array): a point in the solid

        Returns:
            the corresponding colour on the boundary of the solid
        """

        return self.colour(self.boundary_spectrum(colour))

    def boundary_spectrum(self, colour: array):
        """ Calculate a spectrum on the boundary of the solid in the direction of a specified catch

        Args:
            colour (array): A point in the direction for which we want the boundary spectrum

        Returns:
            an array describing the extreme spectrum, its length matches the fractional yield functions'.

        """

        if sum(abs(colour - 0.5)) == 0:
            raise ValueError("Cannot get explicit boundary spectrum for centre of solid.")

        if len(colour.shape) != 1:
            raise ValueError("Expected parameter 'colour' to be a 1D array.")

        if self.n_dims != len(colour):
            raise ValueError("Expected parameter 'colour' to have %i entries" % self.n_dims)


        # set up the standard parameters for the numpy linprog solver

        c = -dot(self.base_curves, colour - 0.5)

        A_ub = concatenate((eye(self.base_n_entries), -eye(self.base_n_entries)))
        b_ub = concatenate((ones(self.base_n_entries), zeros(self.base_n_entries)))

        linear_constraint_m, linear_constraint_v = implicit_line(0.5 * ones(self.n_dims), colour)

        A_eq = dot(linear_constraint_m, transpose(self.base_curves))
        b_eq = linear_constraint_v

        result = linprog(c, A_ub, b_ub, A_eq, b_eq)

        if result.success:
            return result.x

        else:
            raise Exception("Optimisation failed: %s"%opt_status_lookup[result.status])

    def draw(self, projection=None, slices: bool=True, direction=(0, 0, 1), limit=True):
        """ Drawing process

            Args:
                projection: A two-by-n matrix that turns projects the points of the solid
                slices: If the solid is 3D, show slices in the direction specified by the direction parameter
                direction: direction perpendicular to which the solid will be slices
        """

        self.draw_on(plt_obj=None, projection=projection, slices=slices, direction=direction, limit=limit)

    def draw_on(self, plt_obj=None, projection=None, slices: bool=True, direction=(0, 0, 1), limit=True):
        """ Drawing process

        Args:
            projection: A two-by-n matrix that turns projects the points of the solid
            plt_obj: A matplotlib plot object on which to call .plot, if None, we make our own then call show at the end
            slices: If the solid is 3D, show slices in the direction specified by the direction parameter
            direction: direction perpendicular to which the solid will be slices
            """

        if plt_obj is None:
            import matplotlib.pyplot as plt
        else:
            plt = plt_obj

        #
        # Main plotting part, different routines for different dimensionalities
        #

        if self.n_dims == 1:

            # Just a line
            plt.plot([0.5, 0.5], [0.0, 1.0], 'k')

        else:

            s = self.hull_data
            v = s.vertices

            if self.n_dims == 2:

                # No projection needed, just show the outside
                p = s.points
                v = loop(v)
                plt.plot(p[v, 0], p[v, 1], 'k')

            else:

                if projection is None:
                    projection = zeros((self.n_dims, 2), dtype=float)
                    projection[0, 0] = 1.0
                    projection[1, 1] = 1.0

                if self.n_dims == 3:

                    # Set the default direction to be perpendicular to the main diagonal
                    if direction is None:
                        direction = [1, 1, 1]

                    # project according to the matrix provided,
                    # and slice it in the z direction

                    edges = array(get_edges(s.simplices))
                    if slices:
                        print("Slicing 3-D solid...")
                        k = 0.05
                        for z in arange(k/2.0, 1.0, k):

                            slice = slice_solid(s.points, array(edges), z, dir=direction)

                            if slice.shape[0] > 1:

                                solid2D = ConvexHull(slice[:, :2])
                                v = loop(solid2D.vertices)
                                p = solid2D.points

                                plt.fill(p[v, 0], p[v, 1], 'k', alpha=0.1)
                                plt.plot(p[v, 0], p[v, 1], 'k')

                    # main boundary
                    solid2D = ConvexHull(s.points[:, :2])
                    v = loop(solid2D.vertices)
                    p = solid2D.points

                    plt.plot(p[v, 0], p[v, 1], 'k')

                else:
                    # Just plot the extremities of the solid
                    prj = dot(s.points, projection)
                    solid2D = ConvexHull(prj)
                    v = loop(solid2D.vertices)
                    p = solid2D.points

                    plt.plot(p[v, 0], p[v, 1])

        #
        # Plot limits
        #
        if limit:
            plt.xlim([0, 1])
            plt.ylim([0, 1])

        #
        # Finally, if we created the plot here, show it
        #

        if plt_obj is None:
            plt.show()


