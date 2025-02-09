class SpreadsheetFunction(object):
    """Metadata about a function for a spreadsheet application"""

    def __init__(self, name: str, description: str = None, family: str = None,
                 required_args: list[str] = None,
                 optional_args: list[str] = None,
                 has_ellipsis: bool = False):
        super(SpreadsheetFunction, self).__init__()
        self.name = name
        self.description = description
        self.family = family
        self.required_args = required_args
        self.optional_args = optional_args
        self.has_ellipsis = has_ellipsis

    def to_arg_string(self) -> str:
        args = self.required_args
        args += [f'[{a}]' for a in self.optional_args]
        if self.has_ellipsis:
            args += ['...']
        return ', '.join(args)

    def to_completion_arg_string(self) -> str:
        # TODO: Replace this with the fancy one
        return self.to_arg_string()

    def to_sublime_word_completion(self) -> dict[str,str]:
        return {
            "trigger": self.name,
            "contents": self.name,
            "annotation": self.family,
            "details": self.description,
            "kind": "function",
        }

    def to_sublime_snippet_completion(self) -> dict[str,str]:
        return {
            "trigger": self.name.lower(),
            "contents": self.to_completion_arg_string(),
            "annotation": self.family,
            "details": self.description,
            "kind": "snippet",
        }
