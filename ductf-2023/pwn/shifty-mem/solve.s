	.file	"solve.c"
	.text
	.section	.rodata
.LC0:
	.string	"Usage: %s <name>\n"
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
	subq	$224, %rsp
	movl	%edi, -212(%rbp)
	movq	%rsi, -224(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	cmpl	$2, -212(%rbp)
	je	.L2
	movq	-224(%rbp), %rax
	movq	(%rax), %rdx
	movq	stderr(%rip), %rax
	leaq	.LC0(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
	movl	$1, %edi
	call	exit@PLT
.L2:
	movq	-224(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -200(%rbp)
	movl	$-1, -204(%rbp)
.L3:
	movq	-200(%rbp), %rax
	movl	$511, %edx
	movl	$2, %esi
	movq	%rax, %rdi
	call	shm_open@PLT
	movl	%eax, -204(%rbp)
	cmpl	$-1, -204(%rbp)
	je	.L3
	movabsq	$7016996765293412544, %rax
	movabsq	$7016996765293437281, %rdx
	movq	%rax, -192(%rbp)
	movq	%rdx, -184(%rbp)
	movabsq	$7016996765293437281, %rax
	movabsq	$7016996765293437281, %rdx
	movq	%rax, -176(%rbp)
	movq	%rdx, -168(%rbp)
	movq	%rax, -160(%rbp)
	movq	%rdx, -152(%rbp)
	movq	%rax, -144(%rbp)
	movq	%rdx, -136(%rbp)
	movq	%rax, -128(%rbp)
	movq	%rdx, -120(%rbp)
	movq	%rax, -112(%rbp)
	movq	%rdx, -104(%rbp)
	movq	%rax, -96(%rbp)
	movq	%rdx, -88(%rbp)
	movq	%rax, -80(%rbp)
	movq	%rdx, -72(%rbp)
	movabsq	$7016996765293437281, %rax
	movabsq	$276085891425, %rdx
	movq	%rax, -64(%rbp)
	movq	%rdx, -56(%rbp)
	movabsq	$7016996765293412352, %rax
	movabsq	$7016996765293437281, %rdx
	movq	%rax, -48(%rbp)
	movq	%rdx, -40(%rbp)
	movabsq	$276085891425, %rax
	movabsq	$275184877568, %rdx
	movq	%rax, -32(%rbp)
	movq	%rdx, -24(%rbp)
	movw	$0, -16(%rbp)
	movb	$0, -14(%rbp)
	movl	-204(%rbp), %eax
	movl	$0, %edx
	movl	$0, %esi
	movl	%eax, %edi
	call	lseek@PLT
	leaq	-192(%rbp), %rcx
	movl	-204(%rbp), %eax
	movl	$179, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
.L4:
	movl	-204(%rbp), %eax
	movl	$0, %edx
	movl	$0, %esi
	movl	%eax, %edi
	call	lseek@PLT
	leaq	-192(%rbp), %rcx
	movl	-204(%rbp), %eax
	movl	$1, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
	jmp	.L4
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
