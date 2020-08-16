# prefetch-cpu-simulator
CPU simulator to showcase the speed improvement of prefetching instructions

## Background for the uninitiated

### Assembly language
While you may be familiar with high-level code (which includes arrays, while loops, functions, and many more things), the CPU operates in a different language: assembly. 

In assembly, instructions are much simpler - the only things the CPU knows how to do are loading single values from memory, performing mathematical operations on them, and saving them back. Any code you can think of can be translated to a (large) sequence of such assembly instructions (and this is actually what happens when you compile the code, in the case of compiled languages such as C/C++).

The CPU holds a pointer to the instruction that is about to be executed (called 'PC', which stands for 'Program Counter'). Usually, the PC is incremented by one after each instruction is executed (that is, once an instruction is executed, the CPU executes the very next one) - unless the last instruction executed happens to be a JUMP instruction, which moves the PC to a different location within the source code.

### One-operand instruction set
This simulator operates a one-operand instruction set. That is, each instruction is in the following form:
```
<instruction code> <operand>
```
The simulator holds an internal register called an 'accumulator'. Whenever you do an operation, it is based on the value of the accumulator (e.g. when you do `ADD x`, `x` is added to the accumulator; when you do `SAV y`, the value in the accumulator is saved to the `y` location in the memory; when you do `JPZ p`, a jump is made to the p-th instruction if the accumulator's value is 0; and so on).

### CPU pipeline and pre-fetching
Whenever the CPU needs to execute an instruction, it first needs to bring that instruction into its immediate memory in order to read and interpret it. This process takes time - we denote it `fetch time`. 

Instruction prefetching is a technique used to boost performance by fetching instructions before they're actually needed, while the previous instruction is executed. Compare the following examples:
##### A. No prefetch
1. CPU reads instruction N;
2. CPU executes instruction N;
3. CPU reads instruction N+1;
4. CPU executes instruction N+1;
##### B. With prefetch
1. CPU reads instruction N;
2. CPU executes instruction N; at the same time, it preemptively reads instruction N+1;
3. CPU executes instruction N+1.

As you can see, example B achieves the same in fewer units of time. Preemptively reading the next instructionis called prefetching, and it also takes time. We denote it as `prefetch time`.

Sometimes though, the current instruction is a jump - so the next instruction that needs to be executed is not necessarily instruction N+1, but the instruction at the location of the jump. The CPU could not have known that in advance, because decoding that the current instruction is a jump takes place once the instruction has been executed! When this happens, it means that the CPU has made a useless prefetch - the instruction that has to be executed next is not the N+1th instruction, but rather something else, which is not yet in cache. This is known as a "cache miss", and it also takes time (much more than a regular prefetch) - we denote it as `cache miss penalty`.

### Putting it all together
The program consists of a Processor class which emulates a CPU. It has an available memory block of a fixed size and can be run either with or without prefetching. It reads the program to be executed from a text file.

The point of this is to demo how prefetching improves the execution speed of programs, taking into account cache miss penalties and fetch/prefetch times.

## Running the program
Without instruction prefetching:

```
python simulator.py --file program_examples/squares.txt --memory 100
```

With instruction prefetching:

```
python simulator.py --file program_examples/squares.txt --memory 100 --prefetch
```

## Features
- Single accumulator
- Instruction set of 21 instructions with 1 parameter each
- Memory zone with custom number of slots (default 100)
- Instruction register which emulates fetch/prefetch time and miss penalty time
- Toggle between addressing modes: immediate value (default) and indirect addressing mode

## Instruction set
Each instruction has one parameter, denoted y. When in immediate addressing mode, y is used as an immediate value. When in indirect addressing mode, y is used as memory[y] whenever it appears in the table below (e.g. in indirect addressing mode, if memory[10]=25, LOD 10 loads into accumulator the value stored in memory[25]; MOV 10 moves into accumulator the value stored in memory[10] etc). Toggle between the addressing modes with the ADR instruction.

PC gets incremented by one after each executed instruction (including jumps).
In the table below, the instruction operand is denoted `y`.

| Code | Instruction | Explanation | New value of acc | New value of pc |
|---|---|---|---|---|
| 0 | NOP | No operation | - | - |
| 1 | MOV | Move | y | - |
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