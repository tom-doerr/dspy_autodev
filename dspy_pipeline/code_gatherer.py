import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeGatherer:
    def __init__(self, root_dir="."):
        """
        Initializes the CodeGatherer with a root directory to search for code files.

        Args:
            root_dir (str): The root directory to start the search from. Defaults to the current directory.
        """
        self.root_dir = root_dir

    def gather_code(self, extensions=(".py",)):
        code_dict = {}
        for file in os.listdir(self.root_dir):
            if file.endswith(extensions):
                filepath = os.path.join(self.root_dir, file)
                filepath = os.path.abspath(filepath)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code_dict[filepath] = f.read()
                except Exception as e:
                    logging.error(f"Error reading file {filepath}: {e}")
        return code_dict

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
            logging.error(f"File not found: {filename}")
            return None
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            return None
