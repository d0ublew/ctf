	.file	"dump.c"
	.text
	.section	.rodata
.LC0:
	.string	"Missing filename!"
.LC1:
	.string	"rip: %#llx\n"
.LC2:
	.string	"libc_base: %#zx\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$800, %rsp
	movl	%edi, -788(%rbp)
	movq	%rsi, -800(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	$0, -768(%rbp)
	movq	stdin(%rip), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	setbuf@PLT
	movq	stdout(%rip), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	setbuf@PLT
	movq	stderr(%rip), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	setbuf@PLT
	cmpl	$2, -788(%rbp)
	je	.L2
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$1, %eax
	jmp	.L3
.L2:
	movq	-800(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -760(%rbp)
	call	fork@PLT
	movl	%eax, -772(%rbp)
	cmpl	$0, -772(%rbp)
	je	.L4
.L10:
	leaq	-780(%rbp), %rax
	movq	%rax, %rdi
	call	wait@PLT
	movl	-780(%rbp), %eax
	andl	$127, %eax
	testl	%eax, %eax
	je	.L13
	leaq	-752(%rbp), %rdx
	movl	-772(%rbp), %eax
	movq	%rdx, %rcx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$12, %edi
	movl	$0, %eax
	call	ptrace@PLT
	leaq	-528(%rbp), %rdx
	movl	-772(%rbp), %eax
	movq	%rdx, %rcx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$14, %edi
	movl	$0, %eax
	call	ptrace@PLT
	movq	-624(%rbp), %rax
	movabsq	$123145302310911, %rdx
	cmpq	%rdx, %rax
	ja	.L7
	movl	$1, -776(%rbp)
	movq	-624(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L8
.L7:
	cmpl	$0, -776(%rbp)
	je	.L8
	cmpq	$0, -768(%rbp)
	jne	.L9
	movq	-624(%rbp), %rax
	andl	$4095, %eax
	cmpq	$3520, %rax
	jne	.L9
	movq	-624(%rbp), %rax
	subq	$171456, %rax
	movq	%rax, -768(%rbp)
	movq	-768(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC2(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
.L9:
	movq	-624(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, -776(%rbp)
.L8:
	movl	-772(%rbp), %eax
	movl	$0, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$9, %edi
	movl	$0, %eax
	call	ptrace@PLT
	jmp	.L10
.L4:
	movl	$0, %ecx
	movl	$0, %edx
	movl	$0, %esi
	movl	$0, %edi
	movl	$0, %eax
	call	ptrace@PLT
	movq	-760(%rbp), %rcx
	movq	-760(%rbp), %rax
	movl	$0, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	execl@PLT
	jmp	.L11
.L13:
	nop
.L11:
	movl	$0, %eax
.L3:
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L12
	call	__stack_chk_fail@PLT
.L12:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 11.4.0-2ubuntu1~20.04) 11.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
