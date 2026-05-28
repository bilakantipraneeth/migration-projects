from .interfaces import AbstractSecretReader, AbstractSecretWriter

class SecretMigrator:
    """Orchestrates the migration using injected dependencies."""
    def __init__(self, reader: AbstractSecretReader, writer: AbstractSecretWriter):
        self.reader = reader
        self.writer = writer

    def execute(self):
        secret_data = self.reader.read_secret()
        self.writer.write_secret(secret_data)
