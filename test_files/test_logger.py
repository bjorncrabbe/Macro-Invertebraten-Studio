from backend.count_manager import ObservationLogger

logger = ObservationLogger()

logger.save(
    "Libellen",
    98.7,
    "Aeshnidae"
)

print("Opgeslagen!")