import speech_recognition as sr

r = sr.Recognizer()

print("Available microphones:")
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(i, mic)
