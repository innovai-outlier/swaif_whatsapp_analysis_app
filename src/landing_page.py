import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components # Importar components

# Page configuration
st.set_page_config(
    page_title="WhatsApp Analytics Pro - Transforme Conversas em Receita",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Color palette from INNOVAI portfolio
PRIMARY_COLOR = "#1B4F72"  # Dark blue from portfolio
SECONDARY_COLOR = "#5DADE2"  # Light blue from portfolio
ACCENT_COLOR = "#FF7F11"  # Orange accent
SUCCESS_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
DANGER_COLOR = "#dc3545"

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    body {{
        font-family: 'Inter', sans-serif;
    }}
    .main {{
        padding: 0;
    }}
    .hero-section {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        padding: 4rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 0;
        border-bottom-left-radius: 30px;
        border-bottom-right-radius: 30px;
    }}
    .hero-title {{
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .hero-subtitle {{
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }}
    .hero-description {{
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
        text-align: center; /* Centralizado o texto dentro do parágrafo */
    }}
    .cta-button {{
        background: {ACCENT_COLOR};
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        text-decoration: none;
        display: block; /* Alterado para display: block */
        margin: 1rem auto; /* Centraliza horizontalmente com margens automáticas */
        max-width: fit-content; /* Garante que o botão se ajuste ao conteúdo */
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 127, 17, 0.3);
        text-align: center; /* Centraliza o texto dentro do botão CTA */
    }}
    .cta-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 127, 17, 0.4);
    }}
    .section {{
        padding: 4rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }}
    .section-title {{
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 3rem;
        color: {PRIMARY_COLOR};
        font-weight: bold;
    }}
    .feature-card {{
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid {SECONDARY_COLOR};
        transition: transform 0.3s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
    }}
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        color: {ACCENT_COLOR}; /* Added color to icons */
    }}
    .feature-title {{
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: {PRIMARY_COLOR};
    }}
    .benefit-card {{
        background: linear-gradient(135deg, {SUCCESS_COLOR} 0%, #20c997 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    .metric-card {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    .metric-number {{
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}
    .metric-label {{
        font-size: 1.1rem;
        opacity: 0.9;
    }}
    .pricing-card {{
        background: white;
        border: 3px solid {ACCENT_COLOR};
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    .pricing-badge {{
        background: {ACCENT_COLOR};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        font-weight: bold;
    }}
    .price {{
        font-size: 3rem;
        font-weight: bold;
        color: {PRIMARY_COLOR};
        margin: 1rem 0;
    }}
    .testimonial {{
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid {ACCENT_COLOR};
        margin-bottom: 2rem;
        font-style: italic;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .guarantee-section {{
        background: linear-gradient(135deg, {SUCCESS_COLOR} 0%, #20c997 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 20px;
        margin: 2rem auto;
        max-width: 1000px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .footer {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 2rem;
        text-align: center;
        margin-top: 4rem;
        border-top-left-radius: 30px;
        border-top-right-radius: 30px;
    }}
    .stButton > button {{
        background: {ACCENT_COLOR};
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 127, 17, 0.3);
        transition: all 0.3s ease;
        text-align: center; /* Centraliza o texto dentro do botão do Streamlit */
    }}
    .stButton > button:hover {{
        background: #e66a00;
        border: none;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 127, 17, 0.4);
    }}
    .stExpander {{
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    .stExpander > div > div > p {{
        padding: 1rem;
    }}
    .stExpander > div > div > button {{
        background-color: {SECONDARY_COLOR};
        color: white;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <h1 class="hero-title">💬 WhatsApp Analytics Pro</h1>
    <h2 class="hero-subtitle">Transforme Conversas em Receita Garantida</h2>
    <p class="hero-description">
        Descubra exatamente quanto dinheiro sua clínica está perdendo todos os dias com leads não convertidos.
        Nossa ferramenta de análise de conversas de WhatsApp revela os padrões ocultos que separam o sucesso do fracasso.
    </p>
    <a href="#cta" class="cta-button">🚀 Quero Aumentar Minha Receita Agora</a>
</div>
""", unsafe_allow_html=True)

# Problem Section
st.markdown("""
<div class="section">
    <h2 class="section-title">🚨 O Problema Que Está Custando Caro</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📉</span>
        <h3 class="feature-title">Leads Perdidos</h3>
        <p>Você recebe leads todos os dias, mas não sabe por que alguns viram pacientes e outros simplesmente desaparecem.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">💸</span>
        <h3 class="feature-title">Dinheiro Desperdiçado</h3>
        <p>Cada lead perdido representa receita que poderia estar no seu bolso. Sem análise, você não sabe quanto está perdendo.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h3 class="feature-title">Sem Direcionamento</h3>
        <p>Sua secretária atende sem saber exatamente o que funciona, perdendo oportunidades valiosas de conversão.</p>
    </div>
    """, unsafe_allow_html=True)

# Impact Demonstration
st.markdown("""
<div class="section">
    <h2 class="section-title">💰 Quanto Você Está Perdendo?</h2>
</div>
""", unsafe_allow_html=True)

# Interactive calculator
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### 🧮 Calculadora de Custo de Oportunidade")

    leads_por_dia = st.slider("Quantos leads você recebe por dia?", 1, 20, 5)
    valor_consulta = st.slider("Qual o valor médio da sua consulta? (R$)", 100, 2000, 800, step=50)
    taxa_conversao_atual = st.slider("Qual sua taxa de conversão atual? (%)", 10, 90, 40)

    # Calculations
    taxa_conversao_otima = 70  # Target conversion rate
    leads_perdidos_dia = leads_por_dia * (1 - taxa_conversao_atual/100)
    leads_ganhos_otimizacao = leads_por_dia * (taxa_conversao_otima/100 - taxa_conversao_atual/100)

    perda_diaria = leads_perdidos_dia * valor_consulta
    perda_mensal = perda_diaria * 20  # 20 working days
    perda_anual = perda_diaria * 240  # 240 working days

    ganho_potencial_mensal = leads_ganhos_otimizacao * valor_consulta * 20
with col2:
    st.markdown("### 📊 Seu Impacto Financeiro")

    # Create metrics
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">R$ {perda_diaria:,.0f}</div>
            <div class="metric-label">Perda Diária</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">R$ {perda_anual:,.0f}</div>
            <div class="metric-label">Perda Anual</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">R$ {perda_mensal:,.0f}</div>
            <div class="metric-label">Perda Mensal</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="benefit-card">
            <div class="metric-number">+R$ {ganho_potencial_mensal:,.0f}</div>
            <div class="metric-label">Ganho Potencial Mensal</div>
        </div>
        """, unsafe_allow_html=True)

# Solution Section
st.markdown("""
<div class="section">
    <h2 class="section-title">✨ A Solução Que Vai Transformar Sua Clínica</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔍</span>
        <h3 class="feature-title">Análise Profunda</h3>
        <p>Identifique exatamente quais características das conversas levam ao sucesso ou fracasso na conversão de leads.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📈</span>
        <h3 class="feature-title">Métricas Precisas</h3>
        <p>Calcule com precisão o custo de oportunidade e o impacto financeiro de cada lead perdido.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h3 class="feature-title">Otimização Direcionada</h3>
        <p>Receba recomendações específicas para melhorar o atendimento e aumentar a taxa de conversão.</p>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="section">
    <h2 class="section-title">🚀 Funcionalidades Que Fazem a Diferença</h2>
</div>
""", unsafe_allow_html=True)

# Dashboard preview
col1, col2 = st.columns([2, 1])
with col1:
    # Create sample data for demonstration
    sample_data = pd.DataFrame({
        'Tipo': ['Sucesso', 'Falha'],
        'Quantidade': [7, 8],
        'Percentual': [46.7, 53.3]
    })

    fig = px.pie(sample_data, values='Quantidade', names='Tipo',
                 title="Taxa de Conversão Atual",
                 color_discrete_map={'Sucesso': SUCCESS_COLOR, 'Falha': DANGER_COLOR})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.markdown("""
    ### 📊 Dashboard Inteligente

        **Visualize instantaneamente:**
    - Taxa de conversão atual
    - Custo de oportunidade em tempo real
    - Métricas de performance
    - Tendências e padrões

        **Tome decisões baseadas em dados reais!**
    """)

# More features
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📝</span>
        <h3 class="feature-title">Resumos Automáticos</h3>
        <p>Cada conversa é automaticamente resumida, destacando os pontos principais e o status do lead.</p>
    </div>

    <div class="feature-card">
        <span class="feature-icon">⚙️</span>
        <h3 class="feature-title">Análise de Alinhamento</h3>
        <p>Verifique se sua secretária está seguindo suas diretrizes e onde pode melhorar.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📋</span>
        <h3 class="feature-title">Gestão de Pendências</h3>
        <p>Nunca mais perca um follow-up. Acompanhe todas as pendências por conversa.</p>
    </div>

    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <h3 class="feature-title">Recomendações Personalizadas</h3>
        <p>Receba sugestões específicas para melhorar cada aspecto do seu atendimento.</p>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section - NEW
st.markdown("""
<div class="section">
    <h2 class="section-title">💡 Como Funciona em 3 Passos Simples</h2>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 2rem;">
        <div class="feature-card" style="flex: 1; min-width: 300px; text-align: center;">
            <span class="feature-icon">1️⃣</span>
            <h3 class="feature-title">1. Faça o Upload</h3>
            <p>Exporte suas conversas do WhatsApp e faça o upload seguro para nossa ferramenta.</p>
        </div>
        <div class="feature-card" style="flex: 1; min-width: 300px; text-align: center;">
            <span class="feature-icon">2️⃣</span>
            <h3 class="feature-title">2. Análise Instantânea</h3>
            <p>Nossa IA processa as conversas, identifica padrões e calcula métricas de performance.</p>
        </div>
        <div class="feature-card" style="flex: 1; min-width: 300px; text-align: center;">
            <span class="feature-icon">3️⃣</span>
            <h3 class="feature-title">3. Otimize e Converta</h3>
            <p>Receba insights acionáveis e comece a aplicar as melhorias para aumentar sua receita.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Benefits Section
st.markdown("""
<div class="section">
    <h2 class="section-title">🎉 Resultados Que Você Vai Alcançar</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="benefit-card">
        <span class="feature-icon">📈</span>
        <h3>+30% de Conversão</h3>
        <p>Aumente sua taxa de conversão identificando e replicando padrões de sucesso.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="benefit-card">
        <span class="feature-icon">💰</span>
        <h3>+R$ 50.000/mês</h3>
        <p>Recupere receita perdida otimizando seu processo de atendimento.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="benefit-card">
        <span class="feature-icon">⏰</span>
        <h3>-80% Tempo de Análise</h3>
        <p>Automatize a análise de conversas e foque no que realmente importa.</p>
    </div>
    """, unsafe_allow_html=True)

# Testimonials
st.markdown("""
<div class="section">
    <h2 class="section-title">💬 O Que Nossos Clientes Dizem</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="testimonial">
        <p>"Em apenas 30 dias, conseguimos identificar os pontos fracos no nosso atendimento e aumentar nossa conversão em 40%. O ROI foi imediato!"</p>
        <strong>- Dra. Maria Silva, Endocrinologista</strong>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="testimonial">
        <p>"A ferramenta nos mostrou que estávamos perdendo R$ 80.000 por ano em leads mal atendidos. Agora sabemos exatamente como melhorar."</p>
        <strong>- Dr. João Santos, Cardiologista</strong>
    </div>
    """, unsafe_allow_html=True)

# Pricing Section
st.markdown("""
<div class="section">
    <h2 class="section-title">💎 Investimento Que Se Paga Sozinho</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # CSS específico para o bloco do cartão de preço, incluído dentro do HTML
    pricing_card_css = f"""
    <style>
        .pricing-card-embedded {{
            background: white;
            border: 3px solid {ACCENT_COLOR};
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem; /* Adicionado para espaçamento, se necessário */
        }}
        .pricing-badge-embedded {{
            background: {ACCENT_COLOR};
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            font-weight: bold;
        }}
        .price-embedded {{
            font-size: 3rem;
            font-weight: bold;
            color: {PRIMARY_COLOR};
            margin: 1rem 0;
        }}
        .cta-button-embedded {{
            background: {ACCENT_COLOR};
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: block;
            margin: 1rem auto;
            max-width: fit-content;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 127, 17, 0.3);
            text-align: center;
        }}
        .cta-button-embedded:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 127, 17, 0.4);
        }}
        .pricing-card-embedded ul {{
            text-align: left;
            margin: 1rem 0;
            list-style-type: none;
            padding-left: 0;
        }}
        .pricing-card-embedded li {{
            margin-bottom: 0.5rem;
        }}
    </style>
    """

    pricing_card_html = f"""
    {pricing_card_css}
    <div class="pricing-card-embedded">
        <div class="pricing-badge-embedded">🔥 OFERTA LIMITADA</div>
        <h3 style="margin-top: 2rem; color: #1B4F72;">WhatsApp Analytics Pro</h3>
        <div class="price-embedded">R$ 497</div>
        <p style="text-decoration: line-through; color: #666;">De R$ 1.997</p>
        <h4 style="color: {PRIMARY_COLOR}; margin: 2rem 0 1rem 0;">✅ Tudo Incluído:</h4>
        <ul>
            <li>✅ Sistema completo de análise</li>
            <li>✅ Dashboard interativo</li>
            <li>✅ Relatórios automáticos</li>
            <li>✅ Análise de alinhamento</li>
            <li>✅ Gestão de pendências</li>
            <li>✅ Suporte técnico completo</li>
            <li>✅ Atualizações vitalícias</li>
            <li>✅ Garantia de 30 dias</li>
        </ul>
        <a href="#cta" class="cta-button-embedded" style="width: auto;">GARANTIR MINHA LICENÇA</a>
    </div>
    """
    components.html(pricing_card_html, height=550) # Altura ajustada para o conteúdo

# Guarantee Section
st.markdown("""
<div class="guarantee-section">
    <h2>🛡️ Garantia Total de 30 Dias</h2>
    <p style="font-size: 1.2rem; margin: 1rem 0;">
        Teste por 30 dias sem risco. Se não aumentar sua conversão em pelo menos 20%,
        devolvemos 100% do seu dinheiro, sem perguntas.
    </p>
    <p style="font-size: 1rem; opacity: 0.9;">
        Você não tem nada a perder e muito dinheiro a ganhar!
    </p>
</div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown('<div id="cta"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section" style="text-align: center; background: #f8f9fa; border-radius: 20px; padding: 4rem 2rem; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
    <h2 style="color: #1B4F72; margin-bottom: 2rem;">🚀 Pare de Perder Dinheiro Hoje Mesmo!</h2>
    <p style="font-size: 1.3rem; margin-bottom: 2rem; color: #333;">
        Cada dia que você espera é dinheiro saindo do seu bolso.
        Comece a recuperar sua receita perdida agora!
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎯 QUERO AUMENTAR MINHA RECEITA AGORA", key="main_cta"):
        st.success("🎉 Obrigado pelo interesse! Em breve entraremos em contato para configurar sua ferramenta.")
        st.balloons()

# Urgency Section
st.markdown("""
<div class="section" style="text-align: center;">
    <h3 style="color: #dc3545; margin-bottom: 1rem;">⏰ ATENÇÃO: Oferta por Tempo Limitado!</h3>
    <p style="font-size: 1.1rem; color: #666;">
        Apenas 50 licenças disponíveis por mês. Garanta já a sua!
    </p>
</div>
""", unsafe_allow_html=True)

# About Us Section - NEW
st.markdown("""
<div class="section" style="background: #f0f2f6; border-radius: 20px; padding: 4rem 2rem;">
    <h2 class="section-title">✨ Sobre a INNOVAI</h2>
    <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <p style="font-size: 1.1rem; line-height: 1.7; color: #333;">
            A INNOVAI é uma empresa dedicada a desenvolver soluções inovadoras que impulsionam o crescimento e a eficiência de negócios.
            Com paixão por tecnologia e um profundo entendimento das necessidades do mercado, criamos ferramentas inteligentes
            que transformam dados em resultados tangíveis. Nosso compromisso é com o sucesso dos nossos clientes,
            oferecendo produtos de alta qualidade e suporte excepcional.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.7; color: #333; margin-top: 1rem;">
            O WhatsApp Analytics Pro é o resultado de anos de pesquisa e desenvolvimento, projetado para capacitar clínicas
            e profissionais da saúde a maximizar seu potencial de conversão e otimizar a comunicação com seus pacientes.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# FAQ Section
st.markdown("""
<div class="section">
    <h2 class="section-title">❓ Perguntas Frequentes</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("🤔 Como funciona a análise das conversas?"):
    st.write("""
    Nossa ferramenta utiliza inteligência artificial para analisar automaticamente suas conversas de WhatsApp,
    identificando padrões de linguagem, tempo de resposta, tipos de perguntas e outros fatores que influenciam
    na conversão de leads em pacientes.
    """)
with st.expander("📊 Que tipo de relatórios vou receber?"):
    st.write("""
    Você receberá dashboards interativos com métricas de conversão, custo de oportunidade,
    análise de alinhamento da equipe, resumos automáticos das conversas e recomendações
    personalizadas para melhorar seu atendimento.
    """)
with st.expander("🔒 Meus dados ficam seguros?"):
    st.write("""
    Sim! Todos os dados são processados localmente em seu computador. Nenhuma conversa
    é enviada para servidores externos. Sua privacidade e a de seus pacientes está 100% protegida.
    """)
with st.expander("⏱️ Quanto tempo leva para ver resultados?"):
    st.write("""
    Os primeiros insights aparecem imediatamente após o upload das conversas.
    Melhorias na conversão podem ser observadas já na primeira semana de implementação
    das recomendações.
    """)
with st.expander("🛠️ Preciso de conhecimento técnico?"):
    st.write("""
    Não! A ferramenta foi desenvolvida para ser extremamente fácil de usar.
    Basta fazer upload dos arquivos de conversa e tudo é automatizado.
    Incluímos suporte completo e treinamento.
    """)

# Footer
st.markdown(f"""
<div class="footer">
    <h3>💬 WhatsApp Analytics Pro</h3>
    <p>Transformando conversas em receita desde 2024</p>
    <p>© 2024 INNOVAI - Todos os direitos reservados</p>
    <p>📧 contato@innovai.com.br | 📱 (11) 99999-9999</p>
</div>
""", unsafe_allow_html=True)

# Hidden tracking/analytics (placeholder)
st.markdown("""
<script>
    // Placeholder for actual analytics code (e.g., Google Analytics, Matomo)
    // This would typically involve loading an external script and initializing it.
    // Example:
    /*
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-XXXXX-Y', 'auto');
    ga('send', 'pageview');
    */
</script>
""", unsafe_allow_html=True)
