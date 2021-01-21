from html.parser import HTMLParser


stack = []


class Element:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
        self.content = ""

    def append(self, elem):
        self.children.append(elem)

    def add_text(self, text):
        self.content += text

    def control_content(self):
        if isinstance(self.content, str):
            skips = ["not determined", "Negligible", "<", ","]
            remove_followings = ["[", "-", "–"]
            for skip in skips:
                if skip in self.content:
                    self.content = self.content.replace(skip, "")
            if "." in self.content:
                self.content = self.content[:self.content.find(".") + 2]
            for remove_following in remove_followings:
                if remove_following in self.content:
                    self.content = self.content[:self.content.find(remove_following)]
            if self.content == "":
                self.content = "0"
        try:
            self.content = float(self.content)
        except ValueError:
            pass


class TableParser(HTMLParser):
    table = Element("table")
    cells = ["td", "th"]

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        if tag in self.cells + ['table', 'tbody', 'tr']:
            stack.append(Element(tag))

    def handle_endtag(self, tag):
        # print("Child: ", "'"+child.tag+"'", child.content, child.children)
        # print(stack)
        # print(tag, tag in self.cells)
        if tag in self.cells:
            child = stack.pop()
            child.control_content()
            parent = stack.pop()
            # print("Parent: ", parent.tag)
            parent.append(child)
            stack.append(parent)
        if tag == "tr":
            child = stack.pop()
            child.control_content()
            self.table.append(child)

    def handle_data(self, data):
        skip_substr = ['♠', '-', '(', ')']
        raw = data.strip()
        for substr in skip_substr:
            if substr in raw:
                return
        elem = stack.pop()
        elem.add_text(raw)
        stack.append(elem)


def get_table(file):
    start = "<table"
    end = "</table>"
    tag_start = file.find(start)
    tag_end = file.find(end) + len(end)

    return file[tag_start:tag_end]


def parse_table(table):
    parser = TableParser()
    parser.feed(table)
    return parser.table


def parse_table_to_states(table):
    header = [cell.content for cell in table.children[0].children[2:-1]]
    parsed_states = {}

    for row in table.children[2:]:
        state = {}
        for i, cell in enumerate(row.children[2:-1]):
            state[header[i]] = cell.content
        parsed_states[row.children[1].content] = state

    return parsed_states


def find_most_similar(state_dict):
    output = None
    similarity = None

    for name_1, state_1 in state_dict.items():
        for name_2, state_2 in state_dict.items():
            if name_1 != name_2:
                sim = 1
                for prop in state_1:
                    values = sorted([state_1[prop], state_2[prop]])
                    if values[0] > 0:
                        sim *= values[1] / values[0]
                    else:
                        sim *= 1000
                if not similarity or sim < similarity:
                    similarity = sim
                    output = (name_1, name_2)
    return output


wiki_file = open('List.html', encoding='utf-8').read()
html_table = get_table(wiki_file)
parsed_table = parse_table(html_table)
states = parse_table_to_states(parsed_table)
most_similar_tuple = find_most_similar(states)
print(most_similar_tuple)
