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
        """
        Gathers code from all files with the specified extensions within the root directory.

        Args:
            extensions (tuple): A tuple of file extensions to include in the code gathering process.
                                 Defaults to Python files (".py").

        Returns:
            dict: A dictionary where keys are file paths and values are the corresponding code content.
        """
        code_dict = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(extensions):
                    filepath = os.path.join(root, file)
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
