import streamlit as st
from news_api import get_news
from data_processing import process_news

# Configurações
api_key = "9eb39a7fe7c94564995d4988bca51040"
query = "hidrogênio verde"

# Título do dashboard
st.title("Notícias sobre Hidrogênio Verde")

# Campo de pesquisa
search_query = st.text_input("Pesquisar notícias:", "")

# Coleta de notícias
data = get_news(api_key, query)

# Processamento de notícias
news = process_news(data)

# Filtro por pesquisa
if search_query:
    news = news[news["title"].str.contains(search_query, case=False, na=False) |
                news["description"].str.contains(search_query, case=False, na=False)]

# Ordena as notícias por data de publicação em ordem decrescente
news = news.sort_values(by='publishedAt', ascending=False)

# CSS personalizado para estilização
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .news-container {
        background-color: #ffffff;
        padding: 10px;
        margin: 10px;
        border-radius: 8px;
        border: 1px solid #e1e1e1;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease-in-out;
        width: 100%; /* Largura ajustável */
        max-width: 500px; /* Largura máxima */
        height: auto; /* Altura ajustável */
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .news-container:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .news-title {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin: 5px 0;
    }
    .news-title a {
        color: #007bff;
        text-decoration: none;
    }
    .news-title a:hover {
        text-decoration: underline;
    }
    .news-date {
        font-size: 12px;
        color: #777;
        margin: 5px 0;
    }
    .news-description {
        font-size: 12px;
        color: #555;
        margin: 5px 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .news-summary {
        font-size: 12px;
        color: #444;
        font-style: italic;
        margin: 5px 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .news-image {
        border-radius: 8px;
        width: 100%;
        height: auto; /* Altura ajustável */
        object-fit: cover;
        margin-bottom: 10px;
    }
    .read-more {
        font-size: 12px;
        color: #007bff;
        text-decoration: none;
        font-weight: 600;
    }
    .read-more:hover {
        text-decoration: underline;
    }
    .news-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center; /* Centraliza os itens */
    }
    @media (max-width: 600px) {
        .news-title {
            font-size: 14px;
        }
        .news-date, .news-description, .news-summary, .read-more {
            font-size: 10px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibição de notícias em uma grade
st.markdown('<div class="news-grid">', unsafe_allow_html=True)
for index, row in news.iterrows():
    st.markdown(f"""
    <div class="news-container">
        <img src="{row['urlToImage']}" class="news-image">
        <div class="news-title"><a href="{row['url']}" target="_blank">{row['title']}</a></div>
        <div class="news-date">Data: {row['publishedAt'].strftime('%d/%m/%Y')}</div>
        <div class="news-description">{row['description']}</div>
        <div class="news-summary">Resumo: {row['summary'] if 'summary' in row else 'Nenhum resumo disponível.'}</div>
        <a href="{row['url']}" class="read-more" target="_blank">Leia mais</a>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Filtro por data
st.write("Filtro por data:")
date = st.date_input("Selecione uma data:")
if date:
    filtered_news = news[news["publishedAt"].dt.date == date]
    st.write("Notícias filtradas:")
    st.markdown('<div class="news-grid">', unsafe_allow_html=True)
    for index, row in filtered_news.iterrows():
        st.markdown(f"""
        <div class="news-container">
            <img src="{row['urlToImage']}" class="news-image">
            <div class="news-title"><a href="{row['url']}" target="_blank">{row['title']}</a></div>
            <div class="news-date">Data: {row['publishedAt'].strftime('%d/%m/%Y')}</div>
            <div class="news-description">{row['description']}</div>
            <div class="news-summary">Resumo: {row['summary'] if 'summary' in row else 'Nenhum resumo disponível.'}</div>
            <a href="{row['url']}" class="read-more" target="_blank">Leia mais</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Compartilhamento de notícias nas redes sociais
st.write("Compartilhe as notícias:")
if st.button("Compartilhar no Twitter"):
    import webbrowser
    webbrowser.open("https://twitter.com/intent/tweet?url=" + news["url"].iloc[0])
if st.button("Compartilhar no Facebook"):
    import webbrowser
    webbrowser.open("https://www.facebook.com/sharer/sharer.php?u=" + news["url"].iloc[0])
