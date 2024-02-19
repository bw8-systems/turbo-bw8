#bankdef isa { #bits 8 }

#subruledef gpr {
    r0  => 0b0000
    r1  => 0b0001
    r2  => 0b0010
    r3  => 0b0011
    r4  => 0b0100
    r5  => 0b0101
    r6  => 0b0110
    r7  => 0b0111
    r8  => 0b1000
    r9  => 0b1001
    r10 => 0b1010
    r11 => 0b1011
    r12 => 0b1100
    r13 => 0b1101
    r14 => 0b1110
    r15 => 0b1111

    lr => r15
}

#subruledef vec {
    v0 => 0b000
    v1 => 0b001
    v2 => 0b010
    v3 => 0b011
    v4 => 0b100
    v5 => 0b101
    v6 => 0b110
    v7 => 0b111
}

#subruledef mmu {
    mmu0  => 0b0000
    mmu1  => 0b0001
    mmu2  => 0b0010
    mmu3  => 0b0011
    mmu4  => 0b0100
    mmu5  => 0b0101
    mmu6  => 0b0110
    mmu7  => 0b0111
    mmu8  => 0b1000
    mmu9  => 0b1001
    mmu10 => 0b1010
    mmu11 => 0b1011
    mmu12 => 0b1100
    mmu13 => 0b1101
    mmu14 => 0b1110
    mmu15 => 0b1111
}

#subruledef spr {
    ilr => 0b0
    psr => 0b1
}

#subruledef lui_imm {
    {imm: i16} => {
        assert(imm & 0b11111 == 0x00)
        imm
    }
}

#subruledef s5_aligned {
    {imm: s5} => {
        assert(imm & 0b1 == 0x00)
        imm
    }
}

#subruledef stz_imm {
    {imm: u5} => {
        assert(imm & 0b1 == 0x00)
        imm
    }
}

#subruledef jr_imm {
    {imm: s7} => {
        assert(imm & 0b1 == 0x00)
        imm
    }
}

#subruledef func {
    mv   => 0b0000
    add  => 0b0001
    addc => 0b0010
    sub  => 0b0011
    subb => 0b0100
    and  => 0b0101
    or   => 0b0110
    xor  => 0b0111
    shl  => 0b1000
    lsr  => 0b1001
    asr  => 0b1010
    cmp  => 0b1011
}

#subruledef op11 {
    lli  => 0b00
    addi => 0b01
    cmpi => 0b10
}

#subruledef jump {
    j  => 0b0
    jal => 0b1
}

#subruledef jump_rel {
    jr     => 0b000
    jral   => 0b001
    br.eq  => 0b010
    br.ne  => 0b011
    br.lt  => 0b100
    br.ge  => 0b101
    br.lts => 0b110
    br.ges => 0b111
}

#subruledef bitwise_imm {
    andi => 0b0
    ori => 0b1
}

#subruledef unary {
    not => 0b000
    apc => 0b001
    neg => 0b010
    negb => 0b011
    swap => 0b100
    sxt => 0b101
}

#subruledef int {
    sys => 0b0
    irq => 0b1
}

#subruledef nullary {
    reti => 0b000
}

#ruledef bw8 {
    lui {rd: gpr}, {imm: lui_imm} => 0b0 @ imm[14:9] @ imm[15:15] @ imm[8:5] @ rd

    ld8 {rd: gpr}, {rs: gpr}, {imm: s5} => 0b10 @ 0b0 @ imm[0:0] @ imm[3:1] @ imm[4:4] @ rs @ rd
    st8 {rs: gpr}, {rd: gpr}, {imm: s5} => 0b10 @ 0b1 @ imm[0:0] @ imm[3:1] @ imm[4:4] @ rs @ rd

    ld {rd: gpr}, {rs: gpr}, {imm: s5_aligned} => 0b110 @ 0b0 @ imm[3:1] @ imm[4:4] @ rs @ rd
    st {rs: gpr}, {rd: gpr}, {imm: s5_aligned} => 0b110 @ 0b1 @ imm[3:1] @ imm[4:4] @ rs @ rd

    {func: func} {rd: gpr}, {rs: gpr} => 0b1110 @ func @ rs @ rd

    mv {vd: vec}, {rs: gpr} => 0b1110 @ 0b1100 @ 0b0 @ vd @ rs
    mv {rd: gpr}, {vs: vec} => 0b1110 @ 0b1100 @ 0b1 @ vs @ rd

    shli {rd: gpr}, {imm: u4} => 0b1110 @ 0b1101 @ imm[3:0] @ rd
    lsri {rd: gpr}, {imm: u4} => 0b1110 @ 0b1110 @ imm[3:0] @ rd
    asri {rd: gpr}, {imm: u4} => 0b1110 @ 0b1111 @ imm[3:0] @ rd

    {func: op11} {rd: gpr}, {imm: i5} => 0b1111 @ 0b0 @ func @ imm[4:0] @ rd

    {j: jump} {rs: gpr}, {imm: s5_aligned} => 0b1111 @ 0b0 @ 0b11 @ imm[4:4] @ rs @ j @ imm[3:1]

    mv {md: mmu}, {rs: gpr} => 0b1111 @ 0b10 @ 0b0 @ 0b0 @ md @ rs
    mv {rd: gpr}, {ms: mmu} => 0b1111 @ 0b10 @ 0b0 @ 0b1 @ ms @ rd

    {jr: jump_rel} {imm: jr_imm} => 0b1111 @ 0b10 @ 0b1 @ imm[6:6] @ imm[3:1] @ imm[5:4] @ jr

    {func: bitwise_imm} {rd: gpr}, {imm: u4} => 0b1111 @ 0b110 @ func @ imm[3:0] @ rd

    stz {rs: gpr}, {imm: stz_imm} => 0b1111 @ 0b1110 @ rs @ imm[4:1]

    {func: unary} {rd: gpr} => 0b1111 @ 0b1111 @ 0b0 @ func @ rd

    mv {sd: spr}, {rs: gpr} => 0b1111 @ 0b1111 @ 0b10 @ 0b0 @ sd @ rs
    mv {rd: gpr}, {ss: spr} => 0b1111 @ 0b1111 @ 0b10 @ 0b1 @ ss @ rd

    env {imm: u4} => 0b1111 @ 0b1111 @ 0b1110 @ imm

    {int: int} {imm: u2} => 0b1111 @ 0b1111 @ 0b1111 @ 0b0 @ int @ imm

    {func: nullary} => 0b1111 @ 0b1111 @ 0b1111 @ 0b1 @ func
}
