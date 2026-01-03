from flask import request, jsonify, render_template, flash, redirect, url_for, session
from database import db
from models import USUARIOS, TAREFAS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from sqlalchemy import func

status_map = {
    "pendente": {
        "label": "PENDENTE",
        "classe": "status-pendente"
    },
    
    "em andamento": {
        "label": "EM ANDAMENTO",
        "classe": "status-andamento"
    },
    
    "concluida": {
        "label": "CONCLUÍDA",
        "classe": "status-concluida"
    }
}

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("LOGIN.html")

    @app.route("/LOGIN", methods=["GET", "POST"])
    def Login():
        if request.method == "POST":
            email = request.form.get("email")
            senha = request.form.get("senha")

            if not email or not senha:
                flash("Email e senha são obrigatórios !", "warning")
                return redirect(url_for("Login"))
            
            usuario = USUARIOS.query.filter_by(email=email).first()
            
            if not usuario or not check_password_hash(usuario.senha, senha):
                flash("Email ou senha incorretos !", "error")
                return redirect(url_for('Login'))
            
            session["usuario_id"] = usuario.id_usuario
            session["usuario_nome"] = usuario.nome
            
            return redirect(url_for('Inicio'))
        return render_template("LOGIN.html")
    
    @app.route("/CADASTRO", methods=["GET", "POST"])
    def Cadastro():
        if request.method == "POST":
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            telefone = request.form.get("telefone")
            
            if not nome or not email or not senha or not telefone:
                flash("Nome, email, senha e telefone são obrigatórios !", "warning")
                return redirect(url_for('Cadastro'))
            
            usuario = USUARIOS.query.filter_by(email=email).first()
            if usuario:
                flash("Email já cadastrado !", "error")
                return redirect(url_for('Cadastro'))
            
            senha_hash = generate_password_hash(senha)
            novo_usuario = USUARIOS(
                nome=nome,
                email=email,
                senha=senha_hash,
                telefone=telefone
            )
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash("Usuário cadastrado com sucesso !", "success")
            return redirect(url_for('Login'))
        return render_template("CADASTRO.html")
    
    @app.route("/ESQUECISENHA", methods=["GET", "POST"])
    def Trocar_Senha():
        if request.method == "POST":
            email = request.form.get("email")
            nova_senha = request.form.get("nova_senha")
            confirmar_nova_senha = request.form.get("confirmar_nova_senha")
            
            if not email or not nova_senha or not confirmar_nova_senha:
                flash("Email e nova senha são obrigatórios !", "warning")
                return redirect(url_for('Trocar_Senha'))
            
            if nova_senha != confirmar_nova_senha:
                flash("A nova senha e a confirmação tem que ser iguais !", "warning")
                return redirect(url_for('Trocar_Senha'))
            
            usuario = USUARIOS.query.filter_by(email=email).first()
            
            if not usuario:
                flash("Email não cadastrado", "error")
                return redirect(url_for('Trocar_Senha'))
            
            if check_password_hash(usuario.senha, nova_senha):
                flash("A nova senha tem que ser diferente da antiga !", "warning")
                return redirect(url_for('Trocar_Senha'))
            
            usuario.senha = generate_password_hash(nova_senha)
            db.session.commit()
            
            flash("Senha alterada com sucesso !", "success")
            return redirect(url_for('Login'))
        return render_template("ESQUECISENHA.html")
    
    @app.route("/ADICIONARTAREFA", methods=["GET", "POST"])
    def Adicionar_Tarefa():
        if "usuario_id" not in session:
            flash("Faça login para continuar", "warning")
            return redirect(url_for('Login'))
        
        if request.method == "POST":
            titulo = request.form.get("titulo")
            descricao = request.form.get("descricao")
            data_conclusao_str = request.form.get("data_conclusao")
            
            if not titulo:
                flash("O título é obrigatório !", "warning")
                return redirect(url_for('Adicionar_Tarefa'))
            
            if data_conclusao_str:
                data_conclusao = datetime.strptime(data_conclusao_str, "%Y-%m-%d").date()
            else:
                data_conclusao = None
            
            nova_tarefa = TAREFAS (
                titulo=titulo,
                descricao=descricao,
                data_conclusao=data_conclusao,
                id_usuario=session["usuario_id"]
            )
            db.session.add(nova_tarefa)
            db.session.commit()
            
            flash("Tarefa adicionada com sucesso !", "success")
            return redirect(url_for('Inicio'))
        return render_template("ADICIONARTAREFA.html")
    
    @app.route("/EDITARTAREFAS", methods=["GET", "POST"])
    def EditarTarefa():
        if "usuario_id" not in session:
            flash("Faça login para continuar !", "warning")
            return redirect(url_for('Login'))
        
        if request.method == "POST":
            id_tarefa = request.form.get("id")
            titulo = request.form.get("titulo")
            descricao = request.form.get("descricao")
            data_conclusao_str = request.form.get("data_conclusao")
            status = request.form.get("status")
            
            tarefa = TAREFAS.query.filter_by(id_tarefa=id_tarefa, id_usuario=session["usuario_id"]).first()
            
            if not tarefa:
                flash("Tarefa não existe !", "error")
                return redirect(url_for('EditarTarefa'))
            
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            if data_conclusao_str:
                tarefa.data_conclusao = datetime.strptime(data_conclusao_str, "%Y-%m-%d").date()
            tarefa.status = status
            
            db.session.commit()
            flash("Tarefa editada com sucesso", "success")
            return redirect(url_for('EditarTarefa'))
    
        titulo_busca = request.args.get("titulo_busca")
        
        tarefas = []    
        
        if titulo_busca:
            tarefas = TAREFAS.query.filter(TAREFAS.titulo.ilike(f"%{titulo_busca}%"), TAREFAS.id_usuario == session["usuario_id"]).all()
            if not tarefas:
                flash("Nenhuma tarefa com esse título cadastrada !", "error")
                return redirect(url_for('EditarTarefa'))
            
        return render_template("EDITARTAREFA.html", tarefas=tarefas, status_map=status_map)    
    
    @app.route("/EXCLUIRTAREFA", methods=["GET"])
    def ListarTarefas():
        if "usuario_id" not in session:
            flash("Faça login para continuar !", "warning")
            return redirect(url_for('Login'))
        
        
        titulo_busca = request.args.get("titulo_busca")
        tarefas = []    
        
        if titulo_busca:
            tarefas = TAREFAS.query.filter(
                TAREFAS.titulo.ilike(f"%{titulo_busca}%"), 
                TAREFAS.id_usuario == session["usuario_id"]
            ).all()
        
            if not tarefas:
                flash("Nenhuma tarefa com esse título cadastrada !", "error")
        
        return render_template("EXCLUIRTAREFA.html", tarefas=tarefas, status_map=status_map) 

    @app.route("/EXCLUIRTAREFA/excluir", methods=["POST"])
    def ExcluirTarefa():
        if "usuario_id" not in session:
            flash("Faça login para continuar !", "warning")
            return redirect(url_for('Login'))
        
        if not request.is_json:
            return jsonify({"mensagem": "Content-Type deve ser application/json"}), 415

        dados = request.get_json()
        
        if not dados or "id_tarefa" not in dados:
            return jsonify({"mensagem": "Nenhuma tarefa selecionada !"}), 400

        id_tarefas = dados["id_tarefa"]
        
        tarefas = TAREFAS.query.filter(
            TAREFAS.id_tarefa.in_(id_tarefas), 
            TAREFAS.id_usuario == session["usuario_id"]
        ).all()
        
        if not tarefas:
            return jsonify({"mensagem": "Nenhuma tarefa encontrada !"}), 404
        
        for tarefa in tarefas:
            db.session.delete(tarefa)
            
        db.session.commit()
        
        return jsonify({"mensagem": "Tarefas excluídas com sucesso!"})
    
    @app.route("/DASHBOARD", methods=["GET"])
    def Dashboard():
        if "usuario_id" not in session:
            flash("Faça login para continuar !", "warning")
            return redirect(url_for('Login'))
        
        dados = (
            db.session.query(TAREFAS.status, func.count(TAREFAS.id_tarefa).label("total"))
            .filter(TAREFAS.id_usuario == session["usuario_id"])
            .group_by(TAREFAS.status)
            .all()
        )
        
        labels = []
        valores = []
        
        for status, total in dados:
            labels.append(status)
            valores.append(total)
        
        total_tarefas = TAREFAS.query.filter(
            TAREFAS.id_usuario == session["usuario_id"]
        ).count()
        
        vencem_hoje = TAREFAS.query.filter(
            TAREFAS.data_conclusao == date.today(),
            TAREFAS.id_usuario == session["usuario_id"]
        ).all()
        
        tarefas_concluidas = (
            db.session.query(func.count(TAREFAS.id_tarefa))
            .filter(TAREFAS.id_usuario == session["usuario_id"],
                    TAREFAS.status == "concluida")
            .scalar()
        )
        
        tarefas_criadas = (
            db.session.query(func.count(TAREFAS.id_tarefa))
            .filter(TAREFAS.id_usuario == session["usuario_id"])
            .scalar()
        )
        
        tarefas_vencidas = TAREFAS.query.filter(
            TAREFAS.id_usuario == session["usuario_id"],
            TAREFAS.data_conclusao < date.today()
        ).all()
        
        usuario = USUARIOS.query.filter(
            USUARIOS.id_usuario == session["usuario_id"],
        ).first()
        
        return render_template("DASHBOARD.html", dados=dados, total_tarefas=total_tarefas, vencem_hoje=vencem_hoje, tarefas_concluidas=tarefas_concluidas, tarefas_criadas=tarefas_criadas, tarefas_vencidas=tarefas_vencidas, usuario=usuario, labels=labels, valores=valores)
            
    @app.route("/INICIO")
    def Inicio():
        if "usuario_id" not in session:
            flash("Faça login para continuar !", "warning")
            return redirect(url_for('Login'))
        
        tarefas = TAREFAS.query.filter(TAREFAS.id_usuario == session["usuario_id"]).all()
        return render_template("INICIO.html", tarefas=tarefas, status_map=status_map)