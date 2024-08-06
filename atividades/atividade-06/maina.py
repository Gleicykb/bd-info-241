from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

#1) Crie um banco de dados SQLITE3 com o nome dbalunos.db

conn = sqlite3.connect('dbalunos.db')
cursor = conn.cursor()

#2) Crie uma entidade aluno que será persistida em uma tabela TB_ALUNO

cursor.execute('''
    CREATE TABLE IF NOT EXISTS TB_ALUNO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_nome TEXT NOT NULL,
        endereco TEXT NOT NULL
    );
''')

conn.close()

class Aluno(BaseModel):
    id: int = None
    aluno_nome: str
    endereco: str

#3) Crie os seguintes endpoints FASTAPI abaixo descritos: 
#a) Criar_aluno grava dados de um objeto aluno na tabela TB_ALUNO

@app.post("/criar_aluno")
async def criar_aluno(aluno: Aluno):
    try:
        conn = sqlite3.connect('dbalunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO TB_ALUNO (aluno_nome, endereco)
            VALUES (?, ?);
        ''', (aluno.aluno_nome, aluno.endereco))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"mensagem": "Aluno criado!"}

#b) Listar_alunos ler todos os registros da tabela TB_ALUNO

@app.get("/listar_alunos", response_model=List[Aluno])
async def listar_alunos():
    try:
        conn = sqlite3.connect('dbalunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM TB_ALUNO;
        ''')
        alunos = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return [{"id": aluno[0], "aluno_nome": aluno[1], "endereco": aluno[2]} for aluno in alunos]

#c) Listar_um_aluno ler um registro da tabela TB_ALUNO a partir do campo id

@app.get("/listar_um_aluno/{id}", response_model=Aluno)
async def listar_um_aluno(id: int):
    try:
        conn = sqlite3.connect('dbalunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM TB_ALUNO
            WHERE id = ?;
        ''', (id,))
        aluno = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não foi encontrado")
    return {"id": aluno[0], "aluno_nome": aluno[1], "endereco": aluno[2]}

#d) Atualizar_aluno atualiza um registro da tabela TB_ALUNO a partir de um campo id e dos dados de uma entidade aluno

@app.put("/atualizar_aluno/{id}")
async def atualizar_aluno(id: int, aluno: Aluno):
    try:
        conn = sqlite3.connect('dbalunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE TB_ALUNO
            SET aluno_nome = ?, endereco = ?
            WHERE id = ?;
        ''', (aluno.aluno_nome, aluno.endereco, id))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"mensagem": "Aluno atualizado"}

#e) Excluir_aluno exclui um registro da tabela TB_ALUNO a partir de um campo id e dos dados de uma entidade aluno;

@app.delete("/excluir_aluno/{id}")
async def excluir_aluno(id: int):
    try:
        conn = sqlite3.connect('dbalunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM TB_ALUNO
            WHERE id = ?;
        ''', (id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"mensagem": "Aluno excluído"}
