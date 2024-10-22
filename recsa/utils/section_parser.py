__all__ = ['parse_sections']


def parse_sections(text: str) -> dict[str, list[str]]:
	sections: dict[str, list[str]] = {}
	current_section = None
	for line in text.splitlines():
		# Ignore empty lines
		if line.strip() == "":
			continue
		# Ignore comments (lines starting with '#')
		line = line.split('#')[0].strip()
		if not line:
			continue
		# Check if the line is a section header
		if line.startswith('[') and line.endswith(']'):
			current_section = line[1:-1]
			sections[current_section] = []
		elif current_section:
			sections[current_section].append(line)
	return sections
