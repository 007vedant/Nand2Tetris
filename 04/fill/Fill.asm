// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

	@status
	M=-1  // status = white
	D=0   // 0/1
	@SETSCREEN
	0;JMP

(LOOP)
	@KBD
	D=M   // current key
	@SETSCREEN
	D;JEQ // white if no key
	D=-1  // black if key

(SETSCREEN)
	@ARG
	M=D    // new status argument
	@status
	D=D-M  // new status - status
	@LOOP
	D;JEQ  // continue as prev

	@ARG
	D=M
	@status
	M=D   // status=arg

	@SCREEN // screen address@16384
	D=A
	@8192
	D=D+A  //  complete map
	@i
	M=D

(SETLOOP)
	@i
	D=M-1
	M=D  // i=i-1
	@LOOP
	D;JLT // goto loop if i<0

	@status
	D=M   // D=status
	@i
	A=M 
	M=D   // M[curr_address]=status
	@SETLOOP
	0;JMP