import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PetHealth - Calculadora Nutricional", page_icon="🐾", layout="wide")

# --- ESTILO CSS PERSONALIZADO (VERDE ÁGUA) ---
st.markdown("""
    <style>
    .main { background-color: #f0fdfa; }
    .stButton>button { 
        background-color: #2dd4bf; 
        color: white; 
        border-radius: 8px; 
        width: 100%;
        font-weight: bold;
    }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }
    h1, h2, h3 { color: #0f766e; }
    </style>
    """, unsafe_allow_html=True)

# --- DICIONÁRIO EXPANDIDO DE RAÇAS (PADRÃO FCI + ESTIMATIVAS) ---
base_racas = {
    "Pastor Alemão": {"macho": (30, 40), "femea": (22, 32)},
    "Border Collie": {"macho": (14, 20), "femea": (12, 19)},
    "Pastor Belga (Malinois)": {"macho": (25, 30), "femea": (20, 25)},
    "Boxer": {"macho": (30, 32), "femea": (25, 27)},
    "Rottweiler": {"macho": (50, 60), "femea": (35, 48)},
    "Bernese Mountain Dog": {"macho": (38, 50), "femea": (36, 48)},
    "Pinscher Miniatura": {"macho": (4, 6), "femea": (4, 6)},
    "Dogue Alemão": {"macho": (54, 90), "femea": (45, 59)},
    "Yorkshire Terrier": {"macho": (2, 3.2), "femea": (2, 3.2)},
    "Jack Russell Terrier": {"macho": (6, 8), "femea": (6, 8)},
    "Dachshund (Padrão)": {"macho": (7, 12), "femea": (7, 12)},
    "Akita Inu": {"macho": (32, 45), "femea": (23, 34)},
    "Spitz Alemão (Pomerânia)": {"macho": (1.9, 3.5), "femea": (1.9, 3.5)},
    "Beagle": {"macho": (10, 11), "femea": (9, 10)},
    "Labrador Retriever": {"macho": (29, 36), "femea": (25, 32)},
    "Golden Retriever": {"macho": (30, 34), "femea": (25, 32)},
    "Bulldog Francês": {"macho": (9, 14), "femea": (8, 13)},
    "Pug": {"macho": (6, 8), "femea": (6, 8)},
    "Shih Tzu": {"macho": (4.5, 8.1), "femea": (4.5, 8.1)},
    "Chihuahua": {"macho": (1.5, 3), "femea": (1.5, 3)},
    "Poodle (Standard)": {"macho": (20, 32), "femea": (20, 27)},
    "Whippet": {"macho": (12, 14), "femea": (10, 13)},
    "SRD (Porte Pequeno)": {"macho": (1, 10), "femea": (1, 9)},
    "SRD (Porte Médio)": {"macho": (11, 25), "femea": (10, 23)},
    "SRD (Porte Grande)": {"macho": (26, 45), "femea": (24, 42)}
}

# --- INTERFACE ---
st.title("🐾 Calculadora de Nutrição e Peso Canino")
st.markdown("Ferramenta de monitoramento baseada nos padrões **FCI** e fórmulas de **Nutrologia Veterinária**.")

# Criando abas para organizar o app
tab1, tab2 = st.tabs(["📊 Calculadora", "📈 Histórico de Teste"])

with tab1:
    st.subheader("Dados do Animal")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nome = st.text_input("Nome do Pet", "Rex")
        raca = st.selectbox("Raça (FCI)", list(base_racas.keys()))
        genero = st.radio("Gênero", ["Macho", "Fêmea"])

    with col2:
        peso_atual = st.number_input("Peso Atual (kg)", min_value=0.1, value=15.0, step=0.1)
        castrado = st.checkbox("Animal Castrado?")
        kcal_kg = st.number_input("Kcal/kg da Ração (Energia Metabolizável)", value=3500)

    with col3:
        objetivo = st.selectbox("Objetivo Clínico", ["Manutenção", "Perda de Peso Suave", "Perda de Peso Intensiva"])
        refeicoes = st.slider("Refeições por dia", 1, 4, 2)

    # --- LÓGICA DE CÁLCULO ---
    if st.button("GERAR DIAGNÓSTICO"):
        
        # 1. Comparação com Padrão FCI
        genero_key = genero.lower()
        min_fci, max_fci = base_racas[raca][genero_key]
        
        # 2. Cálculo da Necessidade Energética de Repouso (RER)
        # Fórmula: 70 * (peso)^0.75
        rer = 70 * (peso_atual**0.75)
        
        # 3. Definição do Fator Metabólico (K)
        # Valores baseados em diretrizes nutricionais veterinárias
        if objetivo == "Perda de Peso Intensiva":
            fator = 1.0
        elif objetivo == "Perda de Peso Suave":
            fator = 1.2
        else:
            fator = 1.6 if castrado else 1.8
            
        ned = rer * fator # Necessidade Energética Diária
        qtd_diaria = (ned / kcal_kg) * 1000 # em gramas
        
        st.divider()
        
        # --- EXIBIÇÃO DE RESULTADOS ---
        st.subheader(f"Resultado para {nome}")
        
        # Diagnóstico de Peso
        if peso_atual > max_fci:
            st.error(f"🚨 **Sobrepeso Identificado:** O peso atual está acima do padrão da raça ({max_fci}kg).")
        elif peso_atual < min_fci:
            st.warning(f"⚠️ **Abaixo do Peso:** O peso atual está abaixo do padrão da raça ({min_fci}kg).")
        else:
            st.success("✅ **Peso Ideal:** O animal está dentro dos conformes da raça para a FCI.")
            
        # Métricas Nutricionais
        m1, m2, m3 = st.columns(3)
        m1.metric("Energia Diária", f"{int(ned)} kcal")
        m2.metric("Ração Diária", f"{int(qtd_diaria)} g")
        m3.metric("Por Refeição", f"{int(qtd_diaria/refeicoes)} g")
        
        st.info("**Atenção:** Esta calculadora é uma ferramenta de triagem. A avaliação do Escore de Condição Corporal (ECC) pelo médico-veterinário é indispensável.")

with tab2:
    st.subheader("Simulação de Evolução (Data Science)")
    st.write("Exemplo de como o tutor visualizaria a perda de peso no tempo:")
    
    # Criando dados fictícios para o gráfico
    dias = pd.date_range(start='2025-11-01', periods=8, freq='W')
    pesos = [peso_atual - (i * 0.2) for i in range(8)] # Perda de 200g por semana
    
    df_evolucao = pd.DataFrame({'Data': dias, 'Peso (kg)': pesos})
    st.line_chart(df_evolucao.set_index('Data'))
    st.table(df_evolucao)

# --- RODAPÉ ---
st.divider()
st.caption("Desenvolvido para fins acadêmicos | Referência: FCI Breed Standards & NRC Guidelines")
