# Projeto

# Microservicos

### Gateway API
API REST que serve como ponto de entrada para o sistema inteiro

### DAL (sync/async)
Servico responsável pela comunicação com o banco de dados (PSQL) e toda persistência 

### Recommendation Model
Serviço responsável pela geração de modelos de ML, e gerar predictions

### External API
Serviço responsável por buscas em APIs externas/requests longos


## Uso:
Criar um arquivo .env/.dev.env seguindo o template e Rodar o docker-compose p/ dev ou produção:
> docker-compose [-f docker-compose.dev.yml] up --build
### OBS:
- Para rodar em modo de produção é necessário configurar um web server (Apache, NGINX, etc...) p/ comunicação com as APIs
- Logs dos serviços:
> docker-compose [-f docker-compose.dev.yml] log --follow
- Utilização do Redis:
> docker exec -it [redis|redis_dev] redis-cli monitor
