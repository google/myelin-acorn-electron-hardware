/*
 * Copyright (c) 2017, ARM Limited and Contributors. All rights reserved.
 *
 * Modified by Phillip Pearson to just use mov pc, lr for ARMv2.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

/*
 * EABI wrappers from the udivmod and idivmod functions
 */

	.globl ret_uidivmod_values
	.globl ret_idivmod_values

/*
 * signed ret_idivmod_values(signed quot, signed rem);
 * return quotient and remaining the EABI way (regs r0,r1)
 */
ret_idivmod_values:
	mov pc, lr

/*
 * unsigned ret_uidivmod_values(unsigned quot, unsigned rem);
 * return quotient and remaining the EABI way (regs r0,r1)
 */
ret_uidivmod_values:
	mov pc, lr
