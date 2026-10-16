🏃 Running Analytics
Dashboard interativo para visualização e análise de treinos de corrida, integrado à API do Strava. Construído com Python, Streamlit e Plotly.

https://img.shields.io/badge/Python-3.10%2B-blue
https://img.shields.io/badge/Streamlit-1.30%2B-red
https://img.shields.io/badge/License-MIT-green

📖 Sobre o Projeto
O Running Analytics consome dados de atividades diretamente da sua conta do Strava via OAuth 2.0 e apresenta métricas, gráficos e uma tabela detalhada em um dashboard web interativo. Ideal para corredores que querem acompanhar evolução de pace, distância, elevação e frequência cardíaca ao longo do tempo.

✨ Funcionalidades
🔐 Autenticação OAuth 2.0 com o Strava (login seguro, sem armazenar senha).

🔄 Renovação automática do token de acesso via refresh_token.

📊 Métricas agregadas do período filtrado: total de atividades, distância, tempo e elevação.

📈 Gráficos interativos com Plotly:

Evolução da distância por atividade.

Distribuição de distâncias.

Evolução de pace em corridas.

🗂️ Tabela detalhada com todas as atividades carregadas.

🎛️ Filtros dinâmicos por tipo de esporte e intervalo de datas.

🖼️ Preview
<img width="1446" height="844" alt="image" src="https://github.com/user-attachments/assets/7e8a936a-77d4-4691-b11e-c846cc71f374" />


🚀 Começando
Pré-requisitos
Python 3.10+

Uma conta no Strava

Um aplicativo criado no Strava API Settings (gratuito)

1. Clone o repositório
bash
git clone https://github.com/fabriciosro/running-analytics.git
cd running-analytics
2. Crie e ative um ambiente virtual
bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Instale as dependências
bash
pip install -r requirements.txt
4. Configure as credenciais do Strava
Crie a pasta .streamlit e, dentro dela, o arquivo secrets.toml:

bash
mkdir .streamlit
Conteúdo de .streamlit/secrets.toml:

toml
[strava]
client_id = "SEU_CLIENT_ID"
client_secret = "SEU_CLIENT_SECRET"
redirect_uri = "http://localhost:8501"
💡 Use o arquivo .streamlit/secrets.toml.example como modelo. Nunca faça commit do secrets.toml real.

5. Configure o app no Strava
Acesse https://www.strava.com/settings/api e crie um novo aplicativo:

Campo	Valor
Application Name	Running Analytics
Category	Data Visualization
Website	http://localhost:8501
Authorization Callback Domain	localhost
Anote o Client ID e o Client Secret e coloque-os no secrets.toml.

6. Rode a aplicação
bash
streamlit run app.py
O Streamlit abrirá automaticamente em http://localhost:8501.

🔐 Como Funciona a Autenticação
O app usa o Authorization Code Flow do OAuth 2.0:

Tokens armazenados apenas em st.session_state (memória), nunca em disco.

Renovação automática quando o access_token expira (a cada 6h).

Escopo utilizado: activity:read_all.
     
	
🛠️ Tecnologias Utilizadas
Tecnologia	Uso
Python	Linguagem principal
Streamlit	Framework do dashboard
Plotly	Gráficos interativos
Pandas	Tratamento de dados
Requests	Chamadas HTTP à API do Strava
Strava API v3	Fonte dos dados
⚙️ Variáveis de Configuração
Todas as configurações sensíveis ficam em .streamlit/secrets.toml:

Variável	Descrição	Obrigatória
client_id	Client ID do app no Strava	✅
client_secret	Client Secret do app no Strava	✅
redirect_uri	URI de callback registrada no Strava	✅
📊 Métricas Calculadas
O app transforma os dados brutos da API em métricas úteis:

Métrica	Fórmula
distance_km	distance / 1000
moving_time_min	moving_time / 60
moving_time_h	moving_time / 3600
pace_min_km	moving_time_min / distance_km
🧪 Testando Localmente
bash
# Rodar em modo debug
streamlit run app.py --logger.level=debug

# Rodar em porta diferente
streamlit run app.py --server.port=8502
Lembre-se de atualizar o redirect_uri no secrets.toml e o Callback Domain no Strava se mudar a porta.

☁️ Deploy no Streamlit Cloud
Faça push do repositório (sem o secrets.toml) para o GitHub.

Acesse share.streamlit.io e conecte o repositório.

Em Settings → Secrets, cole:

toml
[strava]
client_id = "SEU_CLIENT_ID"
client_secret = "SEU_CLIENT_SECRET"
redirect_uri = "https://seu-app.streamlit.app"
No painel do Strava, atualize o Authorization Callback Domain para seu-app.streamlit.app.

Faça o deploy. 🚀

🔒 Segurança
Nunca faça commit do .streamlit/secrets.toml.

O client_secret nunca deve ser exposto no frontend ou em logs.

Tokens de acesso ficam apenas em memória (st.session_state).

Use o .gitignore incluído para evitar vazamentos acidentais.

Ative Secret Scanning e Push Protection nas configurações do GitHub.

Se você commitou credenciais por engano:

Resete o Client Secret em Strava API Settings.

Remova o arquivo do histórico com git filter-repo ou BFG.

Force push e avise colaboradores.

⚠️ Limites da API do Strava
Limite	Valor
Requisições por 15 min	100
Requisições por dia	1000
Páginas buscadas por execução	10 (configurável em max_pages)
Atividades por página	100 (máximo)
O app busca até 1000 atividades por execução. Ajuste max_pages em app.py se necessário.

🗺️ Roadmap
□ Mapa de calor de treinos por dia da semana.
□ Comparação mês a mês e ano a ano.
□ Zonas de frequência cardíaca.
□ Exportação de dados para CSV/Excel.
□ Modo escuro.
□ Cache com @st.cache_data para reduzir chamadas à API.
□ Testes automatizados com pytest.
□ Suporte a múltiplos atletas.
🤝 Contribuindo
Contribuições são bem-vindas!

Faça um fork do projeto.

Crie uma branch: git checkout -b feature/minha-feature.

Commit suas mudanças: git commit -m 'feat: adiciona nova funcionalidade'.

Push para a branch: git push origin feature/minha-feature.

Abra um Pull Request.

Siga o padrão Conventional Commits.

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

🙏 Agradecimentos
Strava pela API pública.

Streamlit pelo framework incrível.

Comunidade open source. 💙

📬 Contato
Fabricio Rosa

GitHub: @fabriciosro

LinkedIn: fabriciosro
