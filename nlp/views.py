from django.shortcuts import render
from transformers import pipeline

# Lazy-loaded pipelines
_qa_pipeline = None
_sentiment_pipeline = None

def get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline('question-answering',
                                model='distilbert-base-cased-distilled-squad',
                                device=-1)
    return _qa_pipeline

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline('sentiment-analysis')
    return _sentiment_pipeline


def qna_view(request):
    context = {}
    if request.method == 'POST':
        paragraph = request.POST.get("paragraph")
        question = request.POST.get("question")

        if paragraph and question:
            qa = get_qa_pipeline()
            result = qa(question=question, context=paragraph)
            context['answer'] = result['answer']
            context['score'] = round(result['score'], 2)
        
        context['paragraph'] = paragraph
        context['question'] = question

    return render(request, 'nlp/qna.html', context)


def sentiment_analysis_view(request):
    context = {}
    if request.method == 'POST':
        input_text = request.POST.get("input_text")

        if input_text:
            sentiment = get_sentiment_pipeline()
            result = sentiment(input_text)[0]
            context['label'] = result['label']
            context['score'] = round(result['score'], 2)
            context['input_text'] = input_text

    return render(request, 'nlp/sentiment.html', context)
