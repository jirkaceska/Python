#!/usr/bin/python3
import copy
import traceback
from collections import deque

# Specialni domaci ukol IB002 2018
# ** Ukol je lehci nez zadani implementacnich testu na zaverecne zkousce. **
#
# Zadani:
# V tomto domacim ukolu budeme pracovat s datovou strukturou Trie.
# Podrobnosti o teto datove strukture jsou popsany v PDF verzi zadani,
# kterou mate k dispozici ve studijnich materialech.
#
# Poznamka ke slozitosti:
# Nezapominejte, ze slice seznamu `array[i:j]` vytvari v Pythonu novy seznam a
# ma tedy slozitost linearni k delce nove vytvoreneho seznamu. Pouzivani slices
# tedy muze pokazit slozitost Vaseho algoritmu.


class Node:
    """Trida reprezentujici uzel trie.

    Atributy:
        succs       pole nasledniku uzlu (vzdy velikosti presne 26)
        succ_count  pocet nasledniku (tj. pocet prvku pole, ktere nejsou None)
        accepting   pravdivostni hodnota oznacujici, zda je uzel akceptujici
    """

    def __init__(self):
        self.succs = [None] * 26  # pole nasledniku
        self.succ_count = 0       # pocet nasledniku
        self.accepting = False    # je toto akceptujici uzel?
        # je zakazano pridavat uzlum jakekoli dalsi atributy


class Trie:
    """Trida reprezentujici trie. Ma jediny atribut root - koren trie."""

    def __init__(self):
        self.root = None


# Nasledujici pomocnou funkci muzete vyuzit pro prevod malych pismen anglicke
# abecedy na cislo mezi 0 a 25 vcetne.

def get_id(x):
    """Pro zadany znak v rozsahu 'a' - 'z' vrati hodnotu 0 - 25."""
    return ord(x) - ord('a')


# Ukol 1. Count (1 bod)
# Implementujte funkci count(trie), ktera vrati pocet slov, ktere zadana trie
# obsahuje. Funkce nesmi menit zadanou trie.


def count(trie):
    """
    vstup: 'trie' korektni trie
    vystup: pocet slov, ktere 'trie' obsahuje
    casova slozitost: O(n), kde n je pocet uzlu v 'trie'
    """
    def count_accepts(node):
        if node is None:
            return 0
        res = 0
        if node.accepting:
            res += 1
        for succ in node.succs:
            res += count_accepts(succ)
        return res

    return count_accepts(trie.root)


# Ukol 2. Insert (1 bod)
# Implementujte funkci insert(trie, word), ktera do zadane trie vlozi slovo
# 'word'. Pokud trie uz slovo obsahovala, nestane se nic.
# Funkce modifikuje primo zadanou trie, tj. nevytvari novou ani nic nevraci.

def insert(trie, word):
    """
    vstup: 'trie' korektni trie
           'word' retezec z malych pismen anglicke abecedy ('a' az 'z')
    vystup: nic, do 'trie' se vlozi slovo 'word'
            'trie' musi zustat korektni
    casova slozitost: O(d), kde d je delka slova 'word'
    """
    if trie.root is None:
        trie.root = Node()
    node = trie.root

    for letter in word:
        i = get_id(letter)
        if node.succs[i] is None:
            node.succs[i] = Node()
            node.succ_count += 1
        node = node.succs[i]

    node.accepting = True


# Ukol 3. Delete (1 bod)
# Implementujte funkci delete(trie, word), ktera ze zadane trie smaze slovo
# 'word'. Pokud trie toto slovo neobsahovala, nestane se nic.
# Funkce modifikuje primo zadanou trie, tj. nevytvari novou ani nic nevraci.
#
# Nezapomente, ze po odstraneni uzlu z trie je treba zkontrolovat, zda v ni
# nevznikl neakceptujici list. Doporucujeme si vytvorit rekurzivni funkci,
# ktera bude prochazet trie smerem dolu a pri navratu si bude vracet informaci
# (napr. pravdivostni hodnotu) o tom, jestli ma dojit k odstraneni uzlu.
def del_in_node(node, word, w_i):
    word_len = len(word)
    # Trie is deep enough to delete word
    if node is None:
        return word_len < w_i
    # End of word was found
    if word_len == w_i:
        node.accepting = False
        return not node.succ_count

    i = get_id(word[w_i])
    was_deleted = del_in_node(node.succs[i], word, w_i + 1)

    if was_deleted:
        node.succ_count -= 1
        node.succs[i] = None
        # Delete this node from parent when this condition is met
        return node.succ_count == 0 and not node.accepting

    return False


def delete(trie, word):
    """
    vstup: 'trie' korektni trie
           'word' retezec z malych pismen anglicke abecedy ('a' az 'z')
    vystup: nic, z 'trie' se vymaze slovo 'word'
            'trie' musi zustat korektni
    casova slozitost: O(d), kde d je delka slova 'word'
    """
    if del_in_node(trie.root, word, 0):
        trie.root = None


"""
Soubory .dot z testu vykreslite napr. na http://www.webgraphviz.com/.
"""

########################################################################
#               Nasleduje kod testu, NEMODIFIKUJTE JEJ                 #
########################################################################


def make_trie(trie, filename):
    """
    Zde mate k dispozici funkci `make_trie`, ktera vam z `trie` na vstupu
    vygeneruje do souboru `filename` reprezentaci trie pro graphviz.
    Graphviz je nastroj, ktery vam umozni vizualizaci datovych struktur,
    coz se hodi predevsim pro ladeni.
    Pokud je trie nekorektni, problemove uzly jsou vyznaceny cervenou barvou
    a je v nich napsan duvod nekorektnosti.
    Pro zobrazeni graphvizu muzete vyuzit: http://www.webgraphviz.com/
    """

    def dot_node(node):
        label = ""
        bad_node = ',shape="ellipse",color="red"'
        style = ""

        if len(node.succs) != 26:
            style = bad_node
            label = "len(node.succs) != 26"
        elif node.succ_count != ib002_count_not_none(node.succs):
            style = bad_node
            label = "succ_count == " + str(node.succ_count)
        elif not node.accepting and node.succ_count == 0:
            style = bad_node
            label = "non-accepting leaf"
        elif node.accepting:
            style = ',shape="doublecircle"'

        f.write('{} [label="{}"{}]\n'.format(id(node), label, style))

        for i, s in enumerate(node.succs):
            if s is not None:
                dot_node(s)
                char = chr(i + ord('a'))
                f.write('{} -> {} [label=" {}"]\n'.format(id(node),
                                                          id(s), char))

    with open(filename, 'w') as f:
        f.write("digraph {\n")
        f.write('node [shape="circle",ordering="out"]\n')
        if trie.root is not None:
            dot_node(trie.root)
        f.write("}\n")


def ib002_is_correct_trie(trie):
    def is_correct_node(node):
        if node is None:
            return True

        if len(node.succs) != 26 or\
           node.succ_count != ib002_count_not_none(node.succs) or\
           (not node.accepting and node.succ_count == 0):
            return False

        return all(map(is_correct_node, node.succs))

    return is_correct_node(trie.root)


def ib002_count_not_none(l):
    return len(l) - l.count(None)


def ib002_equal_trie(a, b):
    def equal_node(a, b):
        if a is None or b is None:
            return a is None and b is None

        return len(a.succs) == len(b.succs) and a.succ_count == b.succ_count \
            and a.accepting == b.accepting \
            and all(equal_node(x, y) for x, y in zip(a.succs, b.succs))

    return equal_node(a.root, b.root)


def ib002_make_trie_and_report(trie, filename, msg):
    note = " (prazdna trie)" if trie.root is None else ""
    make_trie(trie, filename)
    print("{} je v souboru: {}{}".format(msg, filename, note))


def ib002_one_test_readonly(function, name, tag, result, trie, word=None):
    clone = copy.deepcopy(trie)

    input_file = "Er_{}{}_input.dot".format(name, tag)
    changed_file = "Er_{}{}_changed.dot".format(name, tag)

    if word is None:
        answer = function(clone)
    else:
        answer = function(clone, word)
        name += " se slovem '{}'".format(word)

    if answer != result:
        print("Spatna odpoved: ma byt {}, ale funkce {} vrati {}.".format(
            result, name, answer))
        ib002_make_trie_and_report(trie, input_file, "Vstupni trie")
        return False

    if not ib002_equal_trie(trie, clone):
        print("Funkce {} zmenila vstupni trie!".format(name))
        ib002_make_trie_and_report(trie, input_file, "Puvodni trie")
        ib002_make_trie_and_report(clone, changed_file, "Zmenena trie")
        return False

    return True


def ib002_one_test_modify(function, name, tag, result, trie, word):
    clone = copy.deepcopy(trie)
    function(clone, word)

    input_file = "Er_{}{}_input.dot".format(name, tag)
    output_file = "Er_{}{}_output_student.dot".format(name, tag)
    correct_file = "Er_{}{}_output_correct.dot".format(name, tag)

    if not ib002_is_correct_trie(clone):
        print("Vysledkem funkce {} se slovem '{}' neni korektni trie.".format(
            name, word))
        ib002_make_trie_and_report(trie, input_file, "Puvodni trie")
        ib002_make_trie_and_report(clone, output_file,
                                   "Vase vysledna nekorektni trie")
        ib002_make_trie_and_report(result, correct_file, "Spravny vysledek")
        return False

    if not ib002_equal_trie(clone, result):
        print("Spatny vysledek funkce {} se slovem '{}'.".format(name, word))
        ib002_make_trie_and_report(trie, input_file, "Puvodni trie")
        ib002_make_trie_and_report(clone, output_file, "Vase vysledna trie")
        ib002_make_trie_and_report(result, correct_file, "Spravny vysledek")
        return False

    return True


def ib002_deserialize_trie(text):
    trie = Trie()
    text = "".join(filter(lambda x: x.islower() or x in "+|", text))
    if text == "":
        return trie

    trie.root = Node()
    q = deque([trie.root])

    for char in text:
        node = q[0]
        if char == '+':
            node.accepting = True
        elif char == '|':
            if node.succ_count == 0:
                node.accepting = True
            q.popleft()
        else:
            new_node = Node()
            node.succs[ord(char) - ord('a')] = new_node
            node.succ_count += 1
            q.append(new_node)

    for node in q:
        node.accepting = True

    return trie


test_cases = \
    [('ct|a|eo|rt|an|+o|',
      [('car', 'ct|a|eo|t|an|+o|'), ('cat', 'ct|a|eo|r|an|+o|'),
       ('tea', 'ct|a|eo|rt|n|+o|'), ('ten', 'ct|a|eo|rt|a|+o|'),
       ('to', 'ct|a|eo|rt|an|o|'), ('too', 'ct|a|eo|rt|an|')],
      [('', '+ct|a|eo|rt|an|+o|'), ('c', 'ct|+a|eo|rt|an|+o|'),
       ('ca', 'ct|a|eo|+rt|an|+o|'), ('t', 'ct|a|+eo|rt|an|+o|'),
       ('te', 'ct|a|eo|rt|+an|+o|'), ('card', 'ct|a|eo|rt|an|+o|+d|'),
       ('cargo', 'ct|a|eo|rt|an|+o|+g|||||o|'),
       ('carbon', 'ct|a|eo|rt|an|+o|+b|||||o|n|'),
       ('cats', 'ct|a|eo|rt|an|+o||+s|'),
       ('catch', 'ct|a|eo|rt|an|+o||+c||||h|'),
       ('catnip', 'ct|a|eo|rt|an|+o||+n||||i|p|'),
       ('teak', 'ct|a|eo|rt|an|+o|||+k|'),
       ('tears', 'ct|a|eo|rt|an|+o|||+r|||s|'),
       ('teacup', 'ct|a|eo|rt|an|+o|||+c|||u|p|'),
       ('tent', 'ct|a|eo|rt|an|+o||||+t|'),
       ('tense', 'ct|a|eo|rt|an|+o||||+s||e|'),
       ('tenure', 'ct|a|eo|rt|an|+o||||+u||r|e|'),
       ('toy', 'ct|a|eo|rt|an|+oy|'), ('toss', 'ct|a|eo|rt|an|+os||||||s|'),
       ('towel', 'ct|a|eo|rt|an|+ow||||||e|l|'),
       ('toon', 'ct|a|eo|rt|an|+o|||||+n|'),
       ('tooth', 'ct|a|eo|rt|an|+o|||||+t|h|'),
       ('toodle', 'ct|a|eo|rt|an|+o|||||+d|l|e|'),
       ('a', 'act||a|eo|rt|an|+o|'), ('me', 'cmt|a|e|eo|rt||an|+o|'),
       ('zip', 'ctz|a|eo|i|rt|an|+o|p|'), ('cd', 'ct|ad|eo|rt||an|+o|'),
       ('cup', 'ct|au|eo|rt|p|an|+o|'), ('cyan', 'ct|ay|eo|rt|a|an|+o|||n|'),
       ('cab', 'ct|a|eo|brt|an|+o|'), ('cast', 'ct|a|eo|rst|an|+o||t|'),
       ('caulk', 'ct|a|eo|rtu|an|+o|||l||||k|'), ('tm', 'ct|a|emo|rt|an||+o|'),
       ('two', 'ct|a|eow|rt|an|+o|o|'),
       ('type', 'ct|a|eoy|rt|an|+o|p||||||e|'), ('tex', 'ct|a|eo|rt|anx|+o|'),
       ('tell', 'ct|a|eo|rt|aln|+o||||l|'),
       ('texas', 'ct|a|eo|rt|anx|+o|||||a||s|')]),
     ('a|b|r|a|k|a|+d|a|b|r|a|',
      [('abraka', 'a|b|r|a|k|a|d|a|b|r|a|'),
       ('abrakadabra', 'a|b|r|a|k|a|')],
      [('', '+a|b|r|a|k|a|+d|a|b|r|a|'), ('a', 'a|+b|r|a|k|a|+d|a|b|r|a|'),
       ('ab', 'a|b|+r|a|k|a|+d|a|b|r|a|'), ('abr', 'a|b|r|+a|k|a|+d|a|b|r|a|'),
       ('abra', 'a|b|r|a|+k|a|+d|a|b|r|a|'),
       ('abrak', 'a|b|r|a|k|+a|+d|a|b|r|a|'),
       ('abrakad', 'a|b|r|a|k|a|+d|+a|b|r|a|'),
       ('abrakada', 'a|b|r|a|k|a|+d|a|+b|r|a|'),
       ('abrakadab', 'a|b|r|a|k|a|+d|a|b|+r|a|'),
       ('abrakadabr', 'a|b|r|a|k|a|+d|a|b|r|+a|'),
       ('abrakaw', 'a|b|r|a|k|a|+dw|a||b|r|a|'),
       ('abrakadabrak', 'a|b|r|a|k|a|+d|a|b|r|a|+k|'),
       ('x', 'ax|b||r|a|k|a|+d|a|b|r|a|'), ('af', 'a|bf|r||a|k|a|+d|a|b|r|a|'),
       ('abv', 'a|b|rv|a||k|a|+d|a|b|r|a|'),
       ('abrb', 'a|b|r|ab|k||a|+d|a|b|r|a|'),
       ('abray', 'a|b|r|a|ky|a||+d|a|b|r|a|'),
       ('abraku', 'a|b|r|a|k|au|+d||a|b|r|a|'),
       ('abrakadh', 'a|b|r|a|k|a|+d|ah|b||r|a|'),
       ('abrakadaq', 'a|b|r|a|k|a|+d|a|bq|r||a|'),
       ('abrakadabf', 'a|b|r|a|k|a|+d|a|b|fr||a|'),
       ('abrakadabrl', 'a|b|r|a|k|a|+d|a|b|r|al|')]),
     ('+a|+v|+o|+k|+a|+d|+o|',
      [('', 'a|+v|+o|+k|+a|+d|+o|'), ('a', '+a|v|+o|+k|+a|+d|+o|'),
       ('av', '+a|+v|o|+k|+a|+d|+o|'), ('avo', '+a|+v|+o|k|+a|+d|+o|'),
       ('avok', '+a|+v|+o|+k|a|+d|+o|'), ('avoka', '+a|+v|+o|+k|+a|d|+o|'),
       ('avokad', '+a|+v|+o|+k|+a|+d|o|'), ('avokado', '+a|+v|+o|+k|+a|+d|')],
      [('f', '+af|+v||+o|+k|+a|+d|+o|'), ('as', '+a|+sv||+o|+k|+a|+d|+o|'),
       ('avs', '+a|+v|+os|+k||+a|+d|+o|'), ('avou', '+a|+v|+o|+ku|+a||+d|+o|'),
       ('avoks', '+a|+v|+o|+k|+as|+d||+o|'),
       ('avokak', '+a|+v|+o|+k|+a|+dk|+o|'),
       ('avokadt', '+a|+v|+o|+k|+a|+d|+ot|'),
       ('avokadoj', '+a|+v|+o|+k|+a|+d|+o|+j|')]),
     ('z|a|n|z|i|b|a|r|', [('zanzibar', '')],
      [('', '+z|a|n|z|i|b|a|r|'), ('z', 'z|+a|n|z|i|b|a|r|'),
       ('za', 'z|a|+n|z|i|b|a|r|'), ('zan', 'z|a|n|+z|i|b|a|r|'),
       ('zanz', 'z|a|n|z|+i|b|a|r|'), ('zanzi', 'z|a|n|z|i|+b|a|r|'),
       ('zanzib', 'z|a|n|z|i|b|+a|r|'), ('zanziba', 'z|a|n|z|i|b|a|+r|'),
       ('zanzibarman', 'z|a|n|z|i|b|a|r|+m|a|n|'),
       ('zagreb', 'z|a|gn|r|z|e|i|b|b||a|r|'),
       ('zaire', 'z|a|in|r|z|e|i||b|a|r|')]),
     ('', [],
      [('', '|'), ('f', 'f|'), ('zz', 'z|z|'), ('aqua', 'a|q|u|a|'),
       ('informatics', 'i|n|f|o|r|m|a|t|i|c|s|')]),
     ('|', [('', '')],
      [('a', '+a|'), ('z', '+z|'), ('l', '+l|'),
       ('rebarbora', '+r|e|b|a|r|b|o|r|a|')]),
     ('a|', [('a', '')],
      [('', '+a|'), ('auto', 'a|+u|t|o|'), ('blue', 'ab||l|u|e|'),
       ('zorg', 'az||o|r|g|')]),
     ('z|', [('z', '')],
      [('', '+z|'), ('auto', 'az|u||t|o|'), ('zorg', 'z|+o|r|g|'),
       ('moon', 'mz|o||o|n|')]),
     ('az|', [('a', 'z|'), ('z', 'a|')],
      [('', '+az|'), ('am', 'az|+m|'), ('zp', 'az||+p|'), ('j', 'ajz|')]),
     ('abcdefghijklmnopqrstuvwxyz|',
      [('a', 'bcdefghijklmnopqrstuvwxyz|'),
       ('b', 'acdefghijklmnopqrstuvwxyz|'),
       ('c', 'abdefghijklmnopqrstuvwxyz|'),
       ('d', 'abcefghijklmnopqrstuvwxyz|'),
       ('e', 'abcdfghijklmnopqrstuvwxyz|'),
       ('f', 'abcdeghijklmnopqrstuvwxyz|'),
       ('g', 'abcdefhijklmnopqrstuvwxyz|'),
       ('h', 'abcdefgijklmnopqrstuvwxyz|'),
       ('i', 'abcdefghjklmnopqrstuvwxyz|'),
       ('j', 'abcdefghiklmnopqrstuvwxyz|'),
       ('k', 'abcdefghijlmnopqrstuvwxyz|'),
       ('l', 'abcdefghijkmnopqrstuvwxyz|'),
       ('m', 'abcdefghijklnopqrstuvwxyz|'),
       ('n', 'abcdefghijklmopqrstuvwxyz|'),
       ('o', 'abcdefghijklmnpqrstuvwxyz|'),
       ('p', 'abcdefghijklmnoqrstuvwxyz|'),
       ('q', 'abcdefghijklmnoprstuvwxyz|'),
       ('r', 'abcdefghijklmnopqstuvwxyz|'),
       ('s', 'abcdefghijklmnopqrtuvwxyz|'),
       ('t', 'abcdefghijklmnopqrsuvwxyz|'),
       ('u', 'abcdefghijklmnopqrstvwxyz|'),
       ('v', 'abcdefghijklmnopqrstuwxyz|'),
       ('w', 'abcdefghijklmnopqrstuvxyz|'),
       ('x', 'abcdefghijklmnopqrstuvwyz|'),
       ('y', 'abcdefghijklmnopqrstuvwxz|'),
       ('z', 'abcdefghijklmnopqrstuvwxy|')],
      [('', '+abcdefghijklmnopqrstuvwxyz|'),
       ('ae', 'abcdefghijklmnopqrstuvwxyz|+e|'),
       ('bn', 'abcdefghijklmnopqrstuvwxyz||+n|'),
       ('ct', 'abcdefghijklmnopqrstuvwxyz|||+t|'),
       ('dn', 'abcdefghijklmnopqrstuvwxyz||||+n|'),
       ('eg', 'abcdefghijklmnopqrstuvwxyz|||||+g|'),
       ('fj', 'abcdefghijklmnopqrstuvwxyz||||||+j|'),
       ('gy', 'abcdefghijklmnopqrstuvwxyz|||||||+y|'),
       ('hs', 'abcdefghijklmnopqrstuvwxyz||||||||+s|'),
       ('it', 'abcdefghijklmnopqrstuvwxyz|||||||||+t|'),
       ('jw', 'abcdefghijklmnopqrstuvwxyz||||||||||+w|'),
       ('ki', 'abcdefghijklmnopqrstuvwxyz|||||||||||+i|'),
       ('lw', 'abcdefghijklmnopqrstuvwxyz||||||||||||+w|'),
       ('mu', 'abcdefghijklmnopqrstuvwxyz|||||||||||||+u|'),
       ('ny', 'abcdefghijklmnopqrstuvwxyz||||||||||||||+y|'),
       ('oe', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||+e|'),
       ('ph', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||+h|'),
       ('qs', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||||+s|'),
       ('rn', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||||+n|'),
       ('so', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||||||+o|'),
       ('ts', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||||||+s|'),
       ('uv', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||||||||+v|'),
       ('vd', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||||||||+d|'),
       ('wb', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||||||||||+b|'),
       ('xz', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||||||||||+z|'),
       ('yd', 'abcdefghijklmnopqrstuvwxyz|||||||||||||||||||||||||+d|'),
       ('zd', 'abcdefghijklmnopqrstuvwxyz||||||||||||||||||||||||||+d|')]),
     ('+bp||+l|',
      [('', 'bp||+l|'), ('b', '+p|+l|'), ('p', '+bp||l|'), ('pl', '+bp|')],
      [('d', '+bdp|||+l|'), ('bh', '+bp|+h|+l|'), ('ph', '+bp||+hl|'),
       ('pls', '+bp||+l|+s|')]),
     ('pw|ak|+h||c|x|gm||q|',
      [('pa', 'pw|k|+h|c|x|gm||q|'), ('pkcgq', 'pw|ak|+h||c|x|m|'),
       ('pkcm', 'pw|ak|+h||c|x|g||q|'), ('w', 'pw|ak|h||c|x|gm||q|'),
       ('whx', 'pw|ak|||c|gm|q|')],
      [('', '+pw|ak|+h||c|x|gm||q|'), ('p', 'pw|+ak|+h||c|x|gm||q|'),
       ('pk', 'pw|ak|+h||+c|x|gm||q|'), ('pkc', 'pw|ak|+h||c|x|+gm||q|'),
       ('pkcg', 'pw|ak|+h||c|x|gm||+q|'), ('wh', 'pw|ak|+h||c|+x|gm||q|'),
       ('pac', 'pw|ak|+h|+c|c|x||gm||q|'),
       ('pkcgqb', 'pw|ak|+h||c|x|gm||q||+b|'),
       ('pkcmk', 'pw|ak|+h||c|x|gm||q|+k|'), ('wo', 'pw|ak|+ho||c|x||gm||q|'),
       ('whxr', 'pw|ak|+h||c|x|gm|+r|q|'), ('r', 'prw|ak||+h||c|x|gm||q|'),
       ('pj', 'pw|ajk|+h|||c|x|gm||q|'), ('pkc', 'pw|ak|+h||c|x|+gm||q|'),
       ('pkci', 'pw|ak|+h||c|x|gim||q|'), ('pkcgb', 'pw|ak|+h||c|x|gm||bq|'),
       ('who', 'pw|ak|+h||c|ox|gm|||q|')]),
     ('+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|',
      [('', 'i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('i', '+i|muz||co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('im', '+i|+uz|co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('iucgb', '+i|+muz||co|g|jlq|+p||+fr||wz|dg|'),
       ('iucj', '+i|+muz||co|g|gjlq|+p||b|fr||wz|dg|'),
       ('iucjf', '+i|+muz||co|g|gjlq|+p||b|+r||wz|dg|'),
       ('iucjr', '+i|+muz||co|g|gjlq|+p||b|+f||wz|dg|'),
       ('iucl', '+i|+muz||co|g|gjq|+p||b|+fr|wz|dg|'),
       ('iucqw', '+i|+muz||co|g|gjlq|+p||b|+fr||z|dg|'),
       ('iucqz', '+i|+muz||co|g|gjlq|+p||b|+fr||w|dg|'),
       ('iuo', '+i|+muz||co|g|gjlq|p||b|+fr||wz|dg|'),
       ('iuopd', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|g|'),
       ('iuopg', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|d|'),
       ('izg', '+i|+mu||co|gjlq|+p|b|+fr||wz|dg|')],
      [('iu', '+i|+muz||+co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('iuc', '+i|+muz||co|g|+gjlq|+p||b|+fr||wz|dg|'),
       ('iucg', '+i|+muz||co|g|gjlq|+p||+b|+fr||wz|dg|'),
       ('iucq', '+i|+muz||co|g|gjlq|+p||b|+fr||+wz|dg|'),
       ('iuop', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|+dg|'),
       ('iz', '+i|+muz||co|+g|gjlq|+p||b|+fr||wz|dg|'),
       ('k', '+ik|+muz|||co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('ib', '+i|+bmuz|||co|g|gjlq|+p||b|+fr||wz|dg|'),
       ('imx', '+i|+muz|+x|co|g||gjlq|+p||b|+fr||wz|dg|'),
       ('iucgbu', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|+u|'),
       ('iucjc', '+i|+muz||co|g|gjlq|+p||b|+cfr||wz|dg|'),
       ('iucjfh', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg||+h|'),
       ('iucjrh', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|||+h|'),
       ('iucli', '+i|+muz||co|g|gjlq|+p||b|+fr|+i|wz|dg|'),
       ('iucqwf', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg||||+f|'),
       ('iucqzh', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|||||+h|'),
       ('iuoc', '+i|+muz||co|g|gjlq|+cp||b|+fr||wz||dg|'),
       ('iuopdw', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg||||||+w|'),
       ('iuopgb', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dg|||||||+b|'),
       ('izgg', '+i|+muz||co|g|gjlq|+p|+g|b|+fr||wz|dg|'),
       ('iuy', '+i|+muz||coy|g|gjlq|+p|||b|+fr||wz|dg|'),
       ('iucv', '+i|+muz||co|g|gjlqv|+p||b|+fr||wz||dg|'),
       ('iucgw', '+i|+muz||co|g|gjlq|+p||bw|+fr||wz|dg|'),
       ('iucqn', '+i|+muz||co|g|gjlq|+p||b|+fr||nwz|dg|'),
       ('iuopt', '+i|+muz||co|g|gjlq|+p||b|+fr||wz|dgt|'),
       ('izk', '+i|+muz||co|gk|gjlq|+p|||b|+fr||wz|dg|')]),
     ('ir|e|sw|+t||+y|y||+em|',
      [('ie', 'ir|e|sw|t||+y|y||+em|'), ('iety', 'ir|e|sw|+t||+y|y||em|'),
       ('ietye', 'ir|e|sw|+t||+y|y||+m|'), ('ietym', 'ir|e|sw|+t||+y|y||+e|'),
       ('rs', 'ir|e|w|+t|+y|y||+em|'), ('rw', 'ir|e|sw|+t||y|y||+em|'),
       ('rwy', 'ir|e|sw|+t|||y|+em|')],
      [('', '+ir|e|sw|+t||+y|y||+em|'), ('i', 'ir|+e|sw|+t||+y|y||+em|'),
       ('iet', 'ir|e|sw|+t||+y|+y||+em|'), ('r', 'ir|e|+sw|+t||+y|y||+em|'),
       ('iew', 'ir|e|sw|+tw||+y|y|||+em|'),
       ('ietys', 'ir|e|sw|+t||+y|y||+ems|'),
       ('ietyez', 'ir|e|sw|+t||+y|y||+em|+z|'),
       ('ietymf', 'ir|e|sw|+t||+y|y||+em||+f|'),
       ('rsk', 'ir|e|sw|+t|+k|+y|y|||+em|'),
       ('rwb', 'ir|e|sw|+t||+by|y|||+em|'),
       ('rwyu', 'ir|e|sw|+t||+y|y|+u|+em|'), ('k', 'ikr|e||sw|+t||+y|y||+em|'),
       ('iu', 'ir|eu|sw|+t|||+y|y||+em|'),
       ('ietj', 'ir|e|sw|+t||+y|jy|||+em|'),
       ('rv', 'ir|e|svw|+t|||+y|y||+em|')]),
     ('+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|',
      [('', 'josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('jq', '+osz|kw|g||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('okeb', '+josz|q|kw|g|||e||qy|bjkn|b|es|g|+v||j|h|mz|boquv|'),
       ('okebg', '+josz|q|kw|g|||e||qy|bjkn|b|es||+v||j|h|mz|boquv|'),
       ('okej', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|v||j|h|mz|boquv|'),
       ('okejv', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|||j|h|mz|boquv|'),
       ('okek', '+josz|q|kw|g|||e||qy|bjn|b|es|+g|+v|j|h|mz|boquv|'),
       ('okenj', '+josz|q|kw|g|||e||qy|bjk|b|es|+g|+v||h|mz|boquv|'),
       ('ow', '+josz|q|k|g|||e|qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('sgqbh', '+josz|q|kw|g|||e||y|bjkn|es|+g|+v||j|mz|boquv|'),
       ('sgyem', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|z|boquv|'),
       ('sgyez', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|m|boquv|'),
       ('sgysb', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|oquv|'),
       ('sgyso', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|bquv|'),
       ('sgysq', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|bouv|'),
       ('sgysu', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boqv|'),
       ('sgysv', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boqu|'),
       ('z', '+jos|q|kw|g||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|')],
      [('j', '+josz|+q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('o', '+josz|q|+kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('ok', '+josz|q|kw|g|||+e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('oke', '+josz|q|kw|g|||e||qy|+bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('oken', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||+j|h|mz|boquv|'),
       ('s', '+josz|q|kw|+g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('sg', '+josz|q|kw|g|||e||+qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('sgq', '+josz|q|kw|g|||e||qy|bjkn|+b|es|+g|+v||j|h|mz|boquv|'),
       ('sgqb', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|+h|mz|boquv|'),
       ('sgy', '+josz|q|kw|g|||e||qy|bjkn|b|+es|+g|+v||j|h|mz|boquv|'),
       ('sgye', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|+mz|boquv|'),
       ('sgys', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|+boquv|'),
       ('u', '+josuz|q|kw|g||||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('jqq', '+josz|q|kw|g||+q|e||qy||bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('okebc', '+josz|q|kw|g|||e||qy|bjkn|b|es|+cg|+v||j|h|mz|boquv|'),
       ('okebgk', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|+k|'),
       ('okejw', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+vw||j|h|mz|boquv|'),
       ('okejvo', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv||+o|'),
       ('okekq', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v|+q|j|h|mz|boquv|'),
       ('okenju', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|||+u|'),
       ('owj', '+josz|q|kw|g|||e|+j|qy|bjkn||b|es|+g|+v||j|h|mz|boquv|'),
       ('sgqbhw', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv||||+w|'),
       ('sgyems',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|||||+s|'),
       ('sgyezg',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv||||||+g|'),
       ('sgysbw',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|||||||+w|'),
       ('sgysoi',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv||||||||+i|'),
       ('sgysqa',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|||||||||+a|'),
       ('sgysuj',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv||||||||||+j|'),
       ('sgysvd',
        '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|||||||||||+d|'),
       ('zc', '+josz|q|kw|g|+c||e||qy||bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('ju', '+josz|qu|kw|g||||e||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('oy', '+josz|q|kwy|g|||e|||qy|bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('okn', '+josz|q|kw|g|||en||qy|bjkn||b|es|+g|+v||j|h|mz|boquv|'),
       ('okeo', '+josz|q|kw|g|||e||qy|bjkno|b|es|+g|+v||j||h|mz|boquv|'),
       ('okenq', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||jq|h|mz|boquv|'),
       ('so', '+josz|q|kw|go|||e||qy||bjkn|b|es|+g|+v||j|h|mz|boquv|'),
       ('sgm', '+josz|q|kw|g|||e||mqy|bjkn||b|es|+g|+v||j|h|mz|boquv|'),
       ('sgqw', '+josz|q|kw|g|||e||qy|bjkn|bw|es|+g|+v||j|h||mz|boquv|'),
       ('sgqbl', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|hl|mz|boquv|'),
       ('sgyk', '+josz|q|kw|g|||e||qy|bjkn|b|eks|+g|+v||j|h|mz||boquv|'),
       ('sgyeg', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|gmz|boquv|'),
       ('sgyse', '+josz|q|kw|g|||e||qy|bjkn|b|es|+g|+v||j|h|mz|beoquv|')]),
     ('az|az|+az|az|+az|',
      [('aaa', 'az|az|+az|z|+az|'), ('aaz', 'az|az|+az|a|+az|'),
       ('az', 'az|az|+az|az|az|'), ('aza', 'az|az|+az|az|+z|'),
       ('azz', 'az|az|+az|az|+a|'), ('z', 'az|az|az|az|+az|'),
       ('za', 'az|az|+z|az|+az|'), ('zz', 'az|az|+a|az|+az|')],
      [('', '+az|az|+az|az|+az|'), ('a', 'az|+az|+az|az|+az|'),
       ('aa', 'az|az|+az|+az|+az|'), ('aaam', 'az|az|+az|az|+az|||+m|'),
       ('aaazm', 'az|az|+az|az|+az|||+z||||m|'),
       ('aazm', 'az|az|+az|az|+az||||+m|'),
       ('aazza', 'az|az|+az|az|+az||||+z|||a|'), ('azm', 'az|az|+az|az|+amz|'),
       ('azma', 'az|az|+az|az|+amz||||||a|'),
       ('azaz', 'az|az|+az|az|+az|||||+z|'),
       ('azaza', 'az|az|+az|az|+az|||||+z||a|'),
       ('azzm', 'az|az|+az|az|+az||||||+m|'),
       ('azzaz', 'az|az|+az|az|+az||||||+a|z|'), ('zm', 'az|az|+amz|az|+az|'),
       ('zam', 'az|az|+az|az|+az|+m|'), ('zaa', 'az|az|+az|az|+az|+a|'),
       ('zazm', 'az|az|+az|az|+az|+z||||||m|'),
       ('zzz', 'az|az|+az|az|+az||+z|'),
       ('zzam', 'az|az|+az|az|+az||+a|||||m|'), ('a', 'az|+az|+az|az|+az|'),
       ('ma', 'amz|az|a|+az|az|+az|'), ('am', 'az|amz|+az|az||+az|'),
       ('ama', 'az|amz|+az|az|a|+az|'), ('aam', 'az|az|+az|amz|+az|'),
       ('aama', 'az|az|+az|amz|+az||||a|')])]


def ib002_test_report(ok, basic=False):
    if ok:
        print("[ OK ] Test prosel.")
    elif basic:
        print("[FAIL] Zakladni test neprosel.",
              "Tato cast bude automaticky hodnocena 0 body.")
    else:
        print("[FAIL] Test neprosel.")

    return ok


def ib002_test_header(msg, basic=False):
    print("\n*** {} {}:".format("Zakladni test" if basic else "Test", msg))


def ib002_test_template(msg, test_contained, test_other, basic=False):
    ib002_test_header(msg, basic)
    ok_contained, ok_other = True, True
    cases = (test_cases[0],) if basic else test_cases
    for t, contained, other in cases:
        trie = ib002_deserialize_trie(t)
        if ok_contained:
            for word, result in contained:
                if not test_contained(trie, word, result):
                    ok_contained = False
                    break
        if ok_other:
            for word, result in other:
                if not test_other(trie, word, result):
                    ok_other = False
                    break
        if not ok_contained and not ok_other:
            break

    return ib002_test_report(ok_contained and ok_other, basic)


def ib002_test_count(basic=False):
    ib002_test_header("count", basic)
    ok = True
    cases = (test_cases[0],) if basic else test_cases
    for t, good, _ in cases:
        trie = ib002_deserialize_trie(t)
        if not ib002_one_test_readonly(count, "count", "", len(good), trie):
            ok = False
            break
    return ib002_test_report(ok, basic)


def ib002_test_insert(basic=False):
    def test_contained(trie, word, _):
        return ib002_one_test_modify(insert, "insert", "_noop", trie,
                                     trie, word)

    def test_other(trie, word, result):
        return ib002_one_test_modify(insert, "insert", "_modify",
                                     ib002_deserialize_trie(result),
                                     trie, word)

    return ib002_test_template("insert", test_contained, test_other, basic)


def ib002_test_delete(basic=False):
    def test_contained(trie, word, result):
        return ib002_one_test_modify(delete, "delete", "_modify",
                                     ib002_deserialize_trie(result),
                                     trie, word)

    def test_other(trie, word, _):
        return ib002_one_test_modify(delete, "delete", "_noop", trie,
                                     trie, word)

    return ib002_test_template("delete", test_contained, test_other, basic)


def ib002_try_test(test):
    for basic in True, False:
        try:
            if not test(basic):
                break
        except Exception:
            print("[FAIL] Test vyhodil vyjimku:")
            traceback.print_exc()
            ib002_test_report(False, basic)
            break


if __name__ == '__main__':
    for test in ib002_test_count, ib002_test_insert, ib002_test_delete:
        ib002_try_test(test)
