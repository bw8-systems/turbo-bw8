# `turbo-bw8`
An 8-bit ISA with a pipelined implementation.

## Motivation
Over the course of the `bw8` project, the aspirational applications of the system have evolved in ways that have demanded more and more performance from the system.

Although both the design of the instruction set and the implementation of the microarchitecture have incrementally improved in pursuit of accomodating these change in ways that have yielded a remarkably versatile system, the fundamental skeleton of the design imposes somewhat "hard" limitations on what is and is not going to be possible with the system.

In light of this, the time has come to do a hard-stop, all encompassing, reformulation of the design before committing significant time to the development of demanding tooling so as to ensure that the resulting system can live up to its currently stated goals.

## State of the Union
The Programming Model of the extant system is described below.

### Current Programming Model
**Register File**
- 4x 8-bit General Purpose (data) Registers: `a`, `b`, `c`, `d`.
- 2x 16-bit General Purpose "pointer" Registers: `x`, `y`.
- 1x 16-bit dedicated Stack Pointer, `sp`.

**Bus Interaction**
A 4-bit Bank Register (`br`) extends the internal address registers from 16 bits to 20 bits. This creates a 1 Mword physical address space. The content of the register is only modifiable from the supervisory privilege level, which effectively divides the 1 Mword physical space into 16x 64 Kword "virtual" spaces, which provides a simple layer of process isolation.

The Control Unit (CU) produces line `D/~C` which signifies via the system bus the memory access type of the current memory operation, specifically whether its a data or code access. When paired with `br`, this provides another doubling of the physical address space, allowing for 16x 128 Kword spaces split as 64K code and 64K data.

The ISA has two families of bus access instructions: load and store (`ld`/`st`) for memory operations, and in and out (`in`/`out`) for IO operations. The CU does not manage `br` during IO access cycles, so the resulting IO space is 64KB.

### Project Goals
- Construction of homebrew system in discrete logic on custom PCBs.