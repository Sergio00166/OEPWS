#Styles.css in pyhton :)

def color(arg="",color=""):
    if color=="B": return "[34m[1m"+arg+"[0m"
    elif color=="Bnr": return "[34m[1m"+arg
    elif color=="G": return "[32m[1m"+arg+"[0m"
    elif color=="Gnr": return "[32m[1m"+arg
    elif color=="G-": return "[32m[2m"+arg+"[0m"
    elif color=="R": return "[31m[1m"+arg+"[0m"
    elif color=="Rnr": return "[31m[1m"+arg
    elif color=="W": return "[37m[1m"+arg+"[0m"
    elif color=="Ynr": return "[33m[1m"+arg
    elif color=="Y": return "[33m[1m"+arg+"[0m"
    elif color=="Y-": return "[33m[2m"+arg+"[0m"
    elif color=="M": return "[35m[22m"+arg+"[0m"
    elif color=="Mnr": return "[35m[22m"+arg
    elif color=="C": return "[36m[22m"+arg+"[0m"
    elif color=="B-": return "[34m[22m"+arg
    elif color=="bW": return "[46m[1m"+arg+"[0m"
    elif color=="By": return "[34m[1m"+arg+"[33m[1m[0m"
    elif color=="W": return "[36m[1m"+arg+"[0m"
    elif color=="nrY": return "[33m[1m"+arg
    else: return "[0m"
