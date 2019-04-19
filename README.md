# prefetch-cpu-simulator
CPU simulator to showcase the speed improvement of prefetching instructions

## Running the program
Without instruction prefetching:

python simulator.py --file program_examples/squares.txt --memory 100

With instruction prefetching:

python simulator.py --file program_examples/squares.txt --memory 100 --prefetch

## Features
- Single accumulator
- Instruction set of 21 instructions with 1 parameter each
- Memory zone with custom number of slots (default 100)
- Instruction register which emulates fetch/prefetch time and miss penalty time
- Toggle between addressing modes: immediate value (default) and indirect addressing mode

## Instruction set
Each instruction has one parameter, denoted y. When in immediate addressing mode, y is used as an immediate value. When in indirect addressing mode, y is used as memory[y] whenever it appears in the table below (e.g. in indirect addressing mode, if memory[10]=25, LOD 10 loads into accumulator the value stored in memory[25]; MOV 10 moves into accumulator the value stored in memory[10] etc). Toggle between the addressing modes with the ADR instruction.

PC gets incremented by one after each executed instruction (including jumps).

| Code | Instruction | Explanation | New value of acc | New value of pc |
|---|---|---|---|---|
| 0 | NOP | No operation | - | - |
| 1 | MOV | Move | pc | - |
| 2 | ADD | Add | acc + y | - |
| 3 | SUB | Subtract | acc - y | - |
| 4 | MUL | Multiply | acc \* y | - |
| 5 | DIV | Divide | acc / y | - |
| 6 | AND | Boolean and | acc && y | - |
| 7 | OR | Boolean or | acc \|\| y | - |
| 8 | NOT | Boolean not | !acc | - |
| 9 | BWA | Bitwise and | acc & y | - |
| 10 | BWO | Bitwise or | acc \| y | - |
| 11 | BWX | Bitwise xor | acc ^ y | - |
| 12 | BWL | Bitwise left rotation | acc << y | - |
| 13 | BWR | Bitwise right rotation | acc >> y | - |
| 14 | BWN | Bitwise not | ~acc | - |
| 15 | JMP | Unconditional jump | - | y |
| 16 | JPZ | Jump if zero | - | if acc==0 then y else pc |
| 17 | JPN | Jump if non zero | - | if acc!=0 then y else pc |
| 18 | SAV | Save acc to memory[y] | - | - |
| 19 | LOD | Load acc from memory[y] | memory[y] | - |
| 20 | HLT | Halt | - | - |
| 21 | ADR | Toggle addressing mode | - | - |