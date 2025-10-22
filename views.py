from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Entrada
from datetime import datetime
import matplotlib.pyplot as plt
import io, base64

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/abertura', methods=['GET', 'POST'])
def abertura():
    if request.method == 'POST':
        dados = request.form
        nova = Entrada(
            emitente=dados['emitente'],
            classificação=dados['classificação'],
            empresa=dados['empresa'],
            data=datetime.strptime(dados['data'], "%Y-%m-%d").date(),
            hora=datetime.strptime(dados['hora'], "%H:%M").time(),
            local=dados['local'],
            observação=dados['observação'],
            ação=dados['ação']
        )
        db.session.add(nova)
        db.session.commit()
    entradas = Entrada.query.all()
    return render_template('abertura.html', entradas=entradas)

@views_bp.route('/graficos')
def graficos():
    entradas = Entrada.query.all()
    contagem = {}
    for e in entradas:
        key = e.classificação
        contagem[key] = contagem.get(key, 0) + 1

    fig, ax = plt.subplots()
    ax.bar(contagem.keys(), contagem.values(), color='skyblue')
    ax.set_title('Ocorrências por Classificação')
    ax.set_ylabel('Quantidade')
    ax.set_xlabel('Classificação')
    plt.xticks(rotation=0)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render_template('graficos.html', imagem=img_base64)

@views_bp.route('/ssma', methods=['GET', 'POST'])
def ssma():
    if not session.get('logado'):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        ids = request.form.getlist('id_list')
        for eid in ids:
            entrada = Entrada.query.get(eid)
            if entrada:
                entrada.class_sst = request.form.get(f'class_sst_{eid}', '')
                entrada.class_ambiental = request.form.get(f'class_ambiental_{eid}', '')
                entrada.causa = ', '.join(request.form.getlist(f'causa_{eid}'))
                entrada.parecer = request.form.get(f'parecer_{eid}', '')
                entrada.num_ordem_man = request.form.get(f'num_ordem_man_{eid}', '')
                entrada.obs_sprocedencia = request.form.get(f'obs_sprocedencia_{eid}', '')
                entrada.obs_justificativa = request.form.get(f'obs_justificativa_{eid}', '')
                entrada.multipla_condição = ', '.join(request.form.getlist(f'multipla_condição_{eid}'))
                entrada.multipla_comportamento = ', '.join(request.form.getlist(f'multipla_comportamento_{eid}'))
                entrada.multipla_ambiental = ', '.join(request.form.getlist(f'multipla_ambiental_{eid}'))
                entrada.verificação = request.form.get(f'verificacao_{eid}', '')
        db.session.commit()
        return redirect(url_for('views.ssma'))

    entradas = Entrada.query.all()
    return render_template('ssma.html', entradas=entradas)