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
IADR = 21   # toggle addressing mode


MISS_PENALTY = 0.100
PREFETCH_TIME = 0.010
FETCH_TIME = 0.010

#MISS_PENALTY = 0.00
#PREFETCH_TIME = 0.00
#FETCH_TIME = 0.00


class Processor:
    acc = 0
    pc = 0
    instr = None
    instr_pc = None
    indirect = False
    
    
    program = None
    prefetch = False
    data = []
    
    
    def __init__(self, prefetch, memsize):
        self.prefetch = prefetch
        self.data = [0 for i in range(memsize)]
        self.memsize = memsize
        
    
    def save(self, y):
        if y > self.memsize or y < 0:
            raise Exception("Memory access error")
        self.data[y] = self.acc
        return (self.acc, self.pc)
        
        
    def load(self, y):
        if y > self.memsize or y < 0:
            raise Exception("Memory access error")
        return (self.data[y], self.pc)
        
        
    def toggle_adr(self):
        self.indirect = not self.indirect
        return (self.acc, self.pc)
        
        
    def get_y(self, y):
        return y if self.indirect is False else self.data[y]
    
    
    instruction_set = {
        INOP: lambda self, acc, pc, y: (acc, pc),
        IMOV: lambda self, acc, pc, y: (self.get_y(y), pc),
        IADD: lambda self, acc, pc, y: (acc + self.get_y(y), pc),
        ISUB: lambda self, acc, pc, y: (acc - self.get_y(y), pc),
        IMUL: lambda self, acc, pc, y: (acc * self.get_y(y), pc),
        IDIV: lambda self, acc, pc, y: (acc / self.get_y(y), pc),
        IAND: lambda self, acc, pc, y: (acc and self.get_y(y), pc),
        IOR:  lambda self, acc, pc, y: (acc or self.get_y(y), pc),
        INOT: lambda self, acc, pc, y: (not acc, pc),
        IBWA: lambda self, acc, pc, y: (acc & self.get_y(y), pc),
        IBWO: lambda self, acc, pc, y: (acc | self.get_y(y), pc),
        IBWX: lambda self, acc, pc, y: (acc ^ self.get_y(y), pc),
        IBWL: lambda self, acc, pc, y: (acc << self.get_y(y), pc),
        IBWR: lambda self, acc, pc, y: (acc >> self.get_y(y), pc),
        IBWN: lambda self, acc, pc, y: (~ acc, pc),
        IJMP: lambda self, acc, pc, y: (acc, self.get_y(y)),
        IJPZ: lambda self, acc, pc, y: (acc, self.get_y(y)) if acc == 0 else (acc, pc),
        IJPN: lambda self, acc, pc, y: (acc, self.get_y(y)) if acc != 0 else (acc, pc),
        ISAV: lambda self, acc, pc, y: self.save(self.get_y(y)),
        ILOD: lambda self, acc, pc, y: self.load(self.get_y(y)),
        IHLT: lambda self, acc, pc, y: (acc, -2),
        IADR: lambda self, acc, pc, y: self.toggle_adr()
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
        if self.instr_pc < len(self.program):
            self.instr = self.program[self.instr_pc]
        else:
            raise Exception("Exceeded program code")
        return self.instr
        
        
    def prefetch_instruction(self):
        time.sleep(PREFETCH_TIME)
        self.instr_pc = self.pc + 1 if self.pc < len(self.program)-1 else len(self.program)-1
        self.instr = self.program[self.instr_pc]
        return self.instr
        
        
    def execute_if_not_halted(self):
        if self.pc == -1:
            return True
            
        self.fetch_instruction()
        instr = self.instr
        if self.prefetch:
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
    parser = argparse.ArgumentParser(description='Simulate instruction\
    prefetching for a custom instruction set processor')
    parser.add_argument('-f', '--file', required=True,
        help='program filename to run')
    parser.add_argument('-m', '--memory', default=100,
        help='memory size')
    parser.add_argument('-p','--prefetch', dest='prefetch', default=False, 
        help='activates prefetch if present', action='store_true')
    
    args = parser.parse_args()
    
    lines = [line.rstrip('\n') for line in open(args.file)]
    program = [list(map(lambda l: int(l), line.split(" "))) for line in lines]
    
    cpu = Processor(args.prefetch, int(args.memory))
    cpu.read_program(program)
    cpu.run()
    
    print("CPU Memory data:", cpu.data)
    print("Final accumulator value:", cpu.acc)
    
    