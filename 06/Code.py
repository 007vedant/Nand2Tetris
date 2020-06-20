""" Python script to generate 16-bit codes from parsed instruction."""


class Code(object):
    """ Generates 16-bit binary codes per line.

        Attributes:
            dest_codes: list of destination code strings
            alu_codes: dict of alu operations and binary values
            jump_codes: list of jump code strings

    """

    dest_codes = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']

    alu_codes = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
                 'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
                 '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
                 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
                 'D&A': '0000000', 'D|A': '0010101',
                 '': 'xxxxxxx', '': 'xxxxxxx', '': 'xxxxxxx', '': 'xxxxxxx',
                 'M': '1110000', '': 'xxxxxxx', '!M': '1110001', '': 'xxxxxxx',
                 '-M': '1110011', '': 'xxxxxxx', 'M+1': '1110111', '': 'xxxxxxx',
                 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
                 'D&M': '1000000', 'D|M': '1010101'}

    jump_codes = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    def __init__(self):
        pass

    def a_instruction(self, address):
        """
        Generates 16-bit binary sting for A instruction.
        :param address: int/hex
        :return: 16 bit binary string
        """
        return '0' + self.to_bits(address).zfill(15)

    def c_instruction(self, dest, alu, jump):
        """
        Generates 16 bit binary string for C instruction.
        :param dest: string
        :param alu: string
        :param jump: string
        :return: 16 bit binary string
        """

        return '111' + self.alu(alu) + self.dest(dest) + self.jump(jump)

    def dest(self, d):
        """
        Generates binary string for dest.
        :param d: string
        :return: binary string
        """
        return self.to_bits(self.dest_codes.index(d)).zfill(3)

    def alu(self, c):
        """
        Generates binary string for alu.
        :param c: string
        :return: binary string
        """
        return self.alu_codes[c]

    def jump(self, j):
        """
        Generates binary string for jump.
        :param j: string
        :return: string
        """
        return self.to_bits(self.jump_codes.index(j)).zfill(3)

    def to_bits(self, n):
        """
        Converts to binary string.
        :param n: int/hex
        :return: binary string
        """
        return bin(int(n))[2:]



