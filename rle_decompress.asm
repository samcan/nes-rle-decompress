;;;;;;;;;;;;;;;;
MACRO LoadRLEScreen x, nt
  ; Clobbers: A, X
  LDA #<x
  STA pointer+0
  LDA #>x
  STA pointer+1

  LDX #nt

  JSR DecodeRLEScreen
ENDM
;;;;;;;;;;;;;;;;
;; DecodeRLEScreen
;;
;; Decodes an RLE-compressed screen and loads it into the background.
;;
;;
;; Sample usage:
;;
;;   LDA #<bg_title_screen
;;   STA pointer+0
;;   LDA #>bg_title_screen
;;   STA pointer+1
;;
;;   ; set which nametable to load (0 = nametable 0, 1 = nametable 1)
;;   LDX #$00
;;
;;   JSR DecodeRLEScreen
;;
;; Clobbers: A, X, Y
DecodeRLEScreen:
  ; set output address
  LDA #PpuStatus
  CPX #$01
  BEQ @loadOne
  LDA #$20
  JMP @cont
@loadOne:
  LDA #$24
@cont:
  STA PpuAddr
  LDA #$00
  STA PpuAddr

  ; ; copy screen to VRAM
  ; Decode RLE
  LDY #$00
@big:
  ; get count and byte
  ; get count (has to be LDA rather than LDX)
  LDA (pointer),y
  TAX
  CPX #$00
  BEQ @done
  INY
  ; get byte
  LDA (pointer), y
@loop:
  STA PpuData
  DEX
  BNE @loop
  INY
  BNE @big
  INC pointer+1
  JMP @big
@done:
  RTS
