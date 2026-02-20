import contextvars

increment_context: contextvars.ContextVar["IncrementContext"] = contextvars.ContextVar("dom_item_context_var_ind")

class IncrementContext:
    def __init__(self):
        self._indent: list[int] = []
        self._char: list[str] = []
        self._to_set: dict[str] = {}
        self._is_setted = False

    def set(
        self,
        indent: int = ...,
        char: str = ...,
    ):
        self._is_setted = True
        if indent is not ...:
            self._indent.append(indent)
        elif self._indent:
            self._indent.append(self._indent[-1])

        if char is not ...:
            self._char.append(char)
        elif self._char:
            self._char.append(self._char[-1])

    def inc(self):
        if not self._is_setted:
            self.set(indent=self.indent + 1)
    
        self._is_setted = False

    @property
    def indent(self):
        return self._indent[-1] if self._indent else 0
    
    @property
    def char(self):
        return self._char[-1] if self._char else ""
    
    def pop(self):
        if self._indent:
            self._indent.pop(-1)
        if self._char:
            self._char.pop(-1)
        return True


class _increment:
    @property
    def indent(self) -> int:
        return self.context.indent

    @property
    def char(self) -> str:
        return self.context.char

    @property
    def space(self) -> str:
        return (self.char * self.indent) if self.char else ""

    @property
    def context(self):
        ctx = increment_context.get(None)
        if ctx is None:
            ctx = IncrementContext()
            increment_context.set(ctx)
        return ctx

    @property
    def enter_space(self) -> str:
        return ("\n" + self.space) if self.char else ""

    def __call__(
        self,
        indent: int = ...,
        char: str = ...
    ):
        self.context.set(
            indent=indent,
            char=char
        )
        return self

    def __enter__(self):
        self.context.inc()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.pop()
        return False

inc = _increment()