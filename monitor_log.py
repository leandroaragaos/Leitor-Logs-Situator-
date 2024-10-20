import streamlit as st
import os
import time
import re

# Configuração para o layout ocupar a largura total da página
st.set_page_config(page_title="Atende - Logs Situator", layout="wide")

# Caminho do arquivo de log
log_path = r"C:\ProgramData\Seventh\Situator\Logs\situator.log"

# Dicionário modular de palavras-chave e cores
KEYWORDS = {
    "red": [
        "falha", "error", "nao foi possivel", "Não foi possível enviar a foto da pessoa",
        "Não foi possível realizar o envio de todas as fotos", "falha ao estabelecer conexão com o dispositivo",
        "Falha na sincronização total no dispositivo", "falha enviar tabela", "pupilDistanceTooSmall", 
        "picFormatError", "Ocorreu um erro ao sincronizar o dispositivo MIP 1000", "Não foi possível remover a tag"
    ],
    "orange": [
        "Não foi possível remover a imagem do usuário", "Ocorreu um erro ao buscar os horários do telefone",
        "Falha ao notificar evento recebido", "Não foi possível criar o evento remoto",
        "Sincronização parcial do dispostivo", "não está conectado", "Visitante/Prestador", "ATENÇÂO"
    ],
    "green": [
        "realizada com sucesso", "Sincronização total do dispositivo",
        "Sincronização de dispositivos concluída com sucesso", "sucesso", "Fim da sincronização total do dispositivo MIP 1000"
    ],
    "blue": [
        "Iniciando conexão com o dispositivo", "Iniciando a sincronização", "Iniciando sincronização"
    ]
}

# Função para destacar as palavras-chave com cores
def highlight_keywords(text):
    for color, words in KEYWORDS.items():
        for word in words:
            text = re.sub(f"(?i)\\b{word}\\b", f"<span style='color:{color}; font-weight:bold;'>{word}</span>", text)
    return text

# Função para monitorar e buscar no arquivo de log com base no termo e nas palavras-chave selecionadas
def search_log(term, selected_keywords):
    results = []
    term = term.lower()  # Convertendo o termo de busca para minúsculas
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    line_lower = line.lower()
                    if term in line_lower:
                        if not selected_keywords or any(kw.lower() in line_lower for kw in selected_keywords):
                            results.append(highlight_keywords(line.strip()))
        except UnicodeDecodeError:
            with open(log_path, 'r', encoding='latin-1') as log_file:
                for line in log_file:
                    line_lower = line.lower()
                    if term in line_lower:
                        if not selected_keywords or any(kw.lower() in line_lower for kw in selected_keywords):
                            results.append(highlight_keywords(line.strip()))
    else:
        st.error("Arquivo de log não encontrado.")
    return results

# Sidebar para logo, campo de busca, e seleção de palavras-chave
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Logs - Situator")

# Campo de busca
search_term = st.sidebar.text_input("Digite o nome ou o IP do dispositivo")
auto_search = st.sidebar.checkbox("Ativar busca automática")

# Listar as keywords na sidebar e permitir seleção múltipla
# st.sidebar.subheader("Selecione as palavras-chave (opcional):")
all_keywords = [kw for color in KEYWORDS.values() for kw in color]  # Lista de todas as keywords
selected_keywords = st.sidebar.multiselect("Palavras-chave:", options=all_keywords)

# Título na área principal
st.markdown("<h2 style='text-align: center; color: grey;'>Acompanhe os Logs</h2>", unsafe_allow_html=True)

# Espaço para os resultados dos logs
log_container = st.empty()

# Variável para manter os resultados anteriores
if "previous_results" not in st.session_state:
    st.session_state["previous_results"] = []

# Função para atualizar os resultados e rolar para o final
def update_results():
    results = search_log(search_term, selected_keywords)
    if results != st.session_state["previous_results"]:
        st.session_state["previous_results"] = results
        result_text = "<br>".join(results)
        with log_container:
            st.markdown(result_text, unsafe_allow_html=True)

# Loop de atualização automática
if search_term:
    update_results()
    if auto_search:
        while auto_search:
            time.sleep(2)
            update_results()
else:
    st.write("Digite o nome ou o IP do dispositivo para iniciar a busca.")

# Rodapé fixo na parte inferior da página ocupando toda a extensão da tela
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f0f0;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        border-top: 1px solid #d4d4d4;
        z-index: 1000;
    }
    .css-1d391kg {  /* Ajusta o padding da área principal da Streamlit */
        padding-bottom: 80px;
    }
    </style>
    <div class="footer">
        Atende Portaria @2024 - Leandro Aragão
    </div>
    """,
    unsafe_allow_html=True,
)
