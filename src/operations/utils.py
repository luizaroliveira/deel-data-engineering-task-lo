from sqlalchemy import create_engine, text  # Import text for raw SQL if needed
import re


def has_sql_code(argument_text: str):
    """
    Checks if a given string likely contains SQL code.

    This function uses a combination of regular expressions and keyword checks
    to identify potential SQL code within a string.  It's not foolproof, but
    it should catch most common cases.  False positives are possible.

    Args:
        argument_text: The string to check.

    Returns:
        True if the string likely contains SQL code, False otherwise.
    """

    if not isinstance(argument_text, str):
        raise TypeError("Input must be a string.")

    # Convert to lowercase for case-insensitive matching
    argument_text = argument_text.lower()

    # Regular expression patterns for common SQL keywords and syntax
    patterns = [
        r"\b(select|insert|update|delete|create|drop|alter|grant|revoke|union|join|from|where|group by|order by|having|limit|offset|distinct|as|inner|outer|left|right|full|on|and|or|not|in|between|like|exists|null|is null)\b",
        # Keywords
        r"[;]",  # Semicolon statement terminator
        r"[\(\)]",  # Parentheses (often used in functions/subqueries)
        r"[=><!]+",  # Comparison operators
        r"['\"]",  # Quotes (for string literals)
        r"--",  # SQL comment style
        r"/\*",  # Start of multi-line comment /* */
        r"\*/"  # End of multi-line comment /* */
    ]

    for pattern in patterns:
        if re.search(pattern, argument_text):
            return True