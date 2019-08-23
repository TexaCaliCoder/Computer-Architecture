"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

       
        try:
            with open( sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_number = comment_split[0]
                    if possible_number == '':
                        continue
                    first_bit = possible_number[0]
                    if first_bit == '1' or first_bit == '0':
                        instruction = int(possible_number[:8], 2)
                        self.ram[address] = instruction
                        address +=1
                        
        except FileNotFoundError:
            print(f'Unable to find {sys.argv[1]}, please check the name and try again')
            sys.exit(2)


        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address ):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        ir = self.pc
        running = True
       
        while running:
            operand_a = self.ram_read(ir +1)
            operand_b = self.ram_read(ir + 2)
            # print(f'operand1: {operand_a}')
            # print(f'operand2: {operand_b}')

            if self.ram_read(ir) == 0b10000010: #LDI
                self.reg[operand_a] = int(operand_b)
                print('ldi')
                ir += 3
            elif self.ram_read(ir) == 0b01000111: #PRN
                print( 'print', self.reg[int(operand_a)])
                ir += 2
            elif self.ram_read(ir) == 0b10100010: #MULT
                print('mult')
                mult_sum = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = mult_sum
                ir += 3
            elif self.ram_read(ir) == 0b00000001: #HLT
                print('halt')
                running = False





