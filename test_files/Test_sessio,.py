from backend.session import SessionManager

session = SessionManager()

session.create(
    "123456",
    "B. Crabbe"
)

print(session.location)
print(session.operator)
print(session.observations)