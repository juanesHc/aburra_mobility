"""Error unico del pipeline."""


class ErrorPipeline(Exception):
    """Fallo esperado y explicable: falta un insumo, una herramienta, etc."""
