import json
import textwrap
from utils import *
from verbose import *
from defaults import *
from itertools import product

GET_IDX_TEMPLATE = {
  REQ_NODE: '(index_of (objIdxOf (idOf idm)) (append_to ost#[dir].(d_reqs) (objIdxOf (idOf idm))))',
  HOME_NODE: '(index_of (objIdxOf rsbTo) (append_to ost#[dir].(d_reqs) (objIdxOf rsbTo)))',
  SLAVE_NODE: '(index_of (objIdxOf rsbTo) (append_to ost#[dir].(d_reqs) (objIdxOf rsbTo)))'
}

RULE = {
    REQ_NODE: {
        CLS_REQ: {
            TEMPLATE: 'rquu',
            TRIG    : """receive {trigger} from cidx to oidx""",
            ASSERT  : """fun ost mins => ost#[status] <= {status}""",
            HNDLR   : """!|ost, msg| --> <| {msg_type}; O |>"""
        },
        CLS_RSP: {
            REQ_NODE: {
                SND: {
                    TEMPLATE: 'immu',
                    TRIG    : """receive {trigger} to oidx""",
                    ASSERT  : """fun ost orq mins => {condition}""",
                    HNDLR   : """!|ost, min| -->({ost}, <| {msg_type}; O |>)"""
                },
                SCH: {
                    TEMPLATE: 'rsudo',
                    HLD     : """{hold}""",
                    TRIG    : """receive {trigger}""",
                    ASSERT  : """fun ost => {condition}""",
                    HNDLR   : """!|ost, idm, rq, rsbTo| --> ({ost}, <| {msg_type}; %s |>)""" % GET_IDX_TEMPLATE[REQ_NODE]
                },
                RCV: {
                    TEMPLATE: 'rsdd',
                    HLD     : 'Spec.getRq',
                    TRIG    : """receive {trigger}""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, min, rq, rsbTo| --> ({ost}, <| Spec.getRs; O |>)"""
                }
            },
            HOME_NODE: {
                SND: {
                    TEMPLATE: 'rqsu',
                    TRIG    : 'to oidx',
                    ASSERT  : 'fun ost => ost#[dir].(d_pend) <> nil',
                    HNDLR   : """ost --> <| {msg_type}; head_of ost#[dir].(d_pend) |>"""
                },
                SCH: {
                    TEMPLATE: 'immd',
                    TRIG    : """receive {trigger} from cidx""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, msg| --> (ost +#[dir <- rm_req (msg_value msg) ost#[dir]], <| {msg_type}; O |>)"""
                },
                RCV: {
                    TEMPLATE: 'rsds',
                    TRIG    : """receive {trigger}""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, _| --> (ost +#[dir <- rm_pend ost#[dir]])"""
                }
            },
            SLAVE_NODE: {
                SND: {
                },
                SCH: {
                },
                RCV: {
                }
            }
        }
    },
    HOME_NODE: {
        CLS_REQ: {
            'Read_I_I_I': {
                TEMPLATE: 'rquu',
                TRIG    : """receive {trigger} from cidx to oidx""",
                ASSERT  : """fun ost mins => ost#[status] = {st_home} /\\ ost#[dir].(d_st) = {st_other}""",
                HNDLR   : """!|ost, msg| --> <| {msg_type}; O |>"""
            },
            'Read_I_UC_I': {
                TEMPLATE: 'rqud',
                TRIG    : """receive {trigger} from cidx to oidx""",
                ASSERT  : """fun ost mins => ost#[status] = {st_home} /\\ ost#[dir].(d_st) = {st_other}""",
                HNDLR   : """!|ost, msg| --> ([ost#[dir].(d_excl)], <| {msg_type}; O |>)"""
            }
        },
        CLS_RSP: {
            REQ_NODE: {
                SND: {
                    TEMPLATE: 'immd',
                    TRIG    : """receive {trigger} from cidx""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, msg| --> (ost, <| {msg_type}; O |>)"""
                },
                SCH: {
                    TEMPLATE: 'rsdd',
                    TRIG    : """receive {trigger}""",
                    HLD     : """{hold}""",
                    ASSERT  : """fun ost orq mins => {condition}""",
                    HNDLR   : """!|ost, mins, rq, rsbTo| -->({ost}, <| {msg_type}; %s |>)""" % GET_IDX_TEMPLATE[HOME_NODE]
                },
                RCV: {
                    TEMPLATE: 'rsdd',
                    TRIG    : """receive {trigger}""",
                    HLD     : 'Spec.getRq',
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, min, rq, rsbTo| --> (ost +#[dir <- add_pend (msg_value min) ost#[dir]], <| Spec.getRs; O |>)"""
                }
            },
            HOME_NODE: {
                SND: {
                    TEMPLATE: 'rsudo',
                    TRIG    : """receive {trigger}""",
                    HLD     : """{hold}""",
                    ASSERT  : 'fun ost => {condition}',
                    HNDLR   : """!|ost, idm, rq, rsbTo| --> ({ost}, <| {msg_type}; O |>)"""
                },
                SCH: {
                },
                RCV: {
                }
            },
            SLAVE_NODE: {
                SND: {
                },
                SCH: {
                },
                RCV: {
                }
            }
        }
    },
    SLAVE_NODE: {
        CLS_RSP: {
            REQ_NODE: {
                SND: {
                    TEMPLATE: 'immd',
                    TRIG    : """receive {trigger} from cidx""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, msg| --> ({ost}, <| {msg_type}; O |>)"""
                },
                SCH: {
                    TEMPLATE: 'rsdd',
                    TRIG    : """receive {trigger}""",
                    HLD     : """{hold}""",
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, min, rq, rsbTo| --> ({ost}, <| {msg_type}; %s |>)""" % GET_IDX_TEMPLATE[SLAVE_NODE]
                },
                RCV: {
                    TEMPLATE: 'rsdd',
                    TRIG    : """receive {trigger}""",
                    HLD     : 'Spec.getRq',
                    ASSERT  : 'fun _ _ _ => True',
                    HNDLR   : """!|ost, min, rq, rsbTo| --> (ost +#[dir <- add_pend (msg_value min) ost#[dir]], <| Spec.getRs; O |>)"""
                }
            },
            HOME_NODE: {
                SND: {
                },
                SCH: {
                },
                RCV: {
                }
            }
        }
    }
}

RULE_IDX = {
    REQ_NODE  : {CAT: 0, MAJOR: 0, MINOR: 0}, 
    HOME_NODE : {CAT: 0, MAJOR: 1, MINOR: 0},
    SLAVE_NODE: {CAT: 0, MAJOR: 2, MINOR: 0}
}

RULE_INDEX_TEMPLATE = """{category}~>{major}~>{minor}"""

RN_DEFAULT_REQUEST = 'Spec.getRq'

RN_REQUEST_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    assert ({assertion});
    ({handler})
  }}.
"""

RN_RESPONSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    assert ({assertion});
    ({handler})
  }}.
"""

RN_RESPONSE_TRAVERSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    hold {hold};
    assert ({assertion});
    ({handler})
  }}.
"""

HN_REQUEST_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    assert ({assertion});
    ({handler})
  }}.
"""

HN_RESPONSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    assert ({assertion});
    ({handler})
  }}.
"""

HN_RESPONSE_TRAVERSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    hold {hold};
    assert ({assertion});
    ({handler})
  }}.
"""

SN_RESPONSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    assert ({assertion});
    ({handler})
  }}.
"""

SN_RESPONSE_TRAVERSE_TEMPLATE = """
Definition {rule_name}: Rule :=
  rule {rule_index} from template {template_name} {{
    {trigger};
    hold {hold};
    assert ({assertion});
    ({handler})
  }}.
"""

STATE_TEMPLATE = """\nDefinition {state_name}: nat := {state_value}."""

SET_EXCL_TEMPLATE = {
    REQ_NODE: """ost +#[owned <- false] +#[status <- {target_status}]""",
    FWD_NODE: """ost +#[dir <- setDir{target_status} (objIdxOf (idOf idm)) (append_to ost#[dir].(d_reqs) (objIdxOf (idOf idm)))]""",
    SLAVE_NODE:  """ost +#[dir <- setDir{target_status} (objIdxOf rsbTo) (append_to ost#[dir].(d_reqs) (objIdxOf rsbTo))]"""
}

SET_SHARED_TEMPLATE = {
    REQ_NODE: """ost +#[status <- {target_status}]""",
    FWD_NODE: """ost +#[dir <- setDir{target_status} [objIdxOf rsbTo; objIdxOf (idOf idm)] (append_to ost#[dir].(d_reqs) (objIdxOf (idOf idm)))]""",
    HOME_NODE: """ost +#[dir <- setDir{target_status} (append_to ost#[dir].(d_sharers) (objIdxOf rsbTo)) (append_to ost#[dir].(d_reqs) (objIdxOf rsbTo))]"""
}

GET_DIR_TEMPLATE = """
Definition getDir (idx: %s) (dir: %s): %s :=
  match case dir.(d_st) on eq_nat_dec default %s with
  {state_cases}
  end.
""" % (IDX_TYPE, DIR_TYPE, STATE_TYPE, STATE_INVALID)

SET_DIR_TEMPLATE = """
Definition setDir (state: %s) (exclOpt: option %s) (sharersOpt: option (list %s)) (reqs: list %s) (pend: list nat): %s :=
  let final_excl := match exclOpt with
                    | Some excl => excl
                    | None => 0
                    end in
  let final_sharers := match sharersOpt with
                       | Some sharers => sharers
                       | None => nil
                       end in
  {| d_st := state;
     d_excl := final_excl;
     d_sharers := final_sharers;
     d_reqs := reqs;
     d_pend := pend |}.
""" % (STATE_TYPE, IDX_TYPE, IDX_TYPE, IDX_TYPE, DIR_TYPE)

SET_STATE_TEMPLATE = """
Definition setDir{state_name} {arg_list} (reqs: list %s): %s :=
  setDir {state_name} {real_arg_list} reqs nil.
""" % (IDX_TYPE, DIR_TYPE)

MSG_TEMPLATE = """\nDefinition {msg}: %s := {cls}~>{num}.""" % IDX_TYPE

VARIABLE_TEMPLATE = """
Variables (oidx cidx: %s).
""" % IDX_TYPE

TYPE_TEMPLATE = """
Definition %s: Type := nat.

Record %s := {
  d_st: %s;
  d_excl: %s;
  d_sharers: list %s;
  d_reqs: list %s;
  d_pend: list nat
}.

Definition val: Fin.t 4 := F1.
Definition owned: Fin.t 4 := F2.
Definition status: Fin.t 4 := F3.
Definition dir: Fin.t 4 := F4.
Definition default_state: %s := 0.
""" % (STATE_TYPE, DIR_TYPE, STATE_TYPE, IDX_TYPE, IDX_TYPE, IDX_TYPE, STATE_TYPE)

HELPER_FUNC_TEMPLATE = """
Fixpoint get_pos_aux (x : %s) (l : list %s) (current_index : nat) : nat :=
  match l with
  | nil => 0
  | cons y ys => if idx_dec x y then current_index else get_pos_aux x ys (S current_index)
  end.

Definition get_pos (x : %s) (l : list %s) : nat :=
  get_pos_aux x l 0.

Definition index_of (item : %s) (l : list %s) : nat :=
  get_pos item l.

Fixpoint remove_at {A: Type} (n : nat) (l : list A) : list A :=
  match n, l with
  | 0, cons _ xs => xs
  | S n', cons x xs => cons x (remove_at n' xs)
  | _, _ => l
  end.

Fixpoint append_to {A: Type} (l : list A) (x : A) : list A :=
  match l with
  | nil => [x]
  | cons y ys => cons y (append_to ys x)
  end.

Definition head_of (l : list nat) : nat :=
  match l with
  | nil => 0
  | cons x _ => x
  end.

Definition pop_first {A: Type} (l : list A) : list A :=
  match l with
  | nil => nil
  | cons x xs => xs
  end.

Definition rm_req (idx: nat) (dir: %s) : %s := 
  {| d_st := dir.(d_st);
     d_excl := dir.(d_excl);
     d_sharers := dir.(d_sharers);
     d_reqs := remove_at idx dir.(d_reqs);
     d_pend := dir.(d_pend) |}.

Definition rm_pend (dir: %s) : %s :=
  {| d_st := dir.(d_st);
     d_excl := dir.(d_excl);
     d_sharers := dir.(d_sharers);
     d_reqs := dir.(d_reqs);
     d_pend := pop_first dir.(d_pend) |}.

Definition add_pend (idx: nat) (dir: %s): %s :=
  {| d_st := dir.(d_st);
     d_excl := dir.(d_excl);
     d_sharers := dir.(d_sharers);
     d_reqs := dir.(d_reqs);
     d_pend := append_to dir.(d_pend) idx |}.
""" % ((IDX_TYPE,) * 6 + (DIR_TYPE,) * 6)

HEADER_TEMPLATE = [
    'Require Import Bool Vector List String Peano_dec Lia.',
    'Require Import Common FMap HVector IndexSupport Syntax Semantics.',
    'Require Import Topology RqRsTopo.',
    'Require Import RqRsLang.',
    'Import RqRsNotations.',
    'Require Import Ex.Spec Ex.SpecInds Ex.Template.',
    'Import RuleTemplateNotations.',
    'Set Implicit Arguments.',
    'Local Open Scope list.',
    'Local Open Scope hvec.',
    'Local Open Scope fmap.'
]

SPEC_HEADER_TEMPLATE = [
    'Require Import Bool Vector List String Peano_dec Lia.',
    'Require Import Common FMap HVector IndexSupport Syntax Semantics.',
    'Require Import Topology RqRsTopo.',
    'Require Import RqRsLang.',
    'Require Import Ex.Spec Ex.SpecInds Ex.Template.',
    'Import RuleTemplateNotations.',
    'Import CaseNotations.',
    'Set Implicit Arguments.'
]

SYSTEM_TEMPLATE = """
Variable (tr: tree).
Variables (oidx cidx: IdxT).
Hypothesis (Htr: tr <> Node nil).
Let topo := fst (tree2Topo tr 0).
Let cifc := snd (tree2Topo tr 0).
"""

STATUS_COND_TEMPLATE = """ost#[status] = {status}"""

INSTANCE_TEMPLATE = 'Instance ImplOStateIfc: OStateIfc := {| ost_ty := [nat:Type; bool:Type; ' + STATE_TYPE + ':Type; ' + DIR_TYPE + ':Type]%vector |}.'

IMPORT_TEMPLATE = """Require Import Ex.{name}."""

RULE_TYPES = {}

def regulate_name(name):
    return name.replace('-', '')

def get_rule_num(src, dst, msg_type, status):
    key = f'{src}-{dst}-{msg_type}-{status}'
    if key not in RULE_TYPES:
        RULE_TYPES[key] = 0
    else:
        RULE_TYPES[key] = RULE_TYPES[key] + 1
    return RULE_TYPES[key]

def get_rule_index(grp):
    major = RULE_IDX[grp][MAJOR]
    minor = RULE_IDX[grp][MINOR]
    RULE_IDX[grp][MINOR] = minor + 1
    category = RULE_IDX[grp][CAT]
    return category, major, minor

def get_req_rule(src, dst, others, perm):
    return f'{perm}_{src}_{others}_{dst}'

def get_rule_name(category, src, dst, msg_type, rule_num, status=None):
    category, src, dst, dst, msg_type, rule_num = map(lambda i: regulate_name(i) if type(i) == str else i, [category, src, dst, dst, msg_type, rule_num])
    if not status:
        return f'C{category}_{src}_{dst}_{msg_type}_{rule_num}'
    else:
        return f'C{category}_{src}_{dst}_{status}_{msg_type}_{rule_num}'

def get_name(content):
    name = list(content.keys())[0] if type(content) == dict else content
    if type(name) == str:
        return name.replace('-', '')
    elif type(name) == list:
        ret = []
        for i in name:
            if type(i) != dict:
                err(f'Invalid content {content}')
            ret.append(get_name(i))
        return '_'.join(ret)

def unfold_dict(input_dict, name):
    result = []
    primary_key = list(input_dict.keys())[0]
    primary_key_values = input_dict[primary_key]
    if type(primary_key_values) == dict:
        primary_key_values = [primary_key_values]
    for item in primary_key_values:
        primary_value = item.get(primary_key)
        if not isinstance(primary_value, list):
            primary_value = [primary_value]
        other_keys = [key for key in item.keys() if key != primary_key]
        other_values = [item[key] if isinstance(item[key], list) else [item[key]] for key in other_keys]
        for values in product(*other_values):
            new_item = {name: primary_key}
            for i, key in enumerate(other_keys):
                new_item[key] = values[i]
            result.append(new_item)
    return result

def get_st(status, name):
    res = unfold_dict(status, name) if type(status) == dict else {}
    for st in res:
        for i in st:
            if st[i] not in STATES:
                err(f'Invalid state {st[i]}')
    return res

def get_transition(trans):
    if type(trans) != dict or len(trans) != 1:
        err(f'Invalid transition {trans}')
    st_old = list(trans.keys())[0]
    st_new = trans[st_old]
    if type(st_new) != str:
        err(f'Invalid transition {st_new}')
    return [st_old], st_new

def get_status(item):
    if TRANS in item and type(item[TRANS]) == dict:
        return get_transition(item[TRANS])
    elif STAT in item:
        if type(item[STAT]) not in [list, str]:
            err(f'Invalid status {item[STAT]}')
        if UPDATE in item:
            return (item[STAT], item[UPDATE]) if type(item[STAT]) == list else ([item[STAT]], item[UPDATE])
        else:
            return (item[STAT], None) if type(item[STAT]) == list else ([item[STAT]], None)
    else:
        return [], None

def get_rsp_rules(grp, dst=None):
    if not dst:
        return RULE[grp][CLS_RSP][grp]
    else:
        if is_sn(dst):
            return RULE[grp][CLS_RSP][SLAVE_NODE]
        elif is_hn(dst):
            return RULE[grp][CLS_RSP][HOME_NODE]
        elif is_rn(dst):
            return RULE[grp][CLS_RSP][REQ_NODE]
        else:
            err(f'Invalid groug {grp}')

def get_ost(grp, target_status):
    if target_status == STATE_EXCL:
        return SET_EXCL_TEMPLATE[grp].format(target_status=target_status)
    elif target_status == STATE_SHARED:
        return SET_SHARED_TEMPLATE[grp].format(target_status=target_status)
    else:
        return 'ost'
    
def get_msg_type(msg):
    assert(type(msg) == dict)
    return list(msg.keys())[0]

def get_perm(item):
    perm = item.get(PERM)
    if perm not in PERMISSIONS:
        err(f'Invalid permission {perm}')
    return perm

def is_rn(name):
    return name.startswith(PREFIX[REQ_NODE])

def is_hn(name):
    return name.startswith(PREFIX[HOME_NODE])

def is_sn(name):
    return name.startswith(PREFIX[SLAVE_NODE])

def convert_rn_requests(requests):
    output = ''
    for msg in requests:
        msg_type = get_msg_type(msg)
        request = msg[msg_type]
        src = get_name(request[SRC])
        if is_rn(src):
            dst = get_name(request[DST])
            st = request[STAT] if type(request[STAT]) == list else [request[STAT]]
            for status in st:
                category, major, minor = get_rule_index(REQ_NODE)
                rule_num = get_rule_num(src, dst, msg_type, status)
                rule_name = get_rule_name(category, src, dst, msg_type, rule_num, status)
                rule_index = RULE_INDEX_TEMPLATE.format(category=category, major=major, minor=minor)
                template_name = RULE[REQ_NODE][CLS_REQ][TEMPLATE]
                trigger = get_name(request[TRIG]) if TRIG in request else RULE[REQ_NODE][CLS_REQ][TRIG].format(trigger=RN_DEFAULT_REQUEST)
                assertion = RULE[REQ_NODE][CLS_REQ][ASSERT].format(status=status)
                handler = RULE[REQ_NODE][CLS_REQ][HNDLR].format(msg_type=msg_type)
                rule_template = RN_REQUEST_TEMPLATE.format(
                    rule_name=rule_name,
                    rule_index=rule_index,
                    template_name=template_name,
                    trigger=trigger,
                    assertion=assertion,
                    handler=handler
                )
                rule = textwrap.indent(rule_template, ' ' * SUB_SECTION_INDENT)
                output += rule
    return output

def convert_rn_responses(responses):
    output = ''
    for msg in responses:
        msg_type = get_msg_type(msg)
        response = msg[msg_type]
        src = get_name(response[SRC])
        if is_rn(src):
            dst = get_name(response[DST])
            trig = get_name(response[TRIG]) if TRIG in response else msg_type
            fold = response.get(FOLD)
            rules = get_rsp_rules(REQ_NODE, dst) if not fold else get_rsp_rules(REQ_NODE)
            for rule_type in rules:
                rule_content = rules[rule_type]
                if rule_content:
                    if fold and type(response[DST]) == list and rule_type != SND:
                        resp = None
                        if rule_type in [SCH, RCV]:
                            for item in response[DST]:
                                if type(item) != dict:
                                    err(f'Invalid content {item}')
                                name = list(item.keys())[0]
                                if (is_hn(name) and rule_type == SCH) or (is_rn(name) and rule_type == RCV):
                                    resp = item[name]
                                    break
                        if not resp:
                            err(f'Invalid destinition {dst}')
                        st, trans = get_status(resp)
                        hld = resp.get(HLD)
                    else:
                        st, trans = get_status(response) if rule_type == SND else ([], None)
                        hld = response.get(HLD)
                    for status in st:
                        category, major, minor = get_rule_index(REQ_NODE)
                        rule_index = RULE_INDEX_TEMPLATE.format(category=category, major=major, minor=minor)
                        template_name = rule_content[TEMPLATE] if FOLD not in rule_content or FOLD not in response else rule_content[FOLD] 
                        msg = response[FOLD] if fold and rule_type == SCH else msg_type
                        trigger = rule_content[TRIG].format(trigger=trig if rule_type == SND else msg_type if not fold or rule_type != RCV else fold)
                        condition = STATUS_COND_TEMPLATE.format(status=status) if status else 'True'
                        assertion = rule_content[ASSERT].format(condition=condition)
                        ost = get_ost(REQ_NODE if rule_type != SCH else FWD_NODE, trans)
                        handler = rule_content[HNDLR].format(msg_type=msg, ost=ost) if HNDLR in rule_content else None
                        hold = rule_content[HLD].format(hold=hld if hld != None else trig) if HLD in rule_content else None
                        template = RN_RESPONSE_TRAVERSE_TEMPLATE if hold else RN_RESPONSE_TEMPLATE
                        rule_num = get_rule_num(src, dst, msg_type, status)
                        rule_name = get_rule_name(category, src, dst, msg_type, rule_num, status)
                        rule_template = template.format(
                            rule_name=rule_name,
                            rule_index=rule_index,
                            template_name=template_name,
                            trigger=trigger,
                            hold=hold,
                            assertion=assertion,
                            handler=handler
                        )
                        rule = textwrap.indent(rule_template, ' ' * SUB_SECTION_INDENT)
                        output += rule
    return output

def convert_hn_requests(requests):
    output = ''
    for msg in requests:
        msg_type = get_msg_type(msg)
        request = msg[msg_type]
        src = get_name(request[SRC])
        if is_hn(src):
            dst = get_name(request[DST])
            trig = get_name(request[TRIG]) if TRIG in request else ''
            if not trig:
                err(f'No trigger of {msg_type} for {HOME_NODE}')
            category, major, minor = get_rule_index(HOME_NODE)
            for st in get_st(request[STAT], HOME):
                if type(st) != dict:
                    err(f'Invalid status of {HOME_NODE} requst {msg_type}')
                st_req = st[REQ]
                st_home = st[HOME]
                st_other = st[OTHER]
                status = f'{st_req}_{st_home}_{st_other}'
                rule_num = get_rule_num(src, dst, msg_type, status)
                rule_name = get_rule_name(category, src, dst, msg_type, rule_num, status)
                rule_index = RULE_INDEX_TEMPLATE.format(category=category, major=major, minor=minor)
                req_rule = get_req_rule(st_req, st_home, st_other, get_perm(request))
                template_name = RULE[HOME_NODE][CLS_REQ][req_rule][TEMPLATE]
                trigger = RULE[HOME_NODE][CLS_REQ][req_rule][TRIG].format(trigger=trig)
                assertion = RULE[HOME_NODE][CLS_REQ][req_rule][ASSERT].format(st_home=st_home, st_other=st_other)
                handler = RULE[HOME_NODE][CLS_REQ][req_rule][HNDLR].format(msg_type=msg_type)
                rule_template = HN_REQUEST_TEMPLATE.format(
                    rule_name=rule_name,
                    rule_index=rule_index,
                    template_name=template_name,
                    trigger=trigger,
                    assertion=assertion,
                    handler=handler
                )
                rule = textwrap.indent(rule_template, ' ' * SUB_SECTION_INDENT)
                output += rule
    return output

def convert_hn_responses(responses):
    output = ''
    for msg in responses:
        msg_type = get_msg_type(msg)
        response = msg[msg_type]
        src = get_name(response[SRC])
        if is_hn(src):
            dst = get_name(response[DST]) if DST in response else src
            hld = response.get(HLD)
            trig = get_name(response[TRIG]) if TRIG in response else msg_type
            st, trans = get_status(response)
            for status in st:
                rules = get_rsp_rules(HOME_NODE, dst)
                for rule_type in rules:
                    rule_content = rules[rule_type]
                    if rule_content:
                        category, major, minor = get_rule_index(HOME_NODE)
                        rule_index = RULE_INDEX_TEMPLATE.format(category=category, major=major, minor=minor)
                        template_name = rule_content[TEMPLATE]
                        msg = msg_type if FOLD not in response or rule_type != SND else response[FOLD]
                        trigger = rule_content[TRIG].format(trigger=trig)
                        condition = STATUS_COND_TEMPLATE.format(status=status) if status else 'True'
                        assertion = rule_content[ASSERT].format(condition=condition)
                        ost = get_ost(HOME_NODE, trans)
                        handler = rule_content[HNDLR].format(msg_type=msg, ost=ost) if HNDLR in rule_content else None
                        hold = rule_content[HLD].format(hold=hld if hld != None else trig) if HLD in rule_content else None
                        template = HN_RESPONSE_TRAVERSE_TEMPLATE if hold else HN_RESPONSE_TEMPLATE
                        rule_num = get_rule_num(src, dst, msg, status)
                        rule_name = get_rule_name(category, src, dst, msg_type, rule_num, status)
                        rule_template = template.format(
                            rule_name=rule_name,
                            rule_index=rule_index,
                            template_name=template_name,
                            trigger=trigger,
                            hold=hold,
                            assertion=assertion,
                            handler=handler
                        )
                        rule = textwrap.indent(rule_template, ' ' * SUB_SECTION_INDENT)
                        output += rule
    return output

def convert_sn_responses(responses):
    output = ''
    for msg in responses:
        msg_type = get_msg_type(msg)
        response = msg[msg_type]
        src = get_name(response[SRC])
        if is_sn(src):
            dst = get_name(response[DST])
            hld = response.get(HLD)
            trig = get_name(response[TRIG]) if TRIG in response else msg_type
            rules = get_rsp_rules(SLAVE_NODE, dst)
            for rule_type in rules:
                rule_content = rules[rule_type]
                if rule_content:
                    template_name = rule_content[TEMPLATE]
                    msg = msg_type if rule_type != SND else trig
                    trigger = rule_content[TRIG].format(trigger=msg)
                    st, trans = get_status(response) if rule_type == SCH else ([], None)
                    for status in st:
                        category, major, minor = get_rule_index(SLAVE_NODE)
                        rule_index = RULE_INDEX_TEMPLATE.format(category=category, major=major, minor=minor)
                        condition = STATUS_COND_TEMPLATE.format(status=status) if status else 'True'
                        assertion = rule_content[ASSERT].format(condition=condition)
                        ost = get_ost(SLAVE_NODE, trans)
                        handler = rule_content[HNDLR].format(msg_type=msg_type, ost=ost) if HNDLR in rule_content else None
                        hold = rule_content[HLD].format(hold=hld if hld != None else trig) if HLD in rule_content else None
                        template = SN_RESPONSE_TRAVERSE_TEMPLATE if hold else SN_RESPONSE_TEMPLATE
                        rule_num = get_rule_num(src, dst, msg_type, status)
                        rule_name = get_rule_name(category, src, dst, msg_type, rule_num)
                        rule_template = template.format(
                            rule_name=rule_name,
                            rule_index=rule_index,
                            template_name=template_name,
                            trigger=trigger,
                            hold=hold,
                            assertion=assertion,
                            handler=handler
                        )
                        rule = textwrap.indent(rule_template, ' ' * SUB_SECTION_INDENT)
                        output += rule
    return output

def convert(json_path):
    with open(json_path, 'r') as file:
        json_data = json.load(file)
    
    section_name = os.path.basename(json_path).split('.')[0]
    dsl_output = textwrap.indent(f'\nSection {section_name}.\n', ' ' * DEFAULT_INDENT)
    
    RULE_IDX[REQ_NODE][CAT]   = json_data.get(CAT, 0)
    RULE_IDX[HOME_NODE][CAT]  = json_data.get(CAT, 0)
    RULE_IDX[SLAVE_NODE][CAT] = json_data.get(CAT, 0)

    req = json_data.get(CLS_REQ, [])
    snp = json_data.get(CLS_SNP, [])
    rsp = json_data.get(CLS_RSP, [])
    dat = json_data.get(CLS_DAT, [])

    dsl_output += convert_rn_requests(req)
    dsl_output += convert_rn_responses(rsp)
    dsl_output += convert_hn_requests(req + snp)
    dsl_output += convert_hn_responses(rsp + dat)
    dsl_output += convert_sn_responses(rsp + dat)
    dsl_output += textwrap.indent(f'\nEnd {section_name}.\n', ' ' * DEFAULT_INDENT)
    return dsl_output

def gen_spec(input_path, output_path, spec_name):
    msg_types = {}
    for i in os.listdir(input_path):
        json_path = os.path.join(input_path, i)
        if i.endswith('.json'):
            with open(json_path, 'r') as file:
                json_data = json.load(file)
                for field in MSG_CLS:
                    items = json_data.get(field, [])
                    msg_types[field] = []
                    for item in items:
                        name = get_msg_type(item)
                        match = False
                        for j in msg_types:
                            if name in msg_types[j]:
                                match = True
                                break
                        if not match:
                            msg_types[field].append(name)

    dsl_output = '\n'.join(SPEC_HEADER_TEMPLATE)
    dsl_output += f'\n{TYPE_TEMPLATE}'
    dsl_output += f'{HELPER_FUNC_TEMPLATE}'
    for i in range(len(STATES)):
        dsl_output += STATE_TEMPLATE.format(state_name=STATES[i], state_value=i)
    dsl_output += '\n'

    for i in msg_types:
        for j in msg_types[i]:
            dsl_output += MSG_TEMPLATE.format(msg=j, cls=MSG_CLS.index(i), num=msg_types[i].index(j))
    dsl_output += '\n'

    state_cases = []
    for i in STATES:
        if i != STATE_INVALID:
            if i in [STATE_DIRTY, STATE_EXCL]:
                state_cases.append(f'| {i}: if idx_dec idx dir.(d_excl) then {i} else {STATE_INVALID}')
            else:
                state_cases.append(f'| {i}: if in_dec idx_dec idx dir.(d_sharers) then {i} else {STATE_INVALID}')
    dsl_output += GET_DIR_TEMPLATE.format(state_cases="\n  ".join(state_cases))

    args = []
    dsl_output += SET_DIR_TEMPLATE
    for st in STATES:
        if st == STATE_INVALID:
            args = [None, None]
        elif st == STATE_SHARED:
            args = [None, ('inds', f'list {IDX_TYPE}')]
        else:
            args = [('idx', f'{IDX_TYPE}'), None]
        real_args = filter(lambda i: i != None, args)
        arg_list = map(lambda i: f'({i[0]}: {i[1]})', real_args)
        real_arg_list = map(lambda i: f'(Some {i[0]})' if i else 'None', args)
        dsl_output += SET_STATE_TEMPLATE.format(
            state_name=st,
            arg_list=' '.join(arg_list),
            real_arg_list=" ".join(real_arg_list)
        )
    path = os.path.join(output_path, spec_name)
    with open(path, 'w') as output_file:
        output_file.write(dsl_output)

def gen_target(components, output_path, target_name):
    target = target_name.split('.')[0]
    dsl_output = f'{IMPORT_TEMPLATE.format(name=SPEC.format(target=target))}\n'
    dsl_output += '\n'.join(HEADER_TEMPLATE)
    dsl_output += f'\n\nSection System.\n'
    dsl_output += textwrap.indent(f'{SYSTEM_TEMPLATE}', ' ' * DEFAULT_INDENT)
    dsl_output += textwrap.indent(f'{INSTANCE_TEMPLATE}\n', ' ' * DEFAULT_INDENT)
    for i in components:
        dsl_output += i
    dsl_output += f'\nEnd System.\n'
    path = os.path.join(output_path, target_name)
    with open(path, 'w') as output_file:
        output_file.write(dsl_output)
