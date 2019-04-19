import argparse
import time


INOP = 0    # nop 
IMOV = 1    # mov 
IADD = 2    # add 
ISUB = 3    # sub 
IMUL = 4    # mul 
IDIV = 5    # div 
IAND = 6    # and 
IOR = 7     # or
INOT = 8    # not
IBWA = 9    # bitwise and
IBWO = 10   # bitwise or
IBWX = 11   # bitwise xor
IBWL = 12   # bitwise rot left
IBWR = 13   # bitwise rot right
IBWN = 14   # bitwise not
IJMP = 15   # jump
IJPZ = 16   # jump if zero
IJPN = 17   # jump if nonzero
ISAV = 18   # save data
ILOD = 19   # load data
IHLT = 20   # halt


MISS_PENALTY = 0.100
PREFETCH_TIME = 0.010
FETCH_TIME = 0.010


class Processor:
    acc = 0
    pc = 0
    instr = None
    instr_pc = None
    
    program = None
    data = [0 for i in range(100)]
    
    
    def save(self, y):
        self.data[y] = self.acc
        return (self.acc, self.pc)
        
        
    def load(self, y):
        return (self.data[y], self.pc)
    
    
    instruction_set = {
        INOP: lambda self, acc, pc, y: (acc, pc),
        IMOV: lambda self, acc, pc, y: (y, pc),
        IADD: lambda self, acc, pc, y: (acc + y, pc),
        ISUB: lambda self, acc, pc, y: (acc - y, pc),
        IMUL: lambda self, acc, pc, y: (acc * y, pc),
        IDIV: lambda self, acc, pc, y: (acc / y, pc),
        IAND: lambda self, acc, pc, y: (acc and y, pc),
        IOR:  lambda self, acc, pc, y: (acc or y, pc),
        INOT: lambda self, acc, pc, y: (not acc, pc),
        IBWA: lambda self, acc, pc, y: (acc & y, pc),
        IBWO: lambda self, acc, pc, y: (acc | y, pc),
        IBWX: lambda self, acc, pc, y: (acc ^ y, pc),
        IBWL: lambda self, acc, pc, y: (acc << y, pc),
        IBWR: lambda self, acc, pc, y: (acc >> y, pc),
        IBWN: lambda self, acc, pc, y: (~ acc, pc),
        IJMP: lambda self, acc, pc, y: (acc, y),
        IJPZ: lambda self, acc, pc, y: (acc, y) if acc == 0 else (acc, pc),
        IJPN: lambda self, acc, pc, y: (acc, y) if acc != 0 else (acc, pc),
        ISAV: lambda self, acc, pc, y: self.save(y),
        ILOD: lambda self, acc, pc, y: self.load(y),
        IHLT: lambda self, acc, pc, y: (acc, -2),
    }
    
    
    def process_instruction(self, x, y):
        f = self.instruction_set.get(x)
        (self.acc, self.pc) = f(self, self.acc, self.pc, y)
        self.acc = int(self.acc)
        self.pc = int(self.pc) + 1
        
        
    def read_program(self, program):
        self.program = program
        
        
    def fetch_instruction(self):
        time.sleep(FETCH_TIME)
        if self.instr_pc == self.pc:
            return self.instr
            
        time.sleep(MISS_PENALTY)    
        self.instr_pc = self.pc
        self.instr = self.program[self.instr_pc]
        return self.instr
        
        
    def prefetch_instruction(self):
        time.sleep(PREFETCH_TIME)
        self.instr_pc = self.pc + 1 if self.pc < len(program)-1 else self.pc
        self.instr = self.program[self.instr_pc]
        return self.instr
        
        
    def execute_if_not_halted(self):
        if self.pc == -1:
            return True
            
        self.fetch_instruction()
        instr = self.instr
        self.prefetch_instruction()
        self.process_instruction(instr[0], instr[1])
        
        return False
        
        
    def run(self):
        halted = False;
        while not halted:
            halted = self.execute_if_not_halted()
            
        
    def debug_execute_all(self):
        for line in program:
            self.process_instruction(line[0], line[1])
        
        
if __name__ == "__main__":
    cpu = Processor()
    
    parser = argparse.ArgumentParser(description='Simulate instruction\
    prefetching for a custom instruction set processor')
    parser.add_argument('-f', '--file', required=True,
        help='program filename to run')
    
    args = parser.parse_args()
    
    lines = [line.rstrip('\n') for line in open(args.file)]
    program = [map(lambda l: int(l), line.split(" ")) for line in lines]
    
    cpu.read_program(program)
    cpu.run()
    
    print "Final accumulator value:", cpu.acc
    print "CPU Memory data:", cpu.data
    
    