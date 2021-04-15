# -*- coding: utf-8 -*-
# last edit: 26th of April 2020 by Friedrich Mensing

import myperson
import sys

HELP = "help"
PATH_ARGUMENTS = ["geb_in", "geb_out", "taufe_in", "taufe_out", "verst_in", "verst_out"]
PATH_GEB = {"in": "geb.csv", "out": "emip_ausgabe_geb.txt"}
PATH_TAUFE = {"in": "taufen.csv", "out": "emip_ausgabe_taufen.txt"}
PATH_VERST = {"in": "verstorben.csv", "out": "emip_ausgabe_verstorben.txt"}

SCHEDULE_ARGUMENTS = ["geb", "taufe", "verstorben"]
SCHEDULE_CHANGED = False
SCHEDULE = {"geb": False, "taufe": False, "verst": False}

ALL = ["all"]


def main():
    # print(sys.argv)
    # arguent handling
    argument_handling()

    head()

    if SCHEDULE_CHANGED:
        if SCHEDULE["geb"]:
            geburtstage(path_eingabe=PATH_GEB["in"], path_ausgabe=PATH_GEB["out"])
        if SCHEDULE["taufe"]:
            taufen(path_eingabe=PATH_TAUFE["in"], path_ausgabe=PATH_TAUFE["out"])
        if SCHEDULE["verst"]:
            verstorben(path_eingabe=PATH_VERST["in"], path_ausgabe=PATH_VERST["out"])
    else:
        geburtstage(path_eingabe=PATH_GEB["in"], path_ausgabe=PATH_GEB["out"])
        taufen(path_eingabe=PATH_TAUFE["in"], path_ausgabe=PATH_TAUFE["out"])
        verstorben(path_eingabe=PATH_VERST["in"], path_ausgabe=PATH_VERST["out"])


def argument_handling():
    global SCHEDULE_CHANGED
    for i in sys.argv[1:]:
        if "=" in i:
            s = i.split("=")
            if PATH_ARGUMENTS[0] == s[0]:
                PATH_GEB["in"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["geb"] = True
                continue
            elif PATH_ARGUMENTS[1] == s[0]:
                PATH_GEB["out"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["geb"] = True
                continue
            elif PATH_ARGUMENTS[2] == s[0]:
                PATH_TAUFE["in"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["taufe"] = True
                continue
            elif PATH_ARGUMENTS[3] == s[0]:
                PATH_TAUFE["taufe"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["geb"] = True
                continue
            elif PATH_ARGUMENTS[4] == s[0]:
                PATH_VERST["in"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["verst"] = True
                continue
            elif PATH_ARGUMENTS[5] == s[0]:
                PATH_VERST["out"] = s[1]
                SCHEDULE_CHANGED = True
                SCHEDULE["verst"] = True
                continue

            if s[0] in SCHEDULE_ARGUMENTS:
                SCHEDULE_CHANGED = True
                argv = i.split("=")
                SCHEDULE[argv[0]] = bool(argv[1])
                continue
        if "help" in i:
            if i == "help_path":
                help_path()
                exit(0)
            if i == "help_input":
                help_input()
                exit(0)
            if i== "help_export":
                help_export()
                exit(0)
            else:
                myhelp()
                exit()
        if i in ALL:
            SCHEDULE_CHANGED = True
            for k in SCHEDULE:
                SCHEDULE[k] = True
            continue

        print("unknown argument: %s" % (i))
        exit(-1)


def myhelp():
    print(
        "\n"
        "Inputdateien sind aus der Exeldatei einzeln als casav zu speichern.\n"
        "Die Ausgabedateien werden in UTF-8 codiert und mit Windows Zeielenunbruch gespeichert.\n\n"
        "weitere Hilfen:\n"
        "\thelp: zeigt diese Hilfe\n"
        "\thelp_path: Hilfe zu Pfadangaben\n"
        "\thelp_input: zum Format der Eingabedateien\n"
        "\thelp_export: Hilfe zum exportieren aus Excel\n"
    )


def help_input():
    print(
        "Spalten TAUFEN lauten: Taufdatum	Taufkirche	Name	Vornamen\n"
        "Spalten GEBURTSTAGE: Geburtsdatum	Alter	Anrede	Name	Vorname	  Namensbest.	Akad.Grad\n"
        "Spalten VERSTORBEN: Sterbedatum	Anrede	Name	Vornamen  Namensbest.	Akad.Grad	Alter\n"
    )


def help_path():
    print("")
    print("Die Standartpfade werden genutzt, wenn nichts weiter spezifiziert wird.\n")
    print(
        "Die Standartpfade sind: \n"
        "Input:\n"
        "\t%s\n"
        "\t%s\n"
        "\t%s\n"
        "Output:\n"
        "\t%s\n"
        "\t%s\n"
        "\t%s\n"
        % (PATH_GEB["in"], PATH_TAUFE["in"], PATH_VERST["in"], PATH_GEB["out"], PATH_TAUFE["out"], PATH_VERST["out"])
    )
    print("Mit den Argumenten")
    for i in PATH_ARGUMENTS:
        print("\t" + i + "=<Dateipfad>")
    print("können die Standartpfade verändert werden.")
    print("Sobald Pfade verändert werden, werden nur noch die Teile des Programms ausgeführt, die durch eine Pfadveränderung betroffen sind.")

    print("\n")
    print("Mit Angabe von")
    for i in SCHEDULE_ARGUMENTS:
        print("\t" + i + "=<True,False>")
    print("können einzelne Programmteile ein und ausgeschaltet werden, unabhängig von Pfadänderungen\n")
    print("--BEI VERWENDUNG MEHRERER ARGUMENTE MÜSSEN DIESE DURch LEERZEICHEN VONEINANDER GETRENNT WERDEN.--")


def help_export():
    print("\nexportiere die Datei aus Excel heraus mit\n\tDatei->Exportieren->Dateityp ändern->CSV\n")
    print("Wähle \'Speichern unter\' aus\n")
    print("Wähle den Speicherort aus. und vergebe den Dateinamen.\n\tFür die einfachste handhabe speichere die Tabellenseiten in dem Ordner, wo auch dieses Skript liegt.")
    print("\tFür die Dateinamen rufe help_path auf\n")
    print("Wähle bei Dateityp CSV UTF-8 aus")


def head():
    print("")
    inp = "Inputdateien sind:"
    if SCHEDULE_CHANGED:
        if SCHEDULE["geb"]:
            inp += "\n\t" + PATH_GEB["in"]
        if SCHEDULE["taufe"]:
            inp += "\n\t" + PATH_TAUFE["in"]
        if SCHEDULE["verst"]:
            inp += "\n\t" + PATH_VERST["in"]

    else:
        inp += "\n\t" + PATH_GEB["in"]
        inp += "\n\t" + PATH_TAUFE["in"]
        inp += "\n\t" + PATH_VERST["in"]
    print(inp)

    print("")
    out = "Outputdateien sind:"
    if SCHEDULE_CHANGED:
        if SCHEDULE["geb"]:
            out += "\n\t" + PATH_GEB["out"]
        if SCHEDULE["taufe"]:
            out += "\n\t" + PATH_TAUFE["out"]
        if SCHEDULE["verst"]:
            out += "\n\t" + PATH_VERST["out"]
    else:
        out += "\n\t" + PATH_GEB["out"]
        out += "\n\t" + PATH_TAUFE["out"]
        out += "\n\t" + PATH_VERST["out"]
    print(out)

    print("")

    print("Benutze help, um die Hilfe anzuzeigen.\n")


def geburtstage(path_ausgabe="emip_ausgabe_geb.txt", path_eingabe="geb.csv"):
    file_in = open(file=path_eingabe, mode="r", encoding="UTF-8")
    personen = []
    discard = True
    for zeile in file_in:
        if discard:
            discard = False
            continue
        personen.append(myperson.Myperson(zeile, "geburtstag"))
        if personen[-1].name == None:
            personen.pop()
    file_in.close()

    import random
    random.shuffle(personen)
    personen.sort()

    file_out = open(file=path_ausgabe, mode="a", encoding="UTF-8")
    age = 0
    for i in personen:
        if i.alter > age:
            age = i.alter
            file_out.write("zum " + str(age) + ".\n")
        file_out.write(str(i) + "\n")

    file_out.close()


def taufen(path_ausgabe="emip_ausgabe_taufen.txt", path_eingabe="taufen.csv"):
    file_in = open(file=path_eingabe, mode="r")#, encoding="UTF-8")
    personen = []
    discard = True
    for zeile in file_in:
        if discard:
            discard = False
            continue
        personen.append(myperson.Myperson(zeile, "taufen"))
        if personen[-1].name == None:
            personen.pop()
    file_in.close()

    file_out = open(file=path_ausgabe, mode="a", encoding="UTF-8")
    for i in personen:
        file_out.write(str(i) + "\n")
    file_out.close()


def verstorben(path_ausgabe="emip_ausgabe_verstorben.txt", path_eingabe="verstorben.csv"):
    file_in = open(file=path_eingabe, mode="r", encoding="UTF-8")
    personen = []
    discard = True
    for zeile in file_in:
        if discard:
            discard = False
            continue
        personen.append(myperson.Myperson(zeile, "verstorben"))
        if personen[-1].name == None:
            personen.pop()
    file_in.close()

    file_out = open(file=path_ausgabe, mode="a", encoding="UTF-8")
    for i in personen:
        file_out.write(str(i) + "\n")
    file_out.close()


main()
