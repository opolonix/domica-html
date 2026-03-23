from tags import form, input
from typing import Optional

class RemoteCall:
    ...

class Form(form):
    def __init__(
        self,
        action: Optional[RemoteCall] = None,

        anchor=True
    ):
        super().__init__(anchor=anchor)

    async def render(self):
        ...