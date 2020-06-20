"""Python script for reading .asm(assembly files) and matching lexical expressions and tokens using regular
expressions """

import re

NUM = 1
LABEL = 2
OP = 3
UNKNOWN = 4


class Lex(object):
    """
    Matches lexical expressions and tokens using regex.

    Attributes:
        lines: string read from file
        tokens: word code, word tuple from line in lines
        cur_command = list of tokens for current command
        cur_token = tuple from current command

    """
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.lines = file.read()
        self.tokens = self.tokenize(self.lines.split('\n'))
        self.cur_command = []  # list of tokens for current command
        self.cur_token = (UNKNOWN, 0)  # current token of current command   

    def __str__(self):
        pass

    def has_more_commands(self):
        """
        Checks if more commands are present.
        :return: bool
        """
        return self.tokens != []

    def next_command(self):
        self.cur_command = self.tokens.pop(0)
        self.next_token()
        return self.cur_command

    def has_next_token(self):
        """
        Checks if more tokens present.
        :return: bool
        """
        return self.cur_command != []

    def next_token(self):
        """
        Removes first token of cur_command and assigns to cur_token if present.
        :return: tuple
        """
        if self.has_next_token():
            self.cur_token = self.cur_command.pop(0)
        else:
            self.cur_token = (UNKNOWN, 0)
        return self.cur_token

    def peek_token(self):
        """
        Returns first token of cur_command
        :return: tuple
        """
        if self.has_next_token():
            return self.cur_command[0]
        else:
            return UNKNOWN, 0

    def tokenize(self, lines):
        """
        Returns list of word code, word from list if list no empty.
        :param lines: string
        :return: list
        """
        return [t for t in [self.tokenize_line(l) for l in lines] if t != []]

    def tokenize_line(self, line):
        """
        Returns list of word codes and words.
        :param line: string
        :return: list
        """
        return [self.to_token(word) for word in self.split(self.remove_comment(line))]

    comment = re.compile('//.*$')  # starting with //

    def remove_comment(self, line):
        """
        Removes comment by replacing it with empty string.
        :param line: string
        :return: string
        """
        return self.comment.sub('', line)

    re_num = r'\d+'
    re_label_start = r'\w_.$:'
    re_label = '[' + re_label_start + '][' + re_label_start + r'\d]*'
    re_op = r'[=;()@+\-&|!]'
    re_word = re.compile(re_num + '|' + re_label + '|' + re_op)

    def split(self, line):
        """
        Returns all matched strings in the current line.
        :param line: string
        :return: list
        """
        return self.re_word.findall(line)

    def to_token(self, word):
        """
        Checks word type and returns tuple of type, word
        :param word: string
        :return: tuple
        """
        if self.is_num(word):
            return NUM, word
        elif self.is_label(word):
            return LABEL, word
        elif self.is_op(word):
            return OP, word
        else:
            return UNKNOWN, word
    
    # Following functions check if word is op/num etc

    def is_op(self, word):
        return self.if_match(self.re_op, word)

    def is_num(self, word):
        return self.if_match(self.re_num, word)

    def is_label(self, word):
        return self.if_match(self.re_label, word)

    def if_match(self, re_str, word):
        return re.match(re_str, word) is not None
