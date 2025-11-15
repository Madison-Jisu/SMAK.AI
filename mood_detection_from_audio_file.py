from transformers import pipeline

classifier = pipeline(
    task='audio-classification',
    model='superb/hubert-large-superb-er'
)

result = classifier('final_output_happy_laugh.wav')

print(result)
print()
top_emotion = max(result, key=lambda x: x['score'])
print(f"Detected emotion: {top_emotion['label']} ({top_emotion['score']*100:.1f}%)")