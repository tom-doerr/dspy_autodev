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
        Gathers code from all files with the specified extensions within the root directory.

        Args:
            extensions (tuple): A tuple of file extensions to include in the code gathering process.
                                 Defaults to Python files (".py").

        Returns:
            dict: A dictionary where keys are file paths and values are the corresponding code content.
        """
        code_dict = {}
        errors = []
        for file in os.listdir(self.root_dir):
            filepath = os.path.join(self.root_dir, file)
            if os.path.isfile(filepath) and file.endswith(extensions):
                try:
                    with open(filepath, "r", encoding="utf8") as f:
                        code_dict[filepath] = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(filepath, "r", encoding="latin-1") as f:
                            code_dict[filepath] = f.read()
                        logging.warning(f"Successfully read {filepath} with latin-1 encoding.")
                    except Exception as e:
                        error_message = f"Error reading file {filepath}: {e}"
                        logging.error(error_message)
                        errors.append(error_message)
                except Exception as e:
                    error_message = f"Error reading file {filepath}: {e}"
                    logging.error(error_message)
                    errors.append(error_message)
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
