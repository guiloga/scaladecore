class EntityFactoryError(Exception):
    def _init__(self, entity_type: str):
        self.entity_type = entity_type

    def __str_(self):
        return f'"{self.entity_type}" is not a valid entity type.'
