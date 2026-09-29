from transformers import pipeline
model = pipeline(task="summarization", model="facebook/bart-large-cnn")
response = model("text to summarize")
print(response)

fiid