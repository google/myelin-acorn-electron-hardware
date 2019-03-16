// include sprintf implementation when arcflash pulls in stb_sprintf.h
#define STB_SPRINTF_IMPLEMENTATION

#include "arcflash.h"
#include <stdarg.h>

void display_printf(char const *format, ...) {
  va_list ap;
  va_start(ap, format);
  char buf[500];
  int ret = stbsp_vsnprintf(buf, 500, format, ap);
  if (ret < 0) {
   display_print("printf error");
  } else {
   display_print(buf);
  }
  va_end(ap);
}
