import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # Give the abs path of the working_directory and the directory
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str  = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    except Exception as e:
        return f'Error: {e}'

    # Chack if the target_dir is in working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Chack if the target_dir is a path
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    else:
        # Iterate over the items in the target directory and give info about them
        try:
            info_strings: list[str] = []
            files_dirs: list[str] = os.listdir(target_dir)

            for file_dir_name in files_dirs:
                abs_path: str = os.path.normpath(os.path.join(target_dir, file_dir_name))
                info_strings.append(f"- {file_dir_name}: file_size={os.path.getsize(abs_path)} bytes, is_dir={os.path.isdir(abs_path)}")

            return "\n".join(info_strings)

        except Exception as e:
            return f'Error: {e}'

