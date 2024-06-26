import requests
import json
import json
from flask import render_template
from datetime import datetime

class Ufabc:
    def __init__(self):
        URL = "https://matricula.ufabc.edu.br/cache/todasDisciplinas.js"
        # Não consigo mais usar requisições porque teria que pagar pra hostear isso, então por enquanto vai no hardcoded mesmo
        # req = requests.get(URL).text.replace("todasDisciplinas=", "").replace(";", "")
        
        with open("data.json", encoding="utf8") as f:
            self.obj = json.load(f)

    def nomeDoDia(self, d):
        return ["SÁBADO", "SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO"][d]
    
    def getInfo(self, entry):
        turno = "Diurno" if entry[0] == "D" else "Noturno"
        turma = entry[1:3]
        code = entry[3:13]
        campus = "Santo André" if entry[-2:] == "SA" else "São Bernardo"
        
        formatted = f"{turma}-{turno} ({campus})"

        for i in self.obj:
            if formatted in i["nome"] and i["codigo"] == code:
                
                horarios = []
                for j, horario in enumerate(i["horarios"]):
                    periodicidade = horario["periodicidade_extenso"].split("- ")[1]
                    dia_index = int(horario["semana"])
                    if dia_index == 0:
                        dia_index = 6
                    horarios.append({
                        "periodicidade": periodicidade,
                        "dia": self.nomeDoDia(dia_index),
                        "horario": f"{horario['horas'][0]} às {horario['horas'][-1]}"
                    })
                    
                materia = {
                    "nome_extenso": i["nome"],
                    "nome_abreviacao": acronym(i["nome"].replace(formatted, "")),
                    "nome_materia": i["nome"].replace(formatted, ""),
                    "campus": campus,
                    "horarios": horarios,
                    "codigo": i["codigo"],  
                    "turma": turma,
                    "creditos": i["creditos"]
                }
        return materia

def apology(message, go_back):
    return render_template("apology.html", content=message, go_back=go_back)

def acronym(string):
    oupt = string[0]
    for i in range(1, len(string)):
        if string[i-1] == ' ' and string[i+1] != ' ':
            oupt += string[i]
    
    return oupt.upper()

def find_week(date):
    year, week, _ = date.isocalendar()
    if week % 2 == 1:
        return 1
    else:
        return 2
