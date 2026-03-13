import streamlit as st
import pandas as pd

st.title("Simulador Simples – Reforma Tributária para Clínicas")

st.sidebar.header("Dados da Clínica")

faturamento = st.sidebar.number_input("Faturamento Mensal (R$)", value=100000.0)
folha = st.sidebar.number_input("Folha de Pagamento Mensal (R$)", value=30000.0)
compras = st.sidebar.number_input("Compras/Insumos Mensais (R$)", value=20000.0)

iss = st.sidebar.slider("ISS (%)",2.0,5.0,5.0)/100
equiparacao = st.sidebar.checkbox("Equiparação Hospitalar")

anos = list(range(2026,2034))

def simples(fat):
    return fat*12*0.135

def presumido(fat,equip):

    fat_anual = fat*12

    base_ir = 0.08 if equip else 0.32
    base_csll = 0.12 if equip else 0.32

    irpj = fat_anual*base_ir*0.15

    if fat_anual*base_ir > 240000:
        irpj += (fat_anual*base_ir-240000)*0.10

    csll = fat_anual*base_csll*0.09

    pis_cofins = fat_anual*0.0365
    iss_valor = fat_anual*iss

    return irpj+csll+pis_cofins+iss_valor


def lucro_real(fat,folha,compras):

    fat_anual = fat*12
    folha_anual = folha*12
    compras_anual = compras*12

    lucro = fat_anual-folha_anual-compras_anual

    if lucro < 0:
        lucro = 0

    irpj = lucro*0.15

    if lucro > 240000:
        irpj += (lucro-240000)*0.10

    csll = lucro*0.09

    pis = (fat_anual*0.0925)-(compras_anual*0.0925)

    iss_valor = fat_anual*iss

    return max(pis,0)+irpj+csll+iss_valor


resultados=[]

for ano in anos:

    s = simples(faturamento)
    p = presumido(faturamento,False)
    pe = presumido(faturamento,True)
    r = lucro_real(faturamento,folha,compras)

    regimes={
        "Simples Nacional":s,
        "Lucro Presumido":p,
        "Presumido Equiparado":pe,
        "Lucro Real":r
    }

    melhor=min(regimes,key=regimes.get)

    resultados.append({
        "Ano":ano,
        "Simples Nacional":s,
        "Lucro Presumido":p,
        "Presumido Equiparado":pe,
        "Lucro Real":r,
        "Melhor Regime":melhor
    })

df=pd.DataFrame(resultados)

st.subheader("Projeção Tributária")
st.dataframe(df)

st.subheader("Comparação")

st.line_chart(df.set_index("Ano")[[
"Simples Nacional",
"Lucro Presumido",
"Presumido Equiparado",
"Lucro Real"
]])
