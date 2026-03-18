import contextvars
from typing import Callable, List, Union

increment_context: contextvars.ContextVar["IncrementContext"] = contextvars.ContextVar("dom_item_context_var_ind")

_UNSET = object()

def _str(value, refresh: Callable = None):
    ctx = increment_context.get(None)
    if ctx is not None and ctx.is_final:
        return value

    class r_str(str):
        def re_render(_):
            if not refresh: return str(_)
            return str(refresh())

    return r_str(value)

class IncrementContext:
    def __init__(self):
        self._indent: List[int] = []
        self._char: List[str] = []
        self._final: List[bool] = []
        self._is_set = False

    def set(
        self,
        indent: Union[int, object] = _UNSET,
        char: Union[str, object] = _UNSET,
    ) -> None:
        self._is_set = True
        if indent is not _UNSET:
            self._indent.append(indent)
        elif self._indent:
            self._indent.append(self._indent[-1])

        if char is not _UNSET:
            self._char.append(char)
        elif self._char:
            self._char.append(self._char[-1])

    def inc(self) -> None:
        if not self._is_set:
            self.set(indent=self.indent + 1)
    
        self._is_set = False

    @property
    def indent(self) -> int:
        return self._indent[-1] if self._indent else 0
    
    @property
    def char(self) -> str:
        return self._char[-1] if self._char else "    "

    def pop(self) -> bool:
        if self._indent:
            self._indent.pop()
        if self._char:
            self._char.pop()
        return True

    def enter_final(self) -> None:
        self._final.append(True)

    def exit_final(self) -> bool:
        if self._final:
            self._final.pop()
        return True

    @property
    def is_final(self) -> bool:
        return bool(self._final)


class _increment_final:
    def __init__(self, owner: "_increment"):
        self.owner = owner

    def __enter__(self) -> "_increment_final":
        self.owner.context.enter_final()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.owner.context.exit_final()
        return False


class _increment:
    @property
    def indent(self) -> int:
        return self.context.indent

    @property
    def char(self) -> str:
        return _str(self.context.char, refresh=lambda: self.char)

    @property
    def space(self) -> str:
        return _str((self.char * self.indent) if self.char else "", refresh=lambda: self.space)

    @property
    def context(self) -> IncrementContext:
        ctx = increment_context.get(None)
        if ctx is None:
            ctx = IncrementContext()
            increment_context.set(ctx)
        return ctx

    @property
    def enter_space(self) -> str:
        return _str(("\n" + (self.char * self.indent)) if self.char else "", refresh=lambda: self.enter_space)

    @property
    def start_space(self) -> str:
        return _str((("\n" + (self.char * self.indent)) if self.char and self.indent else ""), refresh=lambda: self.start_space)

    @property
    def final(self) -> _increment_final:
        return _increment_final(self)

    def __call__(
        self,
        indent: Union[int, object] = _UNSET,
        char: Union[str, object] = _UNSET
    ) -> "_increment":
        self.context.set(
            indent=indent,
            char=char
        )
        return self

    def __enter__(self) -> "_increment":
        self.context.inc()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.context.pop()
        return False

inc = _increment()
