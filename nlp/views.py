from django.shortcuts import render
from transformers import pipeline

# Load QnA pipeline
qa = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")


def qna_view(request):
    context = {}
    if request.method == 'POST':
        paragraph = request.POST.get("paragraph")
        question = request.POST.get("question")

        if paragraph and question:
            result = qa(question=question, context=paragraph)
            context['answer'] = result['answer']
            context['score'] = result['score']
        
        context['paragraph'] = paragraph
        context['question'] = question

    return render(request, 'nlp/qna.html', context)

sentiment_pipeline = pipeline("sentiment-analysis")

def sentiment_analysis_view(request):
    context = {}
    if request.method == 'POST':
        input_text = request.POST.get("input_text")

        if input_text:
            result = sentiment_pipeline(input_text)[0]
            context['label'] = result['label']
            context['score'] = round(result['score'], 2)
            context['input_text'] = input_text

    return render(request, 'nlp/sentiment.html', context)
