# generate_diff_mask

A python script that generates a chroma-keyed difference image between an original and an (typically) inpainted image, intended for image tracing in Adobe Illustrator and similar software.

Input/output is assumed to be RGB24 PNG.

### Requirements

- [Vapoursynth](https://github.com/vapoursynth/vapoursynth/releases) (tested on R70+)

### Settings

`--source path_to_file`

Path to original image.

`--target path_to_file`

Path to inpainted image, defaults to `{source}_cleanup.png` if not specified.

`--output path_to_file`

Path to output image, defaults to `{source}_diff.png` if not specified.

`--color r g b`

Color to use for the chroma keying, specified as an RGB24 tuple, defaults to `0 255 0` (pure green) if not specified.
