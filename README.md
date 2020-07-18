# nes-rle-decompress
RLE-decompression library for NES 6502 assembly, written using the [asm6f][asm6f] assembler
syntax. Includes a Python script for RLE-compressing a 1024-byte nametable data file.

## Limitations
* Currently we only encode the count using positive integers. This means that files that don't
have long runs of identical bytes won't compress as well, or may even end up quite larger than
the original file. I have a version of the code in progress which uses negative numbers to specify
that the next n bytes should be copied exactly rather than repeated. This should save some space,
but the code isn't yet working.
* Assumes your code is using vertical mirroring. The macro `LoadRLEScreen` asks for a nametable
to write to, with 0 = $2000 and 1 = $2400. The code could be tweaked easily enough to work with
horizontal mirroring.

## Compressing the nametable data file
`compress_rle.py` is a Python script which will take a 1024-byte nametable data file and
RLE-compress it. In my project, my uncompressed nametable data files have `.bin` extensions
and the compressed nametable data files have `.rle` extensions:

```
> python compress_rle.py --input bg_title_screen.bin --output bg_title_screen.rle
Input file: bg_title_screen.bin
Output file: bg_title_screen.rle
Input file size (bytes): 1024
Output file size (bytes): 516
Compression (%): 49.6

>
```

## Usage in 6502 assembly
First, define a 16-bit variable named `pointer` in RAM:

```
.enum $0000
pointer .dsb 2
.ende
```

If you don't already have constants declared with the PPU addresses, do so:

```
; PPU addresses
PpuCtrl			= $2000
PpuMask			= $2001
PpuStatus		= $2002
OamAddr			= $2003
OamData			= $2004
PpuScroll		= $2005
PpuAddr			= $2006
PpuData			= $2007
OamDma			= $4014
```

Later in code, I define different locations including RLE-compressed nametables.
For example:

```
bg_title_screen:
  .incbin "src/assets/bg_title_screen.rle"
```

The macro `LoadRLEScreen` allows you to specify the 16-bit address in PRG-ROM
where the RLE-compressed nametable data is located, as well as the nametable
it should be loaded into. `LoadRLEScreen` clobbers A, X, and Y.

```
; load into nametable 0
LoadRLEScreen bg_title_screen, $00

; load into nametable 1
LoadRLEScreen bg_title_screen, $01
```

**NOTE:** This assumes you're doing vertical mirroring. I may extend the code so
as to take the nametable memory address you're writing to, hence allowing this
to work with horizontal mirroring.

[asm6f]: https://github.com/freem/asm6f
