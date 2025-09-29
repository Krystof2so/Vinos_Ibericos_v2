################################
# vinos_ibericos/exceptions.py #
#                              #
# Centralisation des           #
# exceptions personnalisées    #
################################

from vinos_ibericos.config.strings import ErrorMsg


class VinedoJsonError(Exception):
    """Exception levée quand le JSON des vinedos est manquant ou invalide."""

    default_message = ErrorMsg.MSG_ERROR_JSON_VINEDO

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)
