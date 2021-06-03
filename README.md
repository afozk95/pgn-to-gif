# pgn-to-gif
Generate GIFs of chess games from PGN files.

## Installation
`pip3 install pgn-to-gif`

## Usage
```
usage: pgn-to-gif [-h] --pgn-path PGN_PATH --gif-path GIF_PATH [--add-initial-position {1,t,true,0,f,false}] [--highlight-last-move {1,t,true,0,f,false}] [--orientation {white,black}]
              [--size SIZE] [--coordinates {1,t,true,0,f,false}] [--css-path CSS_PATH] [--loop LOOP] [--duration DURATION] [--fps FPS] [--palettesize PALETTESIZE]
              [--subrectangles {1,t,true,0,f,false}] [--processes PROCESSES]

optional arguments:
  -h, --help            show this help message and exit
  --pgn-path PGN_PATH   path to pgn file to read (default: None)
  --gif-path GIF_PATH   path to gif file to save (default: None)
  --add-initial-position {1,t,true,0,f,false}
                        add initial position to gif (default: true)
  --highlight-last-move {1,t,true,0,f,false}
                        highlight last move on board (default: true)
  --orientation {white,black}
                        orientation of board (default: white)
  --size SIZE           size of board (default: 400)
  --coordinates {1,t,true,0,f,false}
                        add board coordinates (default: true)
  --css-path CSS_PATH   path to css file to style board (default: None)
  --loop LOOP           number of loops for gif, 0 means infinite (default: 0)
  --duration DURATION   duration of each frame (in seconds) in gif (default: 1.0)
  --fps FPS             frame per second of gif (default: 1.0)
  --palettesize PALETTESIZE
                        number of colors to quantize images to (default: 64)
  --subrectangles {1,t,true,0,f,false}
                        optimize gif by storing change (default: true)
  --processes PROCESSES
                        number of processes when converting svgs to pngs (default: 1)
```

## Examples
Please see [examples](https://github.com/afozk95/pgn-to-gif/tree/master/examples) folder.