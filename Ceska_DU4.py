women = {}
clubs = {}


class Woman:
    def __init__(self, name):
        self._name = name
        self._mother = None
        self._daughters = []

    def add_daughter(self, daughter):
        self._daughters.append(daughter)
        get_woman_by_name(daughter).add_mother(self._name)

    def add_mother(self, mother):
        self._mother = mother

    def get_name(self):
        return self._name

    def get_mother(self):
        return self._mother

    def get_daughters(self):
        return self._daughters


class Club:
    def __init__(self, name):
        self._name = name
        self._members = []

    def add_members(self, members):
        self._members.extend(members)

    def get_members(self):
        return self._members


def get_woman_by_name(name):
    global women
    return women[name]


def read_data(filename):
    file = open(filename, 'r')
    lines = file.read().splitlines()
    data = {}

    for i in range(3):
        temp = []
        elem = lines.pop()
        while not elem.startswith('#'):
            temp.append(elem)
            elem = lines.pop()
        data[elem] = temp

    return data


def process(data):
    for name in data['#Women']:
        global women
        women[name] = Woman(name)

    for dependency in data['#Children']:
        (mother_name, daughter_name) = dependency.split('->')
        get_woman_by_name(mother_name).add_daughter(daughter_name)

    for club in data['#Clubs']:
        global clubs
        [name, members_names] = club.split(':')
        club = Club(name)
        if len(members_names) > 0:
            club.add_members(members_names.split(','))
        clubs[name] = club


def most_clubs():
    global clubs
    global women
    members = []

    for club in clubs:
        members.extend(clubs[club].get_members())

    print("Woman in most clubs:", max(set(members), key=members.count))


def club_info():
    global clubs
    for club in sorted(clubs, key=lambda c: len(clubs[c].get_members()), reverse=True):
        print(club, end=": ")
        print(*sorted(clubs[club].get_members()), sep=", ")


def mothers_family_tree(name):
    woman = get_woman_by_name(name)
    mother = woman.get_mother()
    if mother:
        generation = mothers_family_tree(mother) + 1
    else:
        generation = 0
    print(generation * "    " + woman.get_name())
    return generation


def children_family_tree(name, generation=0):
    woman = get_woman_by_name(name)
    daughters = woman.get_daughters()
    print(generation * "    " + woman.get_name())
    for daughter in daughters:
        children_family_tree(daughter, generation + 1)


file_data = read_data('example_data.txt')
process(file_data)

most_clubs()
print()
club_info()
print()
mothers_family_tree("Betty")
print()
children_family_tree("Mary")
