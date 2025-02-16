import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FixApplier:
    def apply_fix(self, filename: str, search_block: str, replace_block: str):
        """
        Applies a fix by replacing a search block with a replace block in a given file.
        """
        # Prevent edits to autodev.py
        if os.path.basename(filename) == "autodev.py":
            logging.warning("Skipping modification of autodev.py.")
            return

        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf8') as file:
                    content = file.read()

                # Only replace the first occurrence
                if search_block in content:
                    content = content.replace(search_block, replace_block, 1)

                    with open(filename, 'w', encoding='utf8') as file:
                        file.write(content)

                    logging.info(f"Applied patch to {filename}.")
                else:
                    logging.warning(f"Search block not found in {filename}.")

            except FileNotFoundError:
                logging.error(f"File not found: {filename}")
            except Exception as e:
                logging.error(f"Error applying fix to {filename}: {e}")
        else:
            try:
                with open(filename, 'w', encoding='utf8') as file:
                    file.write(replace_block)
                logging.info(f"Created new file {filename} with initial content.")
            except Exception as e:
                logging.error(f"Error creating new file {filename}: {e}")
