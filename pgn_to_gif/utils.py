from typing import Generator, Iterable, Optional, Tuple, Union
from io import StringIO
from pathlib import Path
from tempfile import TemporaryFile
import cairosvg
import chess
import chess.pgn
import chess.svg
import imageio


def read_file(path: Union[Path, str]) -> str:
    """Read file from given path

    Args:
        path (Union[Path, str]): path to file

    Returns:
        str: pgn as str
    """
    with open(path, mode="r") as f:
        text = f.read()
    return text


read_pgn = read_file
read_css = read_file


def pgn_to_game(pgn: str) -> chess.pgn.Game:
    """Parse pgn str to chess game

    Args:
        pgn (str): pgn as str

    Returns:
        chess.pgn.Game: chess game
    """
    game = chess.pgn.read_game(StringIO(pgn))
    return game


def game_to_boards_and_last_moves(
    game: chess.pgn.Game,
    add_initial_position: bool = True,
) -> Generator[Tuple[chess.Board, Optional[chess.Move]], None, None]:
    """Return generator of chess board and last move after each move for given chess game

    Args:
        game (chess.pgn.Game): chess game
        add_initial_position (bool, optional): add initial position. defaults to True.

    Yields:
        Generator[Tuple[chess.Board, Optional[chess.Move]], None, None]: generator of chess board and last move
    """
    if add_initial_position:
        yield chess.Board(), None
    for move, game_node in zip(game.mainline_moves(), game.mainline()):
        yield game_node.board(), move


def board_to_svg(
    board: chess.Board,
    orientation: chess.Color = chess.WHITE,
    last_move: Optional[chess.Move] = None,
    size: int = 400,
    coordinates: bool = True,
    style: Optional[str] = None,
) -> chess.svg.SvgWrapper:
    """Given chess board return svg string

    Args:
        board (chess.Board): chess board
        orientation (chess.Color): board orientation
        lastmove (Optional[chess.Move], optional): last move to highlight on board. defaults to None.
        size (int, optional): size of board in svg. defaults to 400.
        coordinates (bool, optional): add board coordinates to svg. defaults to True.
        style (Optional[str], optional): style css for svg. defaults to None.

    Returns:
        chess.svg.SvgWrapper: wrapped svg string
    """
    assert isinstance(size, int) and size > 0, "size of the board must be positive integer"
    return chess.svg.board(board, orientation=orientation, lastmove=last_move, size=size, coordinates=coordinates, style=style)


def svg_to_png(
    board_svg: chess.svg.SvgWrapper,
) -> bytes:
    """Convert svg to png

    Args:
        board_svg (chess.svg.SvgWrapper): board svg

    Returns:
        bytes: board png
    """
    return cairosvg.svg2png(bytestring=board_svg)


def pngs_to_gif(
    pngs: Iterable[bytes],
    loop: int = 0,
    duration: Optional[float] = None,
    fps: Optional[float] = None,
    palettesize: int = 16,
    subrectangles: bool = True,
) -> TemporaryFile:
    """Make gif from png images

    Args:
        pngs (Iterable[bytes]): iterable of png bytes
        loop (int, optional): number of gif loops, 0 = infinite. defaults to 0.
        duration (Optional[float], optional): duration of each frame in gif (in seconds). defaults to None.
        fps (Optional[float], optional): fps of gif. used only if duration is None. defaults to None.
        palettesize (int, optional): number of colors to quantize the image to. 
            rounded to the nearest power of two. defaults to 16.
        subrectangles (bool, optional): try and optimize the GIF by storing only the rectangular
            parts of each frame that change with respect to the previous. defaults to True.

    Raises:
        ValueError: if duration and fps are both None

    Returns:
        TemporaryFile: gif as temporary file
    """
    if duration is None and fps is None:
        raise ValueError("duration and fps cannot be None at the same time")

    temp_file = TemporaryFile()
    with imageio.get_writer(
        temp_file,
        mode="I",
        format="gif",
        loop=loop,
        duration=duration,
        fps=fps,
        palettesize=palettesize,
        subrectangles=subrectangles,
    ) as writer:
        [writer.append_data(imageio.imread(png)) for png in pngs]

    return temp_file


def save_gif_temp_file(temp_file: TemporaryFile, path: Union[Path, str]) -> None:
    """Save gif in temporary file to given path, and then close temporary file

    Args:
        temp_file (TemporaryFile): gif in temporary file
        path (Path): path to save gif
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_file.seek(0)
    with open(path, mode="wb+") as f:
        f.write(temp_file.read())
    temp_file.close()


def game_to_gif(
    game: chess.pgn.Game,
    gif_path: Optional[Union[Path, str]] = None,
    add_initial_position: bool = True,
    highlight_last_move: bool = True,
    orientation: chess.Color = chess.WHITE,
    size: int = 400,
    coordinates: bool = True,
    style: Optional[str] = None,
    loop: int = 0,
    duration: Optional[float] = None,
    fps: Optional[float] = 1.0,
    palettesize: int = 16,
    subrectangles: bool = True,
) -> Optional[TemporaryFile]:
    """Generate gif of chess game from pgn

    Args:
        game (chess.pgn.Game): chess game
        gif_path (Optional[Union[Path, str]], optional): path to save gif. defaults to None.
        add_initial_position (bool, optional): add initial position. defaults to True.
        highlight_last_move (bool, optional): highlight last move. defaults to True.
        orientation (chess.Color, optional): orientation of chess board. defaults to chess.WHITE.
        size (int, optional): size of chess board. defaults to 400.
        coordinates (bool, optional): add board coordinates. defaults to True.
        style (Optional[str], optional): style of board svg. defaults to None.
        loop (int, optional): loop count of gif, 0 means infinite. defaults to 0.
        duration (Optional[float], optional): duration of each frame in gif. defaults to None.
        fps (Optional[float], optional): frame per second of gif. defaults to 1.0.
        palettesize (int, optional): number of colors to quantize image to. defaults to 16.
        subrectangles (bool, optional): try and optimize gif by storing only the rectangular
            parts of each frame that change with respect to the previous. defaults to True.

    Returns:
        Optional[TemporaryFile]: gif in temporary file 
    """
    boards_and_last_moves = game_to_boards_and_last_moves(game, add_initial_position)
    svgs = (
        board_to_svg(
            board,
            orientation,
            last_move if highlight_last_move else None,
            size,
            coordinates,
            style,
        )
        for board, last_move in boards_and_last_moves
    )
    pngs = (svg_to_png(svg) for svg in svgs)
    gif_temp_file = pngs_to_gif(
        pngs,
        loop,
        duration,
        fps,
        palettesize,
        subrectangles,
    )
    
    if gif_path is not None:
        save_gif_temp_file(gif_temp_file, gif_path)
    else:
        return gif_temp_file


def pgn_to_gif(
    pgn: str,
    gif_path: Optional[Union[Path, str]] = None,
    add_initial_position: bool = True,
    highlight_last_move: bool = True,
    orientation: chess.Color = chess.WHITE,
    size: int = 400,
    coordinates: bool = True,
    style: Optional[str] = None,
    loop: int = 0,
    duration: Optional[float] = None,
    fps: Optional[float] = 1.0,
    palettesize: int = 16,
    subrectangles: bool = True,
) -> Optional[TemporaryFile]:
    """Generate gif of chess game

    Args:
        pgn (str): chess game pgn
        gif_path (Optional[Union[Path, str]], optional): path to save gif. defaults to None.
        add_initial_position (bool, optional): add initial position. defaults to True.
        highlight_last_move (bool, optional): highlight last move. defaults to True.
        orientation (chess.Color, optional): orientation of chess board. defaults to chess.WHITE.
        size (int, optional): size of chess board. defaults to 400.
        coordinates (bool, optional): add board coordinates. defaults to True.
        style (Optional[str], optional): style of board svg. defaults to None.
        loop (int, optional): loop count of gif, 0 means infinite. defaults to 0.
        duration (Optional[float], optional): duration of each frame in gif. defaults to None.
        fps (Optional[float], optional): frame per second of gif. defaults to 1.0.
        palettesize (int, optional): number of colors to quantize image to. defaults to 16.
        subrectangles (bool, optional): try and optimize gif by storing only the rectangular
            parts of each frame that change with respect to the previous. defaults to True.

    Returns:
        Optional[TemporaryFile]: gif in temporary file 
    """
    game = pgn_to_game(pgn)
    return game_to_gif(
        game,
        gif_path,
        add_initial_position,
        highlight_last_move,
        orientation,
        size,
        coordinates,
        style,
        loop,
        duration,
        fps,
        palettesize,
        subrectangles,
    )
