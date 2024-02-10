# Use the official Postgres image as base
FROM postgres:11.5-alpine

# Set environment variables for Postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_DB mydatabase
ENV POSTGRES_PASSWORD Welcome

# Copy SQL scripts to container
COPY init-scripts/ /docker-entrypoint-initdb.d/
