#!/bin/bash
docker rm bigdata-db
docker run --name bigdata-db -e POSTGRES_PASSWORD=pword -p 5433:5432 -d postgres

# psql -h host.docker.internal -U postgres -p 5433 < initialize.sql