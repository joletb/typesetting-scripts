from pathlib import Path
from vapoursynth import core
import argparse
import vapoursynth as vs

parser = argparse.ArgumentParser()
parser.add_argument('--source', dest='source', required=True)
parser.add_argument('--target', dest='target', required=False)
parser.add_argument('--color', dest='color', nargs=3, required=False, default=[0, 255, 0])
parser.add_argument('--output', dest='output', required=False)

args = parser.parse_args()

if args.target == None:
    args.target = f'{Path(args.source).stem}_cleanup.png'

if args.output == None:
    args.output = f'{Path(args.source).stem}_diff.png'

source_image = core.imwri.Read(f'{args.source}')
target_image = core.imwri.Read(f'{args.target}')

diff = core.std.Expr(clips=[source_image, target_image], expr='x y - abs')

binarized_diff = core.std.Binarize(clip=diff, threshold=1)

binarized_diff_r = core.std.ShufflePlanes(clips=[binarized_diff], planes=[0], colorfamily=vs.GRAY)
binarized_diff_g = core.std.ShufflePlanes(clips=[binarized_diff], planes=[1], colorfamily=vs.GRAY)
binarized_diff_b = core.std.ShufflePlanes(clips=[binarized_diff], planes=[2], colorfamily=vs.GRAY)

binarized_diff_m = core.std.Expr([binarized_diff_r, binarized_diff_g, binarized_diff_b], 'x y z + +')

# Fill in any holes in the mask so the output is more cohesive
binarized_diff = binarized_diff_m.std.Maximum().std.Maximum().std.Minimum().std.Minimum()

chroma_key = core.std.BlankClip(width=source_image.width, height=source_image.height, format=source_image.format, length=source_image.num_frames,
                               fpsnum=source_image.fps_num, fpsden=source_image.fps_den, color=args.color)

final_merge = core.std.MaskedMerge(chroma_key, target_image, binarized_diff)

if __name__ == "__main__":
    output = core.imwri.Write(final_merge, imgformat='PNG', filename=f'{args.output}', overwrite=True)
    output.get_frame(0)
