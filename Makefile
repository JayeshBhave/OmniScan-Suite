# Makefile

# Define variables
SCRIPT_NAME = omniscan.py
INSTALL_DIR = /usr/local/bin

# Default target
all:
	@echo "Usage: make install (to install the tool)"

# Install target
install:
	cp $(SCRIPT_NAME) $(INSTALL_DIR)/$(SCRIPT_NAME)
	chmod +x $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "Installed $(SCRIPT_NAME) to $(INSTALL_DIR)"
