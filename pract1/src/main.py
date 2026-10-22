import sys

VFS_NAME = "vfs"
MAX_EXIT_ARGS = 1


def parse(line):
    result = line.split()
    if not result:
        return None, []
    return result[0], result[1:]


def cmd_ls(args):
    print("ls", args)


def cmd_cd(args):
    print("cd", args)


def cmd_exit(args):
    if len(args) > MAX_EXIT_ARGS:
        print("exit: too many arguments", file=sys.stderr)
        return

    try:
        code = int(args[0]) if args else 0
    except ValueError:
        print(f"exit: {args[0]}: numeric argument required", file=sys.stderr)
        code = 2

    sys.exit(code)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}


def execute(command, args):
    if command in COMMANDS:
        COMMANDS[command](args)
    else:
        print(f"\033[31m{command}: command not found\033[0m", file=sys.stderr)


def main():
    while True:
        try:
            inpt = input(f"{VFS_NAME}$ ")
            command, args = parse(inpt)
            if not command:
                continue
            execute(command, args)
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
