import argparse
import sys
import json
from ckb_g2p.converter import Converter


def main():
    parser = argparse.ArgumentParser(
        description="Central Kurdish Grapheme-to-Phoneme (G2P) Converter"
    )

    # Input argument
    parser.add_argument("text", nargs="?", help="Input Kurdish text to convert")

    # Options
    parser.add_argument("--no-stress", action="store_true", help="Disable stress marking")
    parser.add_argument("--no-cache", action="store_true", help="Disable lexicon cache")
    parser.add_argument("--format", choices=["ipa", "syllables"], default="syllables",
                        help="Output format (default: syllables)")
    parser.add_argument("--normalize", action="store_true", default=True,
                        help="Normalize numbers/dates using ckb-textify (default: True)")

    # Batch processing
    parser.add_argument("-i", "--input-file", help="Read from a file (line by line)")
    parser.add_argument("-o", "--output-file", help="Write to a file")

    args = parser.parse_args()

    # Handle input (Argument vs Stdin)
    input_lines = []
    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                input_lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Error: File '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_lines = [args.text]
    elif not sys.stdin.isatty():
        # Pipe support: echo "text" | python cli.py
        input_lines = [line.strip() for line in sys.stdin if line.strip()]
    else:
        parser.print_help()
        sys.exit(0)

    # Initialize Converter
    try:
        converter = Converter(use_cache=not args.no_cache)
    except Exception as e:
        print(f"❌ Error initializing converter: {e}", file=sys.stderr)
        sys.exit(1)

    # Process
    results = []
    for line in input_lines:
        output_format = args.format if args.format else "syllables"

        # If user wants flat IPA, convert returns list, we join it
        # If user wants syllables, convert returns list of syllable strings

        conversion = converter.convert(
            line,
            output_format=output_format,
            normalize=args.normalize
        )

        if output_format == "ipa":
            res_str = "".join(conversion)
        else:
            res_str = " ".join(conversion)

        results.append(res_str)

    # Output
    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + "\n")
        print(f"✅ Processed {len(results)} lines -> {args.output_file}")
    else:
        for res in results:
            print(res)


if __name__ == "__main__":
    main()