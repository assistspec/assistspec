import os
import sys
import fact
import hemiola
import argparse
from utils import *
from defaults import *

def gen():
    parser = argparse.ArgumentParser(description='Generate a specialized specification.')

    parser.add_argument('-f', '--format', choices=['hemiola'], required=True,
                        help='Specify the format. Choices are: hemiola, ...')

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Specify the input path')

    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Specify the output path')
    
    parser.add_argument('-t', '--target', type=str, required=True,
                        help='Specify the target name')
    
    args = parser.parse_args()
    if not args.input:
        raise ValueError("Input path is not specified.")
    if not args.output:
        raise ValueError("Output path is not specified.")
    if not args.target:
        raise ValueError("Target is not specified.")
    
    spec_format = args.format if args.format else 'hermiola'
    spec_name = f'{SPEC.format(target=args.target)}.v'
    target_name = f'{args.target}.v'
    reserved_files = [spec_name, target_name]
    if spec_format == 'hemiola':
        if os.path.isdir(args.input) and os.path.isdir(args.output):
            components = []
            for i in os.listdir(args.input):
                if i in reserved_files:
                    raise ValueError(f"File {i} is reserved.")
                if i.endswith('.json'):
                    input_file = os.path.join(args.input, i)
                    dsl = hemiola.convert(input_file)
                    components.append(dsl)
            if components:
                hemiola.gen_spec(args.input, args.output, spec_name)
                hemiola.gen_target(components, args.output, target_name)
            fact.gen_fact(args.output, target_name)
        else:
            ValueError("Iutput/output path is invalid.")

if __name__ == '__main__':
    if DEBUG:
        gen()
    else:
        try:
            gen()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
