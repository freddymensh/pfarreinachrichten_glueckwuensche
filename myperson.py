TYPES = ("geburtstag", "taufen", "verstorben")


class Myperson():
    anrede = None
    acad_degree = None
    first_name = None
    name_affix = None
    name = None
    alter = None
    datum = None
    ort = None
    type = None

    def __init__(self, s, t):
        assert t in TYPES

        coll = s.split(",")
        coll = s.split(";")

        # abfang leerer Zeilen
        if coll[0] =="":
            return

        self.type = t

        if self.type == TYPES[0]:       # geburtstag
            self.geburtstag_init(coll)
        elif self.type == TYPES[1]:     # taufen
            self.taufen_init(coll)
        elif self.type == TYPES[2]:     # verstorben
            self.verstorben_init(coll)
        else:
            print("argument \'t\' must be in %s", str(TYPES))

    def __str__(self):
        if self.type == TYPES[0]:  # geburtstag
            return self.geburtstag_str()
        elif self.type == TYPES[1]:  # taufen
            return self.taufen_str()
        elif self.type == TYPES[2]:  # verstorben
            return self.verstorben_str()
        else:
            print("attribute \'type\' must be in %s", str(TYPES))

    def __lt__(self, other):        # <
        # sortiere nach alter - datum - name
        if self.alter < other.alter:
            return True
        elif self.alter > other.alter:
            return False

        if str_to_date(self.datum) < str_to_date(other.datum):
            return True
        elif str_to_date(self.datum) > str_to_date(other.datum):
            return False

        if str_to_DIN5007v1(self.name) < str_to_DIN5007v1(other.name):
            return True
        else:
            return False

    def __gt__(self, other):
        return not self < other

    def __eq__(self, other):
        return self is other

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    def geburtstag_str(self):
        akad = ""
        if self.acad_degree != "":
            akad = self.acad_degree + " "

        name_affix = ""
        if self.name_affix != "":
            name_affix = self.name_affix + " "

        return self.datum[0:6] + " " + akad + self.first_name + " " + name_affix + self.name

    def taufen_str(self):
        return self.first_name + " " + self.name + " am " + self.datum + " in " + self.ort

    def verstorben_str(self):
        akad = ""
        if self.acad_degree != "":
            akad = self.acad_degree + " "
        return akad + self.first_name + " " + self.name + " (" + str(self.alter) + ") am " + self.datum

    def geburtstag_init(self, coll):
        self.datum = coll[0]
        self.alter = int(coll[1])
        self.anrede = coll[2]
        self.name = coll[3]
        self.first_name = coll[4]
        self.name_affix = coll[5]
        if coll[6] != "\n":
            self.acad_degree = coll[6][:-1]
        else:
            self.acad_degree = ""

    def taufen_init(self, coll):
        self.datum = coll[0]
        self.ort = coll[1]
        self.name = coll[2]
        self.first_name = coll[3]

    def verstorben_init(self, coll):
        self.datum = coll[0]
        self.anrede = coll[1]
        if coll[5] != "":
            self.name = coll[4] + " " + coll[2]
        else:
            self.name = coll[2]
        self.first_name = coll[3]
        self.first_name = coll[3]
        self.acad_degree = coll[5]
        self.alter = int(coll[6])


def str_to_date(s):
    import datetime
    s = s.split(".")
    for i in range(len(s)):
        s[i] = int(s[i])
    return datetime.date(s[2], s[1], s[0])


def str_to_DIN5007v1(s):
    s = s.lower()
    s = s.replace("ä", "a")
    s = s.replace("ö", "o")
    s = s.replace("ü", "u")
    s = s.replace("ß", "ss")
    return s


def str_to_DIN50007v2(s):
    s = s.lower()
    s = s.replace("ä", "ae")
    s = s.replace("ö", "oe")
    s = s.replace("ü", "ue")
    s = s.replace("ß", "ss")
    return s
