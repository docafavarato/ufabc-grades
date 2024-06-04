from flask import Flask, render_template, url_for, request, redirect
from codes import Ufabc, apology

uf = Ufabc()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", primeira_semana=[], segunda_semana=[], duas_semanas=[])
    elif request.method == "POST":
        primeira_semana, segunda_semana = [], []
        codigos = set(request.form.get("codigosdeturma").split())
        for codigo in codigos:
            try:
                m = uf.getInfo(codigo)
                for p in m["horarios"]:
                    match p["periodicidade"]:
                        case "semanal":
                            if m not in primeira_semana and m not in segunda_semana:
                                primeira_semana.append(m)
                                segunda_semana.append(m)
                        case "quinzenal (I)":
                            if m not in primeira_semana:
                                primeira_semana.append(m)
                        case "quinzenal (II)":
                            if m not in segunda_semana:
                                segunda_semana.append(m)
            except UnboundLocalError:
                return apology("Você provavelmente inseriu os códigos incorretamente ou eu fiz alguma cagada. Acesse o <a href='https://sig.ufabc.edu.br/sigaa/verMenuPrincipal.do'>SIGAA</a> e copie os códigos destacados.<br><img style='margin-top: 1rem;' src='static/images/sigaa1.png'><br><img style='margin-top: 2rem;' src='static/images/sigaa2.png'>", go_back=url_for("index"))
            
        duas_semanas = list(primeira_semana)
        duas_semanas.extend(x for x in segunda_semana if x not in duas_semanas)
        return render_template("index.html", primeira_semana=primeira_semana, segunda_semana=segunda_semana, duas_semanas=duas_semanas)
            
if __name__ == '__main__':
    app.run(debug=True)