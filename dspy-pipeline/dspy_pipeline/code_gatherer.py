import os
import logging

class CodeGatherer:
    def __init__(self, root_dir="."):
        """
        Initializes the CodeGatherer with a root directory to search for code files.

        Args:
            root_dir (str): The root directory to start the search from. Defaults to the current directory.
        """
        self.root_dir = root_dir

    def gather_code(self, extensions=(".py",)):
        """
        Gathers code from files with the specified extensions within the root directory
        (non-recursively).

        Returns:
            tuple: (code_dict, errors)
                code_dict is a dictionary where keys are file paths and values are file contents.
                errors is a list of error messages.
        """
        code_dict = {}
        errors = []
        try:
            for file in os.listdir(self.root_dir):
                filepath = os.path.join(self.root_dir, file)
                if os.path.isfile(filepath) and file.endswith(extensions):
                    try:
                        with open(filepath, "r", encoding="utf8") as f:
                            code_dict[filepath] = f.read()
                    except Exception as e:
                        logging.error(f"Error reading file {filepath}: {e}")
                        errors.append(str(e))
            return code_dict, errors
        except Exception as e:
            errors.append(str(e))
            return code_dict, errors

    def get_code_for_file(self, filename):
        """
        Retrieves the code content for a specific file.

        Args:
            filename (str): The path to the file.

        Returns:
            str: The code content of the file, or None if the file is not found or an error occurs.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logging.warning(f"File not found: {filename}")
            return None
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            return None
