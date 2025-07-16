import os
import textwrap
from utils import *
from defaults import *

GET_DIR_EXCL_TEMPLATE = """
Lemma getDir_%s:
  forall idx dir,
    getDir idx dir = %s ->
    dir.(d_st) = %s /\ dir.(d_excl) = idx.
Proof.
  unfold getDir, caseDec; intros.
  find_if_inside; [find_if_inside; [auto|discriminate]|].
  repeat (find_if_inside; [find_if_inside; discriminate|]).
  discriminate.
Qed.
""" % ((STATE_EXCL,) * 3)

FACT_TEMPLATES = [GET_DIR_EXCL_TEMPLATE]

def wrap_fact(template):
    if SHOW_PROOF:
        in_proof = False
        modified_lines = []
        lines = template.split('\n')
        for line in lines:
            if line.strip() == "Proof.":
                in_proof = True
                modified_lines.append(line)
                modified_lines.append(f"{' ' * DEFAULT_INDENT}Show Proof.")
            elif line.strip() == "Qed.":
                in_proof = False
                modified_lines.append(line)
            else:
                if in_proof:
                    modified_lines.append(line)
                    modified_lines.append(f"{' ' * DEFAULT_INDENT}Show Proof.")
                else:
                    modified_lines.append(line)
        template = '\n'.join(modified_lines)
    return textwrap.indent(template, ' ' * DEFAULT_INDENT)

def gen_fact(output_path, target_name):
    dsl_output = f'\nSection Facts.\n'
    for i in FACT_TEMPLATES:
        fact = wrap_fact(i)
        dsl_output += fact
    dsl_output += f'\nEnd Facts.\n'
    path = os.path.join(output_path, target_name)
    with open(path, 'a') as output_file:
        output_file.write(dsl_output)
