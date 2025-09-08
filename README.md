# 🏢 API Imobiliária

## Como Rodar o Projeto (Via Docker)
### 🔨 Fazendo o build da imagem
```sh
docker compose build
```
Isso usará o build definido no docker-compose.yml, criará a imagem reserva-sala-api:1.0 e já prepara tudo pro up.
### 🚀 Rodando a aplicação
```sh
docker compose up
```
ou em modo "background":
```sh
docker compose up -d
```
### ⛔ Parando a aplicação:
```sh
Ctrl+C
```
ou em modo "background":
```sh
docker compose down
```
### ❌ Apagando a imagem:
**Usando docker compose:**
```sh
docker compose down --rmi all
```
`--rmi all` remove todas as imagens construídas pelo docker compose;
`-v` se quiser também remover volumes

---
