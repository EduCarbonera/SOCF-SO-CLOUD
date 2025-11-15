import os
import platform
import psutil
from flask import Flask, jsonify

app = Flask(__name__)
APP = app

nomes_equipe = ["Eduardo Mendes Carbonera", "Kaio Gonçalves Teles"]


def obter_metricas_sistema():
    """Coleta as métricas de sistema referentes ao processo atual."""
    processo = psutil.Process(os.getpid())

    pid_processo = processo.pid
    
    info_memoria = processo.memory_info()
    uso_memoria_mb = info_memoria.rss / (1024 * 1024)
    
    uso_cpu_percent = processo.cpu_percent(interval=0.1)
    
    nome_so = platform.system()
    # Tenta obter informações de distribuição
    try:
        dist_so = ' '.join(platform.freedesktop_os_release().get('NAME', '')).strip()
    except (AttributeError, OSError):
        dist_so = platform.release()

    sistema_detectado = f"{nome_so} ({dist_so})" if dist_so else nome_so

    metricas = {
        "PID": pid_processo,
        "Memória usada": f"{uso_memoria_mb:.2f} MB",
        "CPU": f"{uso_cpu_percent}%",
        "Sistema Operacional": sistema_detectado
    }
    
    return metricas


@app.route('/info')
def rota_info():
    """Retorna os nomes dos integrantes em JSON."""
    return jsonify({"integrantes": nomes_equipe})


@app.route('/metricas')
def rota_metricas():
    """Retorna as métricas do sistema em JSON."""
    dados = obter_metricas_sistema()
    return jsonify(dados)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)