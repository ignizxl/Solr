FROM bitnami/solr:latest

USER root

COPY scripts/init-solr.sh /init.sh

# Ajusta as permissões do script
RUN chmod +x /init.sh && chown 1001:1001 /init.sh

# Voltar para o usuário Solr
USER 1001

EXPOSE 8983

# Criar o core no Solr na inicialização
CMD ["/init.sh"]
