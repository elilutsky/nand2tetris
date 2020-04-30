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

(GETCLICK)

	// color = -1 if KBD else 0
	@KBD
	D=M
	@NOKEY
	D;JEQ
	D=-1
(NOKEY)
	@color
	M=D
	
	@i
	M=0

(LOOP)
	
	// if (index == 8192) goto GETCLICK
	@i
	D=M
	@8192                 
	D=D-A
	@GETCLICK
	D;JEQ
	
	// addr = SCREEN + index 
	@SCREEN
	D=A
	@i
	D=D+M
	@addr
	M=D
	
	// M[addr] = color
	@color
	D=M
	@addr
	A=M
	M=D
	
	// i++; goto LOOP
	@i
	M=M+1
	@LOOP
	0;JMP

(END)
    @END
    0;JMP 