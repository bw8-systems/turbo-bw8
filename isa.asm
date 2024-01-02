#bankdef isa { #bits 8 }

op:
    .mov = 0b0000

#ruledef reg {
    r0 => 0b00
    r1 => 0b01
    r2 => 0b10
    r3 => 0b11
}

#ruledef bw8 {
    nop => asm {mov r0, r0}
    mov {dst: reg}, {src: reg} => op.mov`4 @ dst`2 @ src`2
}
