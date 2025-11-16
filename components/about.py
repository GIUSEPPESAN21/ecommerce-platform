"""
About page component with company and team information.
"""
import streamlit as st


def render_about_content():
    """Render about page content."""
    st.title("About Us")
    st.markdown("---")
    
    # Company Information
    st.markdown("## 🏢 SAVA Software for Engineering")
    
    col_logo_about, col_info = st.columns([1, 3])
    
    with col_logo_about:
        st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO.jpg?raw=true", width=200)
    
    with col_info:
        st.markdown("""
        **SAVA Software for Engineering** es una empresa líder en desarrollo de software 
        e inteligencia artificial, especializada en crear soluciones innovadoras que 
        transforman la forma en que las empresas operan.
        
        Nuestra misión es proporcionar tecnología de vanguardia que impulse el crecimiento 
        y la eficiencia de nuestros clientes, combinando experiencia técnica con visión estratégica.
        """)
    
    st.markdown("---")
    
    # CEO Section
    st.markdown("## 👔 Leadership Team")
    
    col1_founder, col2_founder = st.columns([1, 3])
    
    with col1_founder:
        st.image("https://placehold.co/200x200/667eea/FFFFFF?text=CEO", width=200, caption="CEO")
    
    with col2_founder:
        st.markdown("#### Joseph Javier Sánchez Acuña")
        st.markdown("**CEO - SAVA SOFTWARE FOR ENGINEERING**")
        st.write("""
        Líder visionario con una profunda experiencia en inteligencia artificial y desarrollo de software.
        Joseph es el cerebro detrás de la arquitectura de OSIRIS, impulsando la innovación
        y asegurando que nuestra tecnología se mantenga a la vanguardia.
        """)
        st.markdown(
            """
            - **LinkedIn:** [joseph-javier-sánchez-acuña](https://www.linkedin.com/in/joseph-javier-sánchez-acuña-150410275)
            - **GitHub:** [GIUSEPPESAN21](https://github.com/GIUSEPPESAN21)
            """
        )
    
    st.markdown("---")
    
    st.markdown("##### 👥 Cofundadores")
    
    c1_cof, c2_cof, c3_cof = st.columns(3)
    
    with c1_cof:
        st.info("**Xammy Alexander Victoria Gonzalez**\n\n*Director Comercial*")
    
    with c2_cof:
        st.info("**Jaime Eduardo Aragon Campo**\n\n*Director de Operaciones*")
    
    with c3_cof:
        st.info("**Joseph Javier Sanchez Acuña**\n\n*Director de Proyecto*")
    
    st.markdown("---")
    
    # Company Values
    st.markdown("## 💎 Our Values")
    
    val_col1, val_col2, val_col3 = st.columns(3)
    
    with val_col1:
        st.markdown("""
        ### 🚀 Innovation
        Constantemente buscamos nuevas formas de resolver problemas 
        y mejorar nuestras soluciones.
        """)
    
    with val_col2:
        st.markdown("""
        ### 🤝 Collaboration
        Trabajamos en equipo para lograr resultados excepcionales 
        y construir relaciones duraderas.
        """)
    
    with val_col3:
        st.markdown("""
        ### ⭐ Excellence
        Nos comprometemos a entregar productos de la más alta calidad 
        que superen las expectativas.
        """)
    
    st.markdown("---")
    
    # Contact Information
    st.markdown("## 📧 Contact Us")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("""
        **GitHub:** [SAVA Software](https://github.com/GIUSEPPESAN21)
        
        **LinkedIn:** [Joseph Javier Sánchez Acuña](https://www.linkedin.com/in/joseph-javier-sánchez-acuña-150410275)
        """)
    
    with contact_col2:
        st.markdown("""
        **Email:** info@savasoftware.com
        
        **Website:** www.savasoftware.com
        """)

