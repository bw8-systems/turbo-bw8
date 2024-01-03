#bankdef isa { #bits 8 }

#subruledef reg {
    r0 => 0b0000
    r1 => 0b0001
    r2 => 0b0010
    r3 => 0b0011
    r4 => 0b0100
    r5 => 0b0101
    r6 => 0b0110
    r7 => 0b0111
    r8 => 0b1000
    r9 => 0b1001
    r10 => 0b1010
    r11 => 0b1011
    r12 => 0b1100
    r13 => 0b1101
    r14 => 0b1110
    r15 => 0b1111
}

#subruledef reg16 {
    a0 => 0b00
    a1 => 0b01
    a2 => 0b10
    a3 => 0b11
}

#ruledef 
#ruledef inst {
    _binop {dst: reg}, {src: reg}, {func: BinFunc} => 0b0`0 @ src @ dst @ 0b0000 @ 0b0001
}

#fn binop() => {

}

#ruledef bw8 {
    mov {dst: reg}, {src: reg} => 0b0`0 @ src @ dst @ 0b0000 @ 0b000
    int {vec: u8} => 0b0`0 @ vec @ 0b0001 @ 0b000
    clrk => 0b0`0 @ 0b000_000 @ 0b00 @ 0b0010 @ 0b000
    seti => 0b0`0 @ 0b000_000 @ 0b01 @ 0b0010 @ 0b000
    clri => 0b0`0 @ 0b000_000 @ 0b10 @ 0b0010 @ 0b000

    add {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b0000 @ 0b0001
    sub {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b0001 @ 0b0001
    addc {dst: reg}, {src: reg} => 0b0`0 @ src @ dst @ 0b0010 @ 0b0001
    subb {dst: reg}, {src: reg} => 0b0`0 @ src @ dst @ 0b0011 @ 0b0001
    and {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b0100 @ 0b0001
    or {dst: reg}, {src: reg}   => 0b0`0 @ src @ dst @ 0b0101 @ 0b0001
    xor {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b0110 @ 0b0001
    shl {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b0111 @ 0b0001
    asr {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b1000 @ 0b0001
    lsr {dst: reg}, {src: reg}  => 0b0`0 @ src @ dst @ 0b1001 @ 0b0001
    cmp  {dst: reg}, {src: reg} => 0b0`0 @ src @ dst @ 0b1010 @ 0b0001

    neg {dst: reg}  => 0b0`0 @ 0b0000 @ dst @ 0b0 @ 0b000 @ 0b010
    negb {dst: reg} => 0b0`0 @ 0b0000 @ dst @ 0b1 @ 0b000 @ 0b010
}

#ruledef alias {
    nop => asm {mov r0, r0}
}