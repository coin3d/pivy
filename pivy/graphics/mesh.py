from pivy import coin
from .colors import COLORS
import numpy as np


def simple_quad_mesh(points, num_u, num_v, colors=None):
    msh_sep = coin.SoSeparator()
    msh = coin.SoQuadMesh()
    vertexproperty = coin.SoVertexProperty()
    vertexproperty.vertex.setValues(0, len(points), points)
    msh.verticesPerRow = num_u
    msh.verticesPerColumn = num_v
    if colors:
        vertexproperty.materialBinding = coin.SoMaterialBinding.PER_VERTEX
        for i in range(len(colors)):
            vertexproperty.orderedRGBA.set1Value(i, coin.SbColor(colors[i]).getPackedValue())
    msh.vertexProperty = vertexproperty

    shape_hint = coin.SoShapeHints()
    shape_hint.vertexOrdering = coin.SoShapeHints.COUNTERCLOCKWISE
    shape_hint.creaseAngle = np.pi / 3
    msh_sep += [shape_hint, msh]
    return msh_sep


def simple_poly_mesh(verts, poly, color=None):
    color = color or COLORS["grey"]
    _vertices = [list(v) for v in verts]
    _polygons = []
    for pol in poly:
        _polygons += list(pol) + [-1]
    sep = coin.SoSeparator()
    vertex_property = coin.SoVertexProperty()
    face_set = coin.SoIndexedFaceSet()
    shape_hint = coin.SoShapeHints()
    shape_hint.vertexOrdering = coin.SoShapeHints.COUNTERCLOCKWISE
    shape_hint.creaseAngle = np.pi / 3
    face_mat = coin.SoMaterial()
    face_mat.diffuseColor = color
    vertex_property.vertex.setValues(0, len(_vertices), _vertices)
    face_set.coordIndex.setValues(0, len(_polygons), list(_polygons))
    vertex_property.materialBinding = coin.SoMaterialBinding.PER_VERTEX_INDEXED
    sep += [shape_hint, vertex_property, face_mat, face_set]
    return sep

