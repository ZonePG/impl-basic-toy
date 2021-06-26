from error.error import Error
from error.string_with_arrows import string_with_arrows


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = (
                f" File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n"
                + result
            )
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call):\n" + result
