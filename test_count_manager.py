from backend.count_manager import CountManager

counter = CountManager()

counter.add("Baetidae", "Baetis")
counter.add("Baetidae", "Baetis")
counter.add("Gammaridae", "Gammarus")

print(counter.get_all())
print(counter.get_total())

counter.remove("Baetidae", "Baetis")

print(counter.get_all())
print(counter.get_total())