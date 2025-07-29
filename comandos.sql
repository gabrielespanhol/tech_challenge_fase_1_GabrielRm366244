-- Criar Virtual env (venv):

Python -m venv nomeDaVenv

-- entrar na venv:

nomeDaVenv\Scripts\activate

-- sair da venv:

deactivate

-- rodar FastAPI:

uvicorn main:app --reload


-- criar um kernel para rodar um notebook dentro de uma venv

pip install ipykernel
python -m ipykernel install --user --name=venv6 --display-name "Python (venv6)"