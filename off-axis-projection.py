# https://web.archive.org/web/20191110002841/http://csc.lsu.edu/~kooima/articles/genperspective/index.html
# https://github.com/mrdoob/three.js/pull/21825
from typing import Tuple

import bpy
from mathutils import Matrix, Vector


def get_lens_shift(
    camera,
    bottom_left, bottom_right, top_left,
    resx, resy,
) -> Tuple["Matrix", float, Tuple[float, float]]:
    """
    Given a camera and a rectangle, find camera parameters that
    the sensor aligns exactly to contain the plane.

    Args:
        camera:            blender object that contains camera data
        bottom_left:       plane parameter
        bottom_right:      plane parameter
        top_left:          plane parameter
        resx:              resolution of sensor (horizontal)
        resy:              resolution of sensor (vertical)

    Returns:
        "Matrix":            camera extrinsic matrix
        float:               lens size
        Tuple[float, float]: sensor x shift, sensor y shift
    """
    # finding extrinsic parameter =======================================================
    # prepare unit vectors in plane coordinates
    vr = bottom_right - bottom_left
    vu = top_left     - bottom_left
    vr.normalize()
    vu.normalize()
    assert vr.dot(vu) < 1e-7, "Given points does not form right triangle"
    vn = vr.cross(vu)
    vn.normalize()

    # describe the plane as in near plene
    va = bottom_left  - camera.location
    vb = bottom_right - camera.location
    vc = top_left     - camera.location
    d = - va.dot(vn)
    l = vr.dot(va) * camera.data.clip_start / d
    r = vr.dot(vb) * camera.data.clip_start / d
    b = vu.dot(va) * camera.data.clip_start / d
    t = vu.dot(vc) * camera.data.clip_start / d
    del va, vb, vc, d

    # Set the camera rotation to match the focal plane to the corners' plane
    # align up vector
    quat_u = Vector((0, 1, 0)).rotation_difference(vu)
    # align near vector
    quat_n_after_u = (quat_u @ Vector((0, 0, 1))).rotation_difference(vn)
    del vn, vu, vr

    # Now we have the extrinsic rotation matrix!
    mat = (quat_n_after_u @ quat_u).to_matrix().to_4x4()
    mat.translation = camera.location
    del quat_u, quat_n_after_u
    # finding extrinsic parameter done ==================================================
    # at this point, camera projection plane is parallel to the plane
    # now set the off-axis projection matrix to match the sensor's corners

    # making of intrinsic matrix
    xasp = yasp = 1
    ycor = yasp / xasp

    # decide sensorfit
    if camera.data.sensor_fit == 'AUTO':
        sensor_fit = ('HORIZONTAL' if (xasp * resx >= yasp * resy) else 'VERTICAL')
    else:
        sensor_fit = camera.data.sensor_fit
    viewfac = resx if (sensor_fit == 'HORIZONTAL') else ycor * resy

    if (camera.data.type == 'ORTHO'):
        lens = None
    else:
        sensor_size = camera.data.sensor_height if (sensor_fit == 'VERTICAL') else camera.data.sensor_width
        lens = (sensor_size * camera.data.clip_start) / viewfac * resx / (r - l)

    assert abs(abs((r - l) / resx) - abs((t - b) / ycor / resy)) < 1e-7, "Computation is broken"
    shift_x = resx * (l + r) / (r - l) / 2 / viewfac
    shift_y = resy * (t + b) / (t - b) * ycor / viewfac / 2
    return mat, lens, (shift_x, shift_y)

def update(camera_name: str, plane_name: str):
    """
    Update camera's rotation and parameters so that it aligns exactly to a plane
    It is assumed that the vertices of mesh of the rect is bottom-left, bottom-right, top-left, top-right
    """
    camera = bpy.data.objects[camera_name]
    plane = bpy.data.objects[plane_name]

    assert len(plane.data.vertices) == 4
    vs = plane.data.vertices[:3]
    bl, br, tl = [plane.matrix_world @ v.co for v in vs]

    resx, resy = bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y

    mat, lens, (shift_x, shift_y) = get_lens_shift(
        camera,
        bl, br, tl,
        resx, resy,
    )
    camera.data.type == 'PERSP'
    camera.matrix_basis = mat
    camera.data.lens = lens
    camera.data.shift_x = shift_x
    camera.data.shift_y = shift_y


update("CameraName", "RectangleName")
