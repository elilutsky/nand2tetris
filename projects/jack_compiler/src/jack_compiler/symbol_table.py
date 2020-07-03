import collections
from enum import Enum
from .jack_to_vm_maps import SegmentType

SymbolDescription = collections.namedtuple('SymbolDescription',
                                           'name type kind index')


class SymbolKind(Enum):
    FIELD = 'field kind'
    STATIC = 'static kind'
    ARGUMENT = 'argument kind'
    LOCAL = 'local kind'


SYMBOL_KIND_TO_SEGMENT_MAP = {
    SymbolKind.FIELD: SegmentType.THIS,
    SymbolKind.STATIC: SegmentType.STATIC,
    SymbolKind.ARGUMENT: SegmentType.ARGUMENT,
    SymbolKind.LOCAL: SegmentType.LOCAL
}


class SymbolTable:
    def __init__(self):

        # each dict maps a symbol name to its SymbolDescription
        self._class_scope_table = dict()
        self._function_scope_table = dict()

    def _get_next_symbol_index_by_kind(self, kind):
        table_to_search = self._symbol_kind_to_table(kind)

        indices = [symbol_info.index for symbol_info in table_to_search if symbol_info.kind == kind]
        current_max = max(indices) if len(indices) > 0 else 0

        return current_max + 1

    def _symbol_kind_to_table(self, kind):
        assert isinstance(type, SymbolKind)
        if kind in [SymbolTable.STATIC, SymbolTable.FIELD]:
            return self._class_scope_table
        return self._function_scope_table

    def _append_symbol(self, name, symbol_type, kind):
        scope_table = self._symbol_kind_to_table(kind)
        assert name not in scope_table, f'f{name} variable is already defined'
        scope_table[name] = SymbolDescription(name=name,
                                              type=symbol_type,
                                              kind=kind,
                                              index=self._get_next_symbol_index_by_kind(kind))

    def reset_function_scope(self):
        self._function_scope_table = dict()

    def append_static(self, name, symbol_type):
        self._append_symbol(name, symbol_type, SymbolKind.STATIC)

    def append_field(self, name, symbol_type):
        self._append_symbol(name, symbol_type, SymbolKind.FIELD)

    def append_argument(self, name, symbol_type):
        self._append_symbol(name, symbol_type, SymbolKind.ARGUMENT)

    def append_local(self, name, symbol_type):
        self._append_symbol(name, symbol_type, SymbolKind.LOCAL)

    def resolve_symbol(self, name):
        """
        Resolves the symbol name according to the Jack language resolution rules
        First, the local function scope is searched.
        If the variable is not found in function scope, the class scope is searched.
        :param name: the variable to search for for
        :return: a tuple of (SegmentType, offset, type) for the VM translation. Otherwise, if not found,
                 None is returned.
                 For a valid Jack program, if None is returned, the caller may assume the symbol is
                 either a subroutine name or a class name
        """

        symbol_description = None

        if name in self._function_scope_table:
            symbol_description = self._function_scope_table[name]

        elif name in self._class_scope_table:
            symbol_description = self._class_scope_table[name]

        if symbol_description is None:
            return None

        return SYMBOL_KIND_TO_SEGMENT_MAP[symbol_description.kind], symbol_description.index, symbol_description.type






