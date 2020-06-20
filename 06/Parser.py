"""Python script for parsing .asm(assembly language files"""
import Lexer


# Parser assumes correctly-formed input - no error checking!  Expects program-generated input.
# Would do a recursive-descent parser for fun, but it's just overkill for this.
# Parser just looks ahead one or two tokens to determine what's there.

class Parser(object):
    """
    Parses entire .asm file including symbols, labels and variables
    """
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    OTHER_INSTRUCTION = 2

    def __init__(self, asm_file):
        self.lex = Lexer.Lex(asm_file)
        self.cmd_info()

    def cmd_info(self):
        self.cmd_type = -1
        self.symbol = ''
        self.dest = ''
        self.alu = ''
        self.jmp = ''

    def __str__(self):
        pass

    def has_more_commands(self):
        """
        Checks if more tokens are present.
        :return: bool
        """
        return self.lex.has_more_commands()

    # Get the next entire command - each command resides on its own line.
    def get_next_cmd(self):
        """
        Reads next entire command into new line
        :return: None
        """
        self.cmd_info()

        self.lex.next_command()
        tok, val = self.lex.cur_token

        if tok == Lexer.OP and val == '@':
            self.a_instruction()
        elif tok == Lexer.OP and val == '(':
            self.other_instruction()
        else:
            self.c_instruction(tok, val)

    # Following functions are used to extracted different commands types from within the command

    def command_type(self):
        return self.cmd_type

    def symbol(self):
        return self.symbol

    def dest(self):
        return self.dest

    def comp(self):
        return self.alu

    def jmp(self):
        return self.jmp

    # checks if @number or @symbol
    def a_instruction(self):
        self.cmd_type = Parser.A_INSTRUCTION
        token_type, self.symbol = self.lex.next_token()

    # checks if (symbol)
    def other_instruction(self):
        self.cmd_type = Parser.OTHER_INSTRUCTION
        token_type, self.symbol = self.lex.next_token()

    # gets c instruction as dest, alu, jump
    def c_instruction(self, token1, value1):
        self.cmd_type = Parser.C_INSTRUCTION
        alu_token, alu_value = self.get_dest(token1, value1)
        self.get_alu(alu_token, alu_value)
        self.get_jump()

    def get_dest(self, token1, value1):
        """
        checks for dest part if present and returns first token of alu part.
        :param token1: string
        :param value1: binary string
        :return: string, binary string
        """
        token2, value2 = self.lex.peek_token()
        if token2 == Lexer.OP and value2 == '=':
            self.lex.next_token()
            self.dest = value1
            alu_token, alu_value = self.lex.next_token()
        else:
            alu_token, alu_value = token1, value1
        return alu_token, alu_value

    def get_alu(self, token, value):
        """
        Gets the alu part
        :param token: string
        :param value: binary string
        :return: None
        """
        if token == Lexer.OP and (value == '-' or value == '!'):
            token2, value2 = self.lex.next_token()
            self.alu = value + value2
        elif token == Lexer.NUM or token == Lexer.LABEL:
            self.alu = value
            token2, value2 = self.lex.peek_token()
            if token2 == Lexer.OP and value2 != ';':
                self.lex.next_token()
                token3, value3 = self.lex.next_token()
                self.alu += value2 + value3

    def get_jump(self):
        """
        Gets the jump part.
        :return: None
        """
        token, value = self.lex.next_token()
        if token == Lexer.OP and value == ';':
            jump_token, jump_value = self.lex.next_token()
            self.jmp = jump_value
