# 📚 Livros API - Web Scraping com FastAPI

Este projeto é uma API REST desenvolvida com FastAPI que realiza scraping de livros de um site fictício, armazena os dados em um banco de dados relacional e fornece diversas rotas para consulta, filtro, análise e manutenção da base.

---

## 🏗️ Arquitetura

- **FastAPI** como framework principal.
- **SQLAlchemy** para ORM e conexão com banco de dados (PostgreSQL/SQLite).
- **Roteamento modular** via `APIRouter`.
- **Scripts de scraping** desacoplados, importados separadamente.
- **Pydantic** para validação de dados via schemas.
- **Swagger/OpenAPI** disponível automaticamente em `/docs`.

---

## ⚙️ Instalação e Configuração

### 1. Clone o projeto

git clone https://github.com/seu-usuario/livros-api.git
cd livros-api

2. Crie e ative um ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. Instale as dependências

pip install -r requirements.txt

4. Configure o banco de dados
Crie um arquivo .env com:

env
Copiar
Editar
DATABASE_URL=sqlite:///./livros.db  # ou substitua por PostgreSQL, ex: postgresql://user:password@host:port/dbname

5. Execute as migrações/tabelas

python scripts/criar_tabelas.py
🚀 Execução

uvicorn main:app --reload
Acesse a documentação interativa em: http://localhost:8000/docs

📌 Rotas da API
🧹 Web Scraping e Manutenção
Método	Rota	Descrição
POST	/api/v1/scraping/trigger	Realiza scraping e popula o banco de dados. Evita duplicatas.
DELETE	/api/v1/scraping/trigger/delete	Limpa todos os registros do banco.

📚 Livros
Método	Rota	Descrição
GET	/api/v1/books	Lista todos os livros (com parâmetro limit opcional).
GET	/api/v1/books/search?title=...&category=...	Busca livros por título e/ou categoria.
GET	/api/v1/books/{id}	Busca um livro pelo ID.
GET	/api/v1/books/top-rated?limit=10	Retorna os livros com maior número de estrelas.
GET	/api/v1/books/price-range?min=0&max=100	Filtra livros por faixa de preço.

📊 Estatísticas
Método	Rota	Descrição
GET	/api/v1/stats/overview	Total de livros, preço médio e distribuição de ratings.
GET	/api/v1/stats/categories	Estatísticas por categoria (quantidade, preço médio, mínimo e máximo).

📁 Utilitários
Método	Rota	Descrição
GET	/api/v1/categories	Lista todas as categorias únicas.
GET	/api/v1/health	Checagem de saúde da API e conexão com o banco.

📦 Exemplo de chamadas
🔹 Carregar base (scraping)

curl -X POST http://localhost:8000/api/v1/scraping/trigger
🔹 Listar livros

curl http://localhost:8000/api/v1/books
🔹 Buscar livro por título

curl "http://localhost:8000/api/v1/books/search?title=travel"
🔹 Estatísticas gerais

curl http://localhost:8000/api/v1/stats/overview
🧪 Testes
Você pode testar as rotas com ferramentas como:

Postman

HTTPie

Navegador (Swagger UI em /docs)

🧑‍💻 Autor
Gabriel Espanhol

📝 Licença
Este projeto é livre para uso educacional e pessoal.