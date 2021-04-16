TYPES = ("geburtstag", "taufen", "verstorben") # TODO in config


class Person():
    anrede = None
    acad_degree = None
    first_name = None
    name_affix = None
    name = None
    alter = None
    datum = None
    ort = None
    mode = None

    def __init__(self, df, mode):
        assert mode in TYPES
        self.mode = mode

        if self.mode == TYPES[0]:       # geburtstag
            self.geburtstag_init(df)
        elif self.mode == TYPES[1]:     # taufen
            self.taufen_init(df)
        elif self.mode == TYPES[2]:     # verstorben
            self.verstorben_init(df)
        else:
            print("argument \'t\' must be in %s", str(TYPES))

    def __str__(self):
        if self.mode == TYPES[0]:  # geburtstag
            return self.geburtstag_str()
        elif self.mode == TYPES[1]:  # taufen
            return self.taufen_str()
        elif self.mode == TYPES[2]:  # verstorben
            return self.verstorben_str()
        else:
            print("attribute \'type\' must be in %s", str(TYPES))

    def __lt__(self, other):        # <
        # sortiere nach alter - datum - name
        if self.alter < other.alter:
            return True
        elif self.alter > other.alter:
            return False

        if self.datum < other.datum:
            return True
        elif self.datum > other.datum:
            return False

#        if str_to_DIN5007v1(self.name) < str_to_DIN5007v1(other.name):
#            return True
#        else:
#            return False

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

        return self.datum[0:6] + " " + akad + self.first_name + " " + name_affix + self.name #TODO: Timestamp to string

    def taufen_str(self):
        return self.first_name + " " + self.name + " am " + self.datum + " in " + self.ort

    def verstorben_str(self):
        akad = ""
        if self.acad_degree != "":
            akad = self.acad_degree + " "
        return akad + self.first_name + " " + self.name + " (" + str(self.alter) + ") am " + self.datum

    def geburtstag_init(self, df):
        df = df.fillna("")
        self.datum = df.iloc[0][['Geburtsdatum']].values[0]
        self.alter = df.iloc[0][['Alter']].values[0]
        self.anrede = df.iloc[0][['Anrede']].values[0]
        self.name = df.iloc[0][['Name']].values[0]
        self.first_name = df.iloc[0][['Rufname']].values[0]
        self.name_affix = df.iloc[0][['Namensbest.']].values[0]
        self.acad_degree = df.iloc[0][['Akad.Grad']].values[0]

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
