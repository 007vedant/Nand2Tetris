""" Python script for assembling the .asm files(assembly code) into .hack files(machine / binary code)
    usage : assembler.py <filename>.asm
"""

import sys
import Code
import Parser
import Lexer
import SymbolTable


class Assembler(object):
    """
    Generates assembled binary code into .hack file from assembly .asm files.

    Attributes:
        symbols: object of SymbolTable class
        symbol_address = 16-bit binary code
    """
    def __init__(self):
        self.symbols = SymbolTable.SymbolTable()
        self.symbol_address = 16

    def pass0(self, asm_file):
        """
        Determines memory location of label definitions(LABEL) in first pass.
        :param asm_file: .asm file
        :return: None
        """
        parser = Parser.Parser(asm_file)
        cur_address = 0
        while parser.has_more_commands():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND or cmd == parser.C_COMMAND:
                cur_address += 1
            elif cmd == parser.L_COMMAND:
                self.symbols.add_address(parser.symbol(), cur_address)

    def pass1(self, asm_file, hack_file):
        """
        Generates binary code and writes to .hack file.
        :param asm_file: .asm file with assembly code
        :param hack_file: .hack file with binary code
        :return: None
        """
        parser = Parser.Parser(asm_file)
        outfile = open(hack_file, 'w')
        code = Code.Code()
        while parser.has_more_commands():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND:
                outfile.write(code.a_instruction(self.get_address(parser.symbol())) + '\n')
            elif cmd == parser.C_COMMAND:
                outfile.write(code.c_instruction(parser.dest(), parser.comp(), parser.jmp()) + '\n')
            elif cmd == parser.L_COMMAND:
                pass
        outfile.close()

    def get_address(self, symbol):
        """
        Looks up address of symbol else adds symbols along with address.
        :param symbol: string
        :return: symbol
        """
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.add_address(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbols.get_address(symbol)

    def assemble(self, asm_file):
        """
        Wrapper around pass0 and pass1 methods.
        :param asm_file: .asm file
        :return: None
        """
        self.pass0(asm_file)
        self.pass1(asm_file, self.hack_file(asm_file))

    def hack_file(self, asm_file):
        """
        Renames .asm files into .hack files.
        :param asm_file: .asm file
        :return: .hack file object
        """
        if asm_file.endswith('.asm'):
            return asm_file.replace('.asm', '.hack')
        else:
            return asm_file + '.hack'


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("command line usage: assembler.py <filename>.asm")
    else:
        asm_file = sys.argv[1]  # name of input file

    asm = Assembler()
    asm.assemble(asm_file)
