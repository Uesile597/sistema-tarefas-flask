from database import db
from datetime import datetime, timezone

class USUARIOS(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(250), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    
    tarefas = db.relationship("TAREFAS", back_populates="usuario")
    
class TAREFAS(db.Model):
    id_tarefa = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    titulo = db.Column(db.String(250), nullable=False)
    descricao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)    
    data_conclusao = db.Column(db.Date)
    status = db.Column(db.Enum('pendente', 'em andamento', 'concluida'), default='pendente')
    
    usuario = db.relationship("USUARIOS", back_populates="tarefas")
    