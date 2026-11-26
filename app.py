
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscarcep", methods=["GET"])
def buscarcep():

    cep = request.args.get("cep")

    # Verifica se o CEP possui 8 dígitos
    cep = cep.replace("-", "").replace(".", "").strip() if cep else ""

    if len(cep) != 8 or not cep.isdigit():
        return render_template(
            "index.html",
            erro="CEP inválido! Digite um CEP com 8 números."
        )

    # Realiza a requisição GET para o ViaCEP
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()

        # Verifica se o CEP foi encontrado
        if dados.get("erro"):
            return render_template(
                "index.html",
                erro="CEP não encontrado!"
            )

        # Retorna a mesma página com os dados do endereço
        return render_template(
            "index.html",
            endereco=dados
        )

    except requests.RequestException:
        return render_template(
            "index.html",
            erro="Não foi possível consultar o ViaCEP. Tente novamente."
        )

if __name__ == "__main__":
    app.run(debug=True)
