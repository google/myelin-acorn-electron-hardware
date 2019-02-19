/*
 * Copyright (c) 2013-2018, ARM Limited and Contributors. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * https://raw.githubusercontent.com/ARM-software/arm-trusted-firmware/6d4f6aea2cd96a4a57ffa2d88b9230e2cab88f28/lib/libc/memset.c
 */

#include <stddef.h>

void *memset(void *dst, int val, size_t count)
{
	char *ptr = dst;

	while (count--)
		*ptr++ = val;

	return dst;
}
