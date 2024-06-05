import streamlit as st

def manual():
    st.title("Manual do Aplicativo")

    # Criando os botões para navegação entre as seções
    pages = {
        "Página Inicial": "Bem-vindo ao Manual do Aplicativo",
        "KPIs e Gráficos": "KPIs e Gráficos",
        "Tabelas de Estoque": "Tabelas de Estoque",
        "ROI e Payback": "ROI e Payback"
    }

    # Layout dos botões
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Página Inicial"):
            page = "Página Inicial"
    with col2:
        if st.button("KPIs e Gráficos"):
            page = "KPIs e Gráficos"
    with col3:
        if st.button("Tabelas de Estoque"):
            page = "Tabelas de Estoque"
    with col4:
        if st.button("ROI e Payback"):
            page = "ROI e Payback"

    if 'page' not in st.session_state:
        st.session_state['page'] = "Página Inicial"

    if 'page' in locals():
        st.session_state['page'] = page

    page = st.session_state['page']

    # Conteúdo das páginas
    if page == "Página Inicial":
        st.header("Bem-vindo ao Manual do Aplicativo")
        st.write("""
        Este manual fornecerá uma visão geral das funcionalidades disponíveis em nosso aplicativo. 
        Navegue pelas diferentes seções do manual usando os botões acima para obter detalhes sobre cada página.
        """)

        st.header("Aplicativo")
        st.write("""
        Para exploração do aplicativo, clique em "Relatório" na barra lateral.

        Acaso o arquivo csv contendo as peças seja atualizado, é possível o subir através da caixa "Carregar arquivo CSV" - a utilização da caixa substituirá o arquivo original, porém não o sobrescreverá na origem. Ainda, cumpre observar que o novo arquivo deverá conter as colunas 'X', 'phantom', 'vin', 'PN', 'Qtde' e 'Price', conforme padrão estipulado pelo cliente.

        Enfim, caso haja alteração na multa ou haja interesse de simulação, possível a alterar na caixa "Valor da Multa (R$)". 
        """)

    elif page == "KPIs e Gráficos":
        st.header("KPIs e Gráficos")
        st.subheader("Página: Qtdes recomendadas")
        
        st.markdown("""
        ### KPIs Apresentados:
        1. **PNs alterados**: Mostra a quantidade de números de peça (PN) que foram alterados.
        2. **Redução (R$) por dia**: Apresenta a economia diária em reais.
        3. **Redução (R$) por mês**: Apresenta a economia mensal em reais.
        4. **Redução (R$) por ano**: Apresenta a economia anual em reais.

        ### Gráfico:
        - **Quantidades Máximas vs. Recomendas**: O gráfico mostra a quantidade máxima e recomendada por PN e phantom, além da redução de gastos.
        - **Seleção de Phantom e PN**: Ao selecionar um phantom e um PN específicos, é exibido um gráfico detalhado mostrando a quantidade de peças já pedidas e o valor ótimo (indicados por uma linha tracejada vermelha).

        A página "Qtdes recomendadas" fornece uma visão detalhada das alterações nas peças e as economias associadas, permitindo que os usuários tomem decisões informadas sobre as quantidades de pedido.
        """)

    elif page == "Tabelas de Estoque":
        st.header("Tabelas de Estoque")
        st.subheader("Página de Estoque AB")
        
        st.markdown("""
        ### Descrição:
        Esta página exibe duas tabelas de estoque do tipo AB, que são usadas para classificar os itens em estoque com base em critérios como valor e volume de movimentação.

        #### Tabela 1:
        - **Estoque A**: Inclui itens que representam uma alta porcentagem do valor total do estoque, mas uma pequena porcentagem do total de itens.
        - **Estoque B**: Inclui itens que representam uma porcentagem intermediária tanto em termos de valor quanto de quantidade.

        #### Tabela 2:
        - **Estoque B (Detalhado)**: Pode fornecer uma visão mais detalhada ou uma classificação refinada dos itens do estoque B, dependendo das necessidades específicas do usuário.

        As tabelas de estoque AB ajudam na priorização de itens, focando na gestão eficiente dos itens que mais impactam financeiramente.
        """)

    elif page == "ROI e Payback":
        st.header("ROI e Payback")
        st.subheader("Página de Valores de ROI e Payback")
        
        st.markdown(r"""
        ### Descrição:
        Esta página fornece informações sobre o Retorno sobre Investimento (ROI) e o Payback de suas ações.

        #### ROI (Retorno sobre Investimento):
        - **Cálculo do ROI**: ROI é uma métrica de desempenho usada para avaliar a eficiência ou rentabilidade de um investimento. É calculado como:
        $$
          ROI = \frac{Ganho do Investimento - Custo do Investimento}{Custo do Investimento}
        $$
        - **Apresentação**: Mostra os valores de ROI, indicando o quanto de retorno foi obtido em comparação ao investimento realizado.

        #### Payback:
        - **Cálculo do Payback**: Payback é o período de tempo necessário para recuperar o investimento inicial. É uma medida simples de quanto tempo leva para que um investimento "se pague".
        - **Apresentação**: Mostra os períodos de payback, ajudando a entender o tempo necessário para que as economias ou ganhos cubram os custos iniciais.

        Esta página é crucial para entender a viabilidade econômica e o impacto financeiro das mudanças e otimizações implementadas.
        """)

