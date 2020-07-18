# nes-rle-decompress
RLE-decompression library for NES 6502 assembly, written using the [asm6f][asm6f] assembler
syntax. Includes a Python script for RLE-compressing a 1024-byte nametable data file.

## Usage in 6502 assembly
First, define a 16-bit variable named `pointer` in RAM:

```
.enum $0000
pointer .dsb 2
.ende
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
