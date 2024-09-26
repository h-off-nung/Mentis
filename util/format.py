import re

def format_for_telegram(text: str) -> str:
    # Escape necessary characters for Markdown V2
    general_escape_chars = r'\[\]()~_`>#\+\-=|{}.!'

    # First, escape all the general Markdown V2 characters
    formatted_text = re.sub(f'([{re.escape(general_escape_chars)}])', r'\\\1', text)

    # Ensure proper escaping of asterisks that are not part of a bold entity
    # This also converts bold '**text**' into '*text*' while ensuring correct Markdown V2 syntax
    formatted_text = re.sub(r'(\*)', r'\\*', formatted_text)  # Escape any existing asterisks
    formatted_text = re.sub(r'\\\*\\\*(.+?)\\\*\\\*', r'*\1*', formatted_text)  # Handle bold properly

    return formatted_text
