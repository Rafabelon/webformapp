import streamlit as st
import dropbox
import os
from io import BytesIO

# Configurar a conexão com o Dropbox
dbx = dropbox.Dropbox(st.secrets.TOKEN_DE_ACESSO)

def upload_to_dropbox(file_content, dropbox_path):
    try:
        dbx.files_upload(file_content, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        st.success(f"Arquivo salvo com sucesso em: {dropbox_path}")
    except Exception as e:
        st.error(f"Erro ao enviar para o Dropbox: {e}")

def main():
    st.title("Cadastro de Novo Cliente")
    st.image('Zeit-Bank---Verde.png', caption='www.zeitbank.com.br')

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if st.session_state.submitted:
        st.header("Obrigado! Entraremos em contato em breve.")
    else:
        # Seleção do tipo de cadastro
        tipo_cadastro = st.selectbox("Selecione o tipo de cadastro", ["Cadastro Pessoa Física", "Cadastro Pessoa Jurídica"])

        # Seleção do serviço
        tipo_servico = st.selectbox("Selecione o serviço", ["Abertura de Conta Digital", "Máquinas de Cartão", "Ambos"])

        if st.button("Iniciar Cadastro"):
            st.session_state.tipo_cadastro = tipo_cadastro
            st.session_state.tipo_servico = tipo_servico

        if "tipo_cadastro" in st.session_state and "tipo_servico" in st.session_state:
            if st.session_state.tipo_cadastro == "Cadastro Pessoa Física":
                if st.session_state.tipo_servico == "Máquinas de Cartão":
                    cadastro_pessoa_fisica_maquinas()
                elif st.session_state.tipo_servico == "Abertura de Conta Digital":
                    cadastro_pessoa_fisica_conta()
                else:
                    cadastro_pessoa_fisica_ambos()
            else:
                if st.session_state.tipo_servico == "Máquinas de Cartão":
                    cadastro_pessoa_juridica_maquinas()
                elif st.session_state.tipo_servico == "Abertura de Conta Digital":
                    cadastro_pessoa_juridica_conta()
                else:
                    cadastro_pessoa_juridica_ambos()

def cadastro_pessoa_fisica_maquinas():
    st.header("Cadastro Pessoa Física - Máquinas de Cartão")

    nome_completo = st.text_input("Nome Completo", key="nome_completo_pf_mq")
    cpf = st.text_input("CPF", key="cpf_pf_mq")
    documento = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_pf_mq")
    arquivo_documento = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_pf_mq")

    if st.button("Submeter Cadastro"):
        salvar_dados(nome_completo, cpf, documento, arquivo_documento, None, None, None)
        st.session_state.submitted = False
        #st.experimental_rerun()

def cadastro_pessoa_fisica_conta():
    st.header("Cadastro Pessoa Física - Abertura de Conta Digital")

    nome_completo = st.text_input("Nome Completo", key="nome_completo_pf_ac")
    cpf = st.text_input("CPF", key="cpf_pf_ac")
    documento = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_pf_ac")
    arquivo_documento = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_pf_ac")
    selfie_sem_documento = st.file_uploader("Selfie sem Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_sem_documento_pf_ac")
    selfie_com_documento = st.file_uploader("Selfie com Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_com_documento_pf_ac")
    comprovante_residencia = st.file_uploader("Comprovante de Residência", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_residencia_pf_ac")

    if st.button("Submeter Cadastro"):
        salvar_dados(nome_completo, cpf, documento, arquivo_documento, selfie_sem_documento, selfie_com_documento, comprovante_residencia)
        st.session_state.submitted = True
        st.experimental_rerun()

def cadastro_pessoa_fisica_ambos():
    st.header("Cadastro Pessoa Física - Ambos")

    nome_completo = st.text_input("Nome Completo", key="nome_completo_pf_ambos")
    cpf = st.text_input("CPF", key="cpf_pf_ambos")
    documento = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_pf_ambos")
    arquivo_documento = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_pf_ambos")
    selfie_sem_documento = st.file_uploader("Selfie sem Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_sem_documento_pf_ambos")
    selfie_com_documento = st.file_uploader("Selfie com Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_com_documento_pf_ambos")
    comprovante_residencia = st.file_uploader("Comprovante de Residência", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_residencia_pf_ambos")

    if st.button("Submeter Cadastro"):
        salvar_dados(nome_completo, cpf, documento, arquivo_documento, selfie_sem_documento, selfie_com_documento, comprovante_residencia)
        st.session_state.submitted = True
        st.experimental_rerun()

def cadastro_pessoa_juridica_maquinas():
    st.header("Cadastro Pessoa Jurídica - Máquinas de Cartão")

    razao_social = st.text_input("Razão Social", key="razao_social_pj_mq")
    cnpj = st.text_input("CNPJ", key="cnpj_pj_mq")
    contrato_estatuto = st.selectbox("Contrato ou Estatuto da empresa", ["Empresário Individual", "EIRELI", "Sociedade Simples ou Limitada", "Sociedade Anônima (S.A)"], key="contrato_estatuto_pj_mq")
    arquivo_documento_empresa = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_empresa_pj_mq")
    comprovante_endereco_empresa = st.file_uploader("Comprovante de Endereço", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_endereco_empresa_pj_mq")
    documentacao_contabil = st.selectbox("Documentação Contábil", ["Balanço", "DRE", "Faturamento"], key="documentacao_contabil_pj_mq")
    arquivos_contabeis = st.file_uploader("Anexar Documentos Contábeis", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True, key="arquivos_contabeis_pj_mq")
    
    nome_representante = st.text_input("Nome Completo do Representante Legal", key="nome_representante_pj_mq")
    cpf_representante = st.text_input("CPF", key="cpf_representante_pj_mq")
    documento_representante = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_representante_pj_mq")
    arquivo_documento_representante = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_representante_pj_mq")

    if st.button("Submeter Cadastro"):
        salvar_dados_juridica(razao_social, cnpj, contrato_estatuto, arquivo_documento_empresa, comprovante_endereco_empresa, documentacao_contabil, arquivos_contabeis, nome_representante, cpf_representante, documento_representante, arquivo_documento_representante)
        st.session_state.submitted = True
        st.experimental_rerun()

def cadastro_pessoa_juridica_conta():
    st.header("Cadastro Pessoa Jurídica - Abertura de Conta Digital")

    razao_social = st.text_input("Razão Social", key="razao_social_pj_ac")
    cnpj = st.text_input("CNPJ", key="cnpj_pj_ac")
    contrato_estatuto = st.selectbox("Contrato ou Estatuto da empresa", ["Empresário Individual", "EIRELI", "Sociedade Simples ou Limitada", "Sociedade Anônima (S.A)"], key="contrato_estatuto_pj_ac")
    arquivo_documento_empresa = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_empresa_pj_ac")
    comprovante_endereco_empresa = st.file_uploader("Comprovante de Endereço", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_endereco_empresa_pj_ac")
    documentacao_contabil = st.selectbox("Documentação Contábil", ["Balanço", "DRE", "Faturamento"], key="documentacao_contabil_pj_ac")
    arquivos_contabeis = st.file_uploader("Anexar Documentos Contábeis", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True, key="arquivos_contabeis_pj_ac")
    
    nome_representante = st.text_input("Nome Completo do Representante Legal", key="nome_representante_pj_ac")
    cpf_representante = st.text_input("CPF", key="cpf_representante_pj_ac")
    documento_representante = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_representante_pj_ac")
    arquivo_documento_representante = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_representante_pj_ac")
    selfie_sem_documento_representante = st.file_uploader("Selfie sem Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_sem_documento_representante_pj_ac")
    selfie_com_documento_representante = st.file_uploader("Selfie com Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_com_documento_representante_pj_ac")
    comprovante_residencia_representante = st.file_uploader("Comprovante de Residência", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_residencia_representante_pj_ac")

    if st.button("Submeter Cadastro"):
        salvar_dados_juridica(razao_social, cnpj, contrato_estatuto, arquivo_documento_empresa, comprovante_endereco_empresa, documentacao_contabil, arquivos_contabeis, nome_representante, cpf_representante, documento_representante, arquivo_documento_representante, selfie_sem_documento_representante, selfie_com_documento_representante, comprovante_residencia_representante)
        st.session_state.submitted = True
        st.experimental_rerun()

def cadastro_pessoa_juridica_ambos():
    st.header("Cadastro Pessoa Jurídica - Ambos")

    razao_social = st.text_input("Razão Social", key="razao_social_pj_ambos")
    cnpj = st.text_input("CNPJ", key="cnpj_pj_ambos")
    contrato_estatuto = st.selectbox("Contrato ou Estatuto da empresa", ["Empresário Individual", "EIRELI", "Sociedade Simples ou Limitada", "Sociedade Anônima (S.A)"], key="contrato_estatuto_pj_ambos")
    arquivo_documento_empresa = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_empresa_pj_ambos")
    comprovante_endereco_empresa = st.file_uploader("Comprovante de Endereço", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_endereco_empresa_pj_ambos")
    documentacao_contabil = st.selectbox("Documentação Contábil", ["Balanço", "DRE", "Faturamento"], key="documentacao_contabil_pj_ambos")
    arquivos_contabeis = st.file_uploader("Anexar Documentos Contábeis", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True, key="arquivos_contabeis_pj_ambos")
    
    nome_representante = st.text_input("Nome Completo do Representante Legal", key="nome_representante_pj_ambos")
    cpf_representante = st.text_input("CPF", key="cpf_representante_pj_ambos")
    documento_representante = st.selectbox("Documento", ["CNH", "RG", "CPF"], key="documento_representante_pj_ambos")
    arquivo_documento_representante = st.file_uploader("Anexar Documento", type=["pdf", "jpg", "jpeg", "png"], key="arquivo_documento_representante_pj_ambos")
    selfie_sem_documento_representante = st.file_uploader("Selfie sem Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_sem_documento_representante_pj_ambos")
    selfie_com_documento_representante = st.file_uploader("Selfie com Documento", type=["pdf", "jpg", "jpeg", "png"], key="selfie_com_documento_representante_pj_ambos")
    comprovante_residencia_representante = st.file_uploader("Comprovante de Residência", type=["pdf", "jpg", "jpeg", "png"], key="comprovante_residencia_representante_pj_ambos")

    if st.button("Submeter Cadastro"):
        salvar_dados_juridica(razao_social, cnpj, contrato_estatuto, arquivo_documento_empresa, comprovante_endereco_empresa, documentacao_contabil, arquivos_contabeis, nome_representante, cpf_representante, documento_representante, arquivo_documento_representante, selfie_sem_documento_representante, selfie_com_documento_representante, comprovante_residencia_representante)
        st.session_state.submitted = True
        st.experimental_rerun()

def salvar_dados(nome_completo, cpf, documento, arquivo_documento, selfie_sem_documento, selfie_com_documento, comprovante_residencia):
    folder_path = f"/{nome_completo}"

    # Cria um arquivo de texto com as informações
    dados = f"Nome Completo: {nome_completo}\nCPF: {cpf}\nDocumento: {documento}\n"
    if selfie_sem_documento is not None:
        dados += "Selfie sem Documento: Sim\n"
    if selfie_com_documento is not None:
        dados += "Selfie com Documento: Sim\n"
    if comprovante_residencia is not None:
        dados += "Comprovante de Residência: Sim\n"

    upload_to_dropbox(dados.encode(), f"{folder_path}/dados.txt")

    # Salva os arquivos
    if arquivo_documento is not None:
        upload_to_dropbox(arquivo_documento.getvalue(), f"{folder_path}/{arquivo_documento.name}")

    if selfie_sem_documento is not None:
        upload_to_dropbox(selfie_sem_documento.getvalue(), f"{folder_path}/{selfie_sem_documento.name}")

    if selfie_com_documento is not None:
        upload_to_dropbox(selfie_com_documento.getvalue(), f"{folder_path}/{selfie_com_documento.name}")

    if comprovante_residencia is not None:
        upload_to_dropbox(comprovante_residencia.getvalue(), f"{folder_path}/{comprovante_residencia.name}")

    st.success(f"Cadastro de {nome_completo} salvo com sucesso!")

def salvar_dados_juridica(razao_social, cnpj, contrato_estatuto, arquivo_documento_empresa, comprovante_endereco_empresa, documentacao_contabil, arquivos_contabeis, nome_representante, cpf_representante, documento_representante, arquivo_documento_representante, selfie_sem_documento_representante=None, selfie_com_documento_representante=None, comprovante_residencia_representante=None):
    folder_path = f"/{razao_social}"

    # Cria um arquivo de texto com as informações
    dados = (
        f"Razão Social: {razao_social}\nCNPJ: {cnpj}\n"
        f"Contrato ou Estatuto da empresa: {contrato_estatuto}\n"
        f"Documentação Contábil: {documentacao_contabil}\n"
        f"Nome Completo do Representante Legal: {nome_representante}\n"
        f"CPF do Representante Legal: {cpf_representante}\n"
        f"Documento do Representante Legal: {documento_representante}\n"
    )
    if selfie_sem_documento_representante is not None:
        dados += "Selfie sem Documento do Representante: Sim\n"
    if selfie_com_documento_representante is not None:
        dados += "Selfie com Documento do Representante: Sim\n"
    if comprovante_residencia_representante is not None:
        dados += "Comprovante de Residência do Representante: Sim\n"

    upload_to_dropbox(dados.encode(), f"{folder_path}/dados.txt")

    # Salva os arquivos da empresa
    if arquivo_documento_empresa is not None:
        upload_to_dropbox(arquivo_documento_empresa.getvalue(), f"{folder_path}/{arquivo_documento_empresa.name}")

    if comprovante_endereco_empresa is not None:
        upload_to_dropbox(comprovante_endereco_empresa.getvalue(), f"{folder_path}/{comprovante_endereco_empresa.name}")

    for arquivo_contabil in arquivos_contabeis:
        upload_to_dropbox(arquivo_contabil.getvalue(), f"{folder_path}/{arquivo_contabil.name}")

    # Salva os arquivos do representante
    if arquivo_documento_representante is not None:
        upload_to_dropbox(arquivo_documento_representante.getvalue(), f"{folder_path}/{arquivo_documento_representante.name}")

    if selfie_sem_documento_representante is not None:
        upload_to_dropbox(selfie_sem_documento_representante.getvalue(), f"{folder_path}/{selfie_sem_documento_representante.name}")

    if selfie_com_documento_representante is not None:
        upload_to_dropbox(selfie_com_documento_representante.getvalue(), f"{folder_path}/{selfie_com_documento_representante.name}")

    if comprovante_residencia_representante is not None:
        upload_to_dropbox(comprovante_residencia_representante.getvalue(), f"{folder_path}/{comprovante_residencia_representante.name}")

    st.success(f"Cadastro de {razao_social} salvo com sucesso!")

if __name__ == "__main__":
    main()