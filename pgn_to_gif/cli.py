from typing import Literal, Optional, Sequence
import argparse
from pathlib import Path
from .utils import read_css, read_pgn, pgn_to_gif
import chess


def parse_orientation(orientation: Literal["white", "black"]) -> chess.Color:
    if orientation == "white":
        return chess.WHITE
    elif orientation == "black":
        return chess.BLACK
    else:
        raise ValueError(f"unknown {orientation=}")


def parse_bool(bool_str: Literal["1", "t", "true", "0", "f", "false"]) -> bool:
    true_values = ["1", "t", "true"]
    false_values = ["0", "f", "false"]
    if bool_str.lower() in true_values:
        return True
    elif bool_str.lower() in false_values:
        return False
    else:
        raise ValueError(f"cannot parse to bool, {bool_str}")


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--pgn-path", dest="pgn_path", required=True, type=Path, help="path to pgn file to read")
    parser.add_argument("--gif-path", dest="gif_path", required=True, type=Path, help="path to gif file to save")
    parser.add_argument("--add-initial-position", dest="add_initial_position", default="true", choices=["1", "t", "true", "0", "f", "false"], help="add initial position to gif")
    parser.add_argument("--highlight-last-move", dest="highlight_last_move", default="true", choices=["1", "t", "true", "0", "f", "false"], help="highlight last move on board")
    parser.add_argument("--orientation", dest="orientation", default="white", choices=["white", "black"], help="orientation of board")
    parser.add_argument("--size", dest="size", default=400, type=int, help="size of board")
    parser.add_argument("--coordinates", dest="coordinates", default="true", choices=["1", "t", "true", "0", "f", "false"], help="add board coordinates")
    parser.add_argument("--css-path", dest="css_path", default=None, type=Path, help="path to css file to style board")
    parser.add_argument("--loop", dest="loop", default=0, type=int, help="number of loops for gif, 0 means infinite")
    parser.add_argument("--duration", dest="duration", default=1.0, type=float, help="duration of each frame (in seconds) in gif")
    parser.add_argument("--fps", dest="fps", default=1.0, type=float, help="frame per second of gif")
    parser.add_argument("--palettesize", dest="palettesize", default=64, type=int, help="number of colors to quantize images to")
    parser.add_argument("--subrectangles", dest="subrectangles", default="true", choices=["1", "t", "true", "0", "f", "false"], help="optimize gif by storing change")

    args = parser.parse_args(argv)

    pgn = read_pgn(args.pgn_path)
    style = None if args.css_path is None else read_css(args.css_path)
    orientation = parse_orientation(args.orientation)
    add_initial_position = parse_bool(args.add_initial_position)
    highlight_last_move = parse_bool(args.highlight_last_move)
    coordinates = parse_bool(args.coordinates)
    subrectangles = parse_bool(args.subrectangles)
    pgn_to_gif(
        pgn,
        args.gif_path,
        add_initial_position,
        highlight_last_move,
        orientation,
        args.size,
        coordinates,
        style,
        args.loop,
        args.duration,
        args.fps,
        args.palettesize,
        subrectangles,
    )


if __name__ == "__main__":
    main()
