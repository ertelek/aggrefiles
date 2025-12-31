from pathlib import Path
import argparse
import pathspec
import sys


def aggregate_files(root: Path,
                    ext: str,
                    output: Path,
                    gitignore_spec=None) -> int:
    """
    Aggregate all files under `root` (recursively) whose suffix matches `ext`
    into the `output` file.

    For each file:
      - write its path relative to `root`
      - write its contents
      - write a horizontal line of dashes

    If `gitignore_spec` is provided (a pathspec.PathSpec instance), any file
    matching that spec will be skipped.
    """
    root = root.resolve()
    output = output.resolve()
    ext = ext.lower()

    files = []
    for path in root.rglob("*"):
        # Skip anything that matches the gitignore spec
        if gitignore_spec is not None:
            rel_path_str = path.relative_to(root).as_posix()
            if gitignore_spec.match_file(rel_path_str):
                continue

        if path.is_file() and path.suffix.lower() == ext:
            # Avoid aggregating the output file into itself
            if path.resolve() == output:
                continue
            files.append(path)

    files.sort()

    if not files:
        print(f"No files with extension '{ext}' found under {root}",
              file=sys.stderr)
        return 0

    separator = "-" * 80

    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8", errors="replace") as out_f:
        for file_path in files:
            rel_path = file_path.relative_to(root).as_posix()
            out_f.write(rel_path + "\n")
            try:
                content = file_path.read_text(encoding="utf-8",
                                              errors="replace")
            except Exception as exc:  # pragma: no cover - defensive
                content = f"[Error reading file: {exc}]"

            out_f.write(content)
            if not content.endswith("\n"):
                out_f.write("\n")
            out_f.write(separator + "\n\n")

    print(f"Aggregated {len(files)} file(s) into {output}")
    return len(files)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog="aggrefiles",
        description=
        "Aggregate files with a given extension into a single file.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to search (default: current directory).",
    )
    parser.add_argument(
        "-e",
        "--ext",
        default=".txt",
        help=
        "File extension to match, with or without leading dot (default: .txt).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=
        "Output file path. Default: aggregated<ext> in the root directory.",
    )
    parser.add_argument(
        "-g",
        "--gitignore",
        default=".gitignore",
        help=
        ("Path to a .gitignore-style file. Any file or folder matching one of its "
         "patterns will be skipped. Uses gitwildmatch semantics (requires the "
         "'pathspec' package)."),
    )

    args = parser.parse_args(argv)
    root = Path(args.root)

    ext = args.ext
    if not ext.startswith("."):
        ext = "." + ext

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = root / out_path
    else:
        # e.g., aggregated.txt
        out_path = root / f"aggregated{ext}"

    gitignore_spec = None
    if args.gitignore:
        gitignore_path = Path(args.gitignore)
        if not gitignore_path.is_absolute():
            gitignore_path = root / gitignore_path

        if gitignore_path.is_file():
            with gitignore_path.open("r", encoding="utf-8",
                                     errors="replace") as f:
                gitignore_spec = pathspec.PathSpec.from_lines(
                    "gitwildmatch", f)
        else:
            print(
                f"Warning: gitignore file not found at {gitignore_path}, "
                "continuing without it.",
                file=sys.stderr,
            )
    else:
        print("No gitignore file specified, continuing without it.",
              file=sys.stderr)

    try:
        aggregate_files(root, ext, out_path, gitignore_spec=gitignore_spec)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
