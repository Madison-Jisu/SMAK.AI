from transformers import pipeline

classifier = pipeline(
    task='audio-classification',
    model='superb/hubert-large-superb-er'
)

# Run the classifier on a local audio file
result = classifier('final_output.wav')

print(result)
print()

# Get the highest emotion
top_emotion = max(result, key=lambda x: x['score'])
label = top_emotion['label']
score = top_emotion['score'] * 100

print(f"Detected emotion: {label} ({score:.1f}%)")

# ---- Warning logic ----
# We check specifically for "sad" or "sadness" labels depending on the model
sad_labels = ["sad", "sadness"]

if "sad" in label.lower():
    if score > 90:
        print("⚠️ Warning: Very high sadness detected. Consider reaching out for help. We are concerned about your mental health" \
        "and it's highly risky that you are this sad. Please let us know if you need any help from us, or consider getting" \
        "professional help!")
    elif score > 80:
        print("⚠️ Notice: High sadness detected. You may be feeling overwhelmed.")
    else:
        print("No high-sadness warning.")