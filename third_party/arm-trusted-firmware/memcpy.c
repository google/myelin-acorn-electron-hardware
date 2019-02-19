/*
 * Copyright (c) 2013-2018, ARM Limited and Contributors. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * https://raw.githubusercontent.com/ARM-software/arm-trusted-firmware/6d4f6aea2cd96a4a57ffa2d88b9230e2cab88f28/lib/libc/memcpy.c
 */

#include <stddef.h>

void *memcpy(void *dst, const void *src, size_t len)
{
	const char *s = src;
	char *d = dst;

	while (len--)
		*d++ = *s++;

	return dst;
}
