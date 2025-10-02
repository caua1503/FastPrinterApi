from sqlalchemy.orm import registry

# Centralized table registry for all models
table_registry = registry()
table_registry_logs = registry()
