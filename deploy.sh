#!/bin/bash
#preparar el servidor
sudo sysctl -w vm.max_map_count=262144
#arrancar el monitoreo
docker compose -f docker-compose.monitoring.yml logs -f

#Ver cuánta RAM consumen (Elastic suele consumir mucho):
docker stats

#Apagar solo la monitorización:
docker compose -f docker-compose.monitoring.yml down

#verificar contenido de las tablas en contenedor de docker
docker exec -it db_callcenter psql -U user -d callcenter_db -c "SELECT * FROM llamadas ORDER BY fecha_creacion DESC;"

#Este comando es como pedirle el "inventario detallado" a la bodega de Elasticsearch
curl -X GET "localhost:9200/_cat/indices?v"

