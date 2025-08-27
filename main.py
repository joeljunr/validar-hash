from os import name
import streamlit as st
import sqlite3
import hashlib

#Função pra calcular o hash.
def calcular_hash(file):
    file.seek(0)
    data = file.read()
    file.seek(0)
    return hashlib.md5(data).hexdigest()
   
#Função pra criar a tabela no banco de dados.
def create_table():
    conn = sqlite3.connect('contratos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arquivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

#Função pra inserir arquivos na tabela.
def inserir_file(name, hash):
    conn = sqlite3.connect('contratos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO arquivos (filename, hash) VALUES (?, ?)', (name, hash))
    conn.commit()
    conn.close()

#Função pra verificar se o arquivo já foi inserido.
def check_file(name):
    conn = sqlite3.connect('contratos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hash FROM arquivos WHERE filename = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

create_table()

st.title('Verificação de Contratos')

uploaded_file = st.file_uploader('Escolha um arquivo para verificar', type=['pdf', 'docx', 'doc','txt'])

if uploaded_file is not None:

    name = uploaded_file.name
    st.success(f'Nome do arquivo: {name}')
    #calcula o hash do arquivo
    hash = calcular_hash(uploaded_file)
    st.success(f'Hash do arquivo:{hash}')
    
    hash_in_db = check_file(name)
    #Se o arquivo já foi inserido, verifica se o hash é o mesmo.
    if hash_in_db:
        if hash == hash_in_db:
            st.success('Arquivo já inserido e está integro')
        else:
            st.error('O arquivo está no banco de dados, mas é diferente do arquivo inserido')
    else:
        inserir_file(name, hash)
        st.success('Contrato inserido com sucesso')





