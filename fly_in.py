import sys
from parser import main_parser


def main() -> None:

    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        print(
            "[ERROR] -> Usage: python fly_in.py <file.txt> "
        )
        sys.exit(1)

    fd = sys.argv[1]
    main_parser(fd)


if __name__ == "__main__":
    main()
