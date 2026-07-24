from backend.sample_manager import SampleManager

sample = SampleManager()

if sample.open_sample("123456"):

    print(sample.location)
    print(sample.operator_id)
    print(sample.observation_count)
    print(sample.status)

else:

    print("Staal niet gevonden.")