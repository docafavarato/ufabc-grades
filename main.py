import math
from flask import Flask, render_template, url_for, request, redirect
from codes import Ufabc, apology,find_week
import datetime
from zoneinfo import ZoneInfo

uf = Ufabc()
app = Flask(__name__)

dias_da_semana = {
    "Monday": "SEGUNDA",
    "Tuesday": "TERÇA",
    "Wednesday": "QUARTA",
    "Thursday": "QUINTA",
    "Friday": "SEXTA",
    "Saturday": "SÁBADO",
    "Sunday": "DOMINGO"
}

@app.route("/", methods=["GET", "POST"])
def index():
    week = find_week(datetime.datetime.now(ZoneInfo("Brazil/East")))
    if request.method == "GET":
        return render_template("index.html", primeira_semana=[], segunda_semana=[], duas_semanas=[], linhas_primeira=5, linhas_segunda=5, week=week)
    elif request.method == "POST":
        dia_semana_ing = datetime.datetime.now(ZoneInfo("Brazil/East")).strftime('%A')
        dia_atual = dias_da_semana[dia_semana_ing]
        primeira_semana, segunda_semana = [], []
        codigos = set(request.form.get("codigosdeturma").split())
        horarios_primeira_semana = 0 
        horarios_segunda_semana = 0
        for codigo in codigos:
            try:
                m = uf.getInfo(codigo)
                for p in m["horarios"]:
                    match p["periodicidade"]:
                        case "semanal":
                            horarios_primeira_semana += 1
                            horarios_segunda_semana += 1
                            if m not in primeira_semana and m not in segunda_semana:
                                primeira_semana.append(m)
                                segunda_semana.append(m)
                        case "quinzenal (I)":
                            horarios_primeira_semana += 1
                            if m not in primeira_semana:
                                primeira_semana.append(m)       
                        case "quinzenal (II)":
                            horarios_segunda_semana += 1
                            if m not in segunda_semana:
                                segunda_semana.append(m)

            except UnboundLocalError:
                return apology("Você provavelmente inseriu os códigos incorretamente ou eu fiz alguma cagada. Acesse o <a href='https://sig.ufabc.edu.br/sigaa/verMenuPrincipal.do'>SIGAA</a> e copie os códigos destacados.<br><img style='margin-top: 1rem;' src='static/images/sigaa1.png'><br><img style='margin-top: 2rem;' src='static/images/sigaa2.png'>", go_back=url_for("index"))
            
        duas_semanas = list(primeira_semana)
        duas_semanas.extend(x for x in segunda_semana if x not in duas_semanas)
        return render_template("index.html", dia_atual=dia_atual, primeira_semana=primeira_semana, segunda_semana=segunda_semana, duas_semanas=duas_semanas,linhas_primeira=math.ceil(horarios_primeira_semana / 5), linhas_segunda=math.ceil(horarios_segunda_semana / 5), week=week)
            
if __name__ == '__main__':
    app.run(debug=True)