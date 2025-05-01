# Risc OS ROM Tools

Tools to mess with RISC OS ROM images.

- extract_modules.py: Extract kernel and modules from a ROM image.
  - Writes a list of module names as `module_list.txt`, and writes modules into `modules/`.
- find_source_folders_by_module.py: Parse RISC OS 3.71 Makefile to find source folders for modules.
  - Writes `module_to_source_mapping.json`.