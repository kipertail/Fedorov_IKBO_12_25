import argparse
import os
import sys

DEFAULT_VFS_NAME = "vfs"
CONFIG = {}
MAX_EXIT_ARGS = 1


def error(message):
    sys.stdout.flush()
    print(message, file=sys.stderr)


def parse(line):
    result = line.split()
    if not result:
        return None, []
    return result[0], result[1:]


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", help="путь к VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def build_config(args):
    CONFIG["vfs_path"] = args.vfs
    CONFIG["script_path"] = args.script
    if args.vfs:
        name = os.path.splitext(os.path.basename(args.vfs))[0]
        CONFIG["vfs_name"] = name or DEFAULT_VFS_NAME
    else:
        CONFIG["vfs_name"] = DEFAULT_VFS_NAME


def print_config():
    for key, value in CONFIG.items():
        print(f"[config] {key} = {value}")


def prompt():
    return f"{CONFIG['vfs_name']}$ "


def cmd_conf_dump(args):
    if args:
        error("conf-dump: too many arguments")
        return False
    for key, value in CONFIG.items():
        print(f"{key}={value}")
    return True


def cmd_ls(args):
    print("ls", args)
    return True


def cmd_cd(args):
    print("cd", args)
    return True


def cmd_exit(args):
    if len(args) > MAX_EXIT_ARGS:
        error("exit: too many arguments")
        return False

    try:
        code = int(args[0]) if args else 0
    except ValueError:
        error(f"exit: {args[0]}: numeric argument required")
        code = 2

    sys.exit(code)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "conf-dump": cmd_conf_dump,
}


def execute(command, args):
    if command in COMMANDS:
        return COMMANDS[command](args)
    error(f"\033[31m{command}: command not found\033[0m")
    return False


def run_script(path):
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as err:
        error(f"[script] не удалось открыть {path}: {err.strerror}")
        return

    for num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        print(f"{prompt()}{line}")
        command, args = parse(line)
        if not execute(command, args):
            error(f"[script] ошибка в строке {num}: {line}")


def repl():
    while True:
        try:
            line = input(prompt())
            command, args = parse(line)
            if not command:
                continue
            execute(command, args)
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break


def main():
    args = parse_cli_args()
    build_config(args)
    print_config()
    if CONFIG["script_path"]:
        run_script(CONFIG["script_path"])
    repl()


if __name__ == "__main__":
    main()
