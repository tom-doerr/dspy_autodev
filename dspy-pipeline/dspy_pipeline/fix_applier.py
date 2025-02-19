import os
import logging
from rich.console import Console

console = Console()

class FixApplier:
    def apply_fix(self, filename: str, search_block: str, replace_block: str):
        """
        Applies a fix by replacing a search block with a replace block in a given file.
        """
        # Prevent edits to autodev.py
        if os.path.basename(filename) == "autodev.py":
            console.print("[red]Skipping modification of autodev.py. Please fix autodev.py manually.[/red]")
            return

        if os.path.exists(filename):
            try:
                import re
                with open(filename, "r", encoding="utf8") as f:
                    content = f.read()
                search_clean = search_block.strip()
                if replace_block.lstrip().startswith('@@'):
                    import diff_match_patch as dmp_module
                    dmp = dmp_module.diff_match_patch()
                    patches = dmp.patch_fromText(replace_block)
                    new_content, results = dmp.patch_apply(patches, content)
                    if all(results):
                        with open(filename, "w", encoding="utf8") as f:
                            f.write(new_content)
                        console.print(f"[green]Applied patch to {filename} using diff-match-patch.[/green]")
                    else:
                        console.print(f"[red]Patch could not be fully applied to {filename}.[/red]")
                elif replace_block.lstrip().startswith('['):
                    import json
                    import jsonpatch
                    try:
                        patch_obj = json.loads(replace_block)
                    except Exception as err:
                        console.print(f"[red]Failed to parse JSON patch: {err}[/red]")
                        return
                    try:
                        json_content = json.loads(content)
                        new_json = jsonpatch.apply_patch(json_content, patch_obj)
                        new_content = json.dumps(new_json, indent=2)
                        with open(filename, "w", encoding="utf8") as f:
                            f.write(new_content)
                        console.print(f"[green]Applied JSON patch to {filename} using jsonpatch.[/green]")
                    except Exception as err:
                        try:
                            if isinstance(patch_obj, list) and len(patch_obj) == 1 and \
                               patch_obj[0].get("op") == "add" and patch_obj[0].get("path") == "/-":
                                new_content = patch_obj[0].get("value", "")
                                with open(filename, "w", encoding="utf8") as f:
                                    f.write(new_content)
                                console.print(f"[green]Created or replaced {filename} using JSON patch fallback.[/green]")
                                return
                        except Exception as inner_err:
                            console.print(f"[red]Fallback failed: {inner_err}[/red]")
                        console.print(f"[red]Failed to apply JSON patch to {filename}: {err}[/red]")
                        return
                else:
                    if search_clean in content:
                        new_content = content.replace(search_clean, replace_block, 1)
                        count = 1
                    else:
                        pattern = re.compile(r'(\s*)' + re.escape(search_clean) + r'(\s*)')
                        new_content, count = re.subn(pattern, lambda m: m.group(1) + replace_block + m.group(2), content, count=1)
                    if count:
                         logging.info(f"Replacement count: {count}, new content for {filename}: {new_content}")
                         with open(filename, "w", encoding="utf8") as f:
                              f.write(new_content)
                         console.print(f"[green]Applied patch to {filename}.[/green]")
                    else:
                         console.print(f"[red]No matching search block found in {filename}. Patch not applied.[/red]")
            except FileNotFoundError:
                logging.error(f"File not found: {filename}")
            except Exception as e:
                logging.error(f"Error applying fix to {filename}: {e}")
        else:
            try:
                with open(filename, 'w', encoding='utf8') as file:
                    file.write(replace_block)
                console.print(f"[blue]Created new file {filename}.[/blue]")
            except Exception as e:
                logging.error(f"Error creating new file {filename}: {e}")
