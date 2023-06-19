# Blender off-axis projection

![Demo](demo.gif)

One can fit arbitrary rectangular plane to a given camera without changing camera location,
but only by changing rotation, lens size and shift.

The script `off-axis-projection.py` does that.

It corresponds to manipulating [tilt-shift](https://en.wikipedia.org/wiki/Tilt%E2%80%93shift_photography) lenses in real life.

Applications of off-axis rendering include:
- Computer games; see [Portal](https://en.wikipedia.org/wiki/Portal_(video_game))
- Immersive virtual reality; see [CAVE](https://en.wikipedia.org/wiki/Cave_automatic_virtual_environment)

Keywords: Off-axis projection, Oblique projection, tilt-shift lens

## How to use

1. Open the blender file you want to use
2. Make a plane object to fit the plane of your interest (NOTE: plane aspect ratio should be identical to render aspect ratio!)
3. Go to `scripting/Text Editor` pane
4. Create a new file and copy paste the content of `off-axis-projection.py`
5. In last line, replace `"CameraName"` and `"RectangleName"` to the name of your camera and plane respectively.
6. Run script by pressing `Run Script`
7. ???
8. Profit!
