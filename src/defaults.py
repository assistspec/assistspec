STATE_EXCL    = 'UC'
STATE_SHARED  = 'SC'
STATE_INVALID = 'I'
STATE_DIRTY   = 'D'
STATE_CLEAN   = 'C'

STATES = [STATE_EXCL, STATE_SHARED, STATE_INVALID, STATE_DIRTY, STATE_CLEAN]

REQ_NODE   = 'RN'
FWD_NODE   = 'FN'
HOME_NODE  = 'HN'
SLAVE_NODE = 'SN'

PREFIX = {REQ_NODE: 'RN',HOME_NODE: 'HN', SLAVE_NODE: 'SN'}

CLS_DAT = 'Data'
CLS_SNP = 'Snoop'
CLS_REQ = 'Request'
CLS_RSP = 'Response'

MSG_CLS = [CLS_REQ, CLS_SNP, CLS_DAT, CLS_RSP]

DIR_TYPE   = 'DirT'
IDX_TYPE   = 'IdxT'
STATE_TYPE = 'StateT'

PERMISSIONS = ['Read', 'Write']

HLD      = 'Hold'
FOLD     = 'Fold'
HOME     = 'Home'
MAJOR    = 'Major'
MINOR    = 'Minor'
OTHER    = 'Other'
SND      = 'Sender'
SRC      = 'Source'
STAT     = 'Status'
UPDATE   = 'Update'
ASSERT   = 'Assert'
TRIG     = 'Trigger'
HNDLR    = 'Handler'
RCV      = 'Receiver'
TEMPLATE = 'Template'
CAT      = 'Category'
REQ      = 'Requester'
SCH      = 'Scheduler'
PERM     = 'Permission'
TRANS    = 'Transition'
DST      = 'Destination'

SPEC = """{target}Spec"""

DEFAULT_INDENT = 2
SUB_SECTION_INDENT = DEFAULT_INDENT * 2
