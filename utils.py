from colortext import *

def cube_totals_to_string(totals):
    string = ""
    if totals[0] != 0:
        string += orangetext(str(totals[0]) + " orange cube")
        if (totals[0] > 1):
            string += orangetext("s")
    if totals[1] != 0:
        if len(string) != 0:
            if totals[2] == 0:
                string += " and "
            else:
                string += ", "
        string += greentext(str(totals[1]) + " green cube")
        if (totals[1] > 1):
            string += greentext("s")
    if totals[2] != 0:
        if len(string) != 0:
            string += " and "
        string += purpletext(str(totals[2]) + " purple cube")
        if (totals[2] > 1):
            string += purpletext("s")
    return string