from app import LDA_model

LDA_plot():
    vis = gensimvis.prepare(lda_model_tfidf, bow_corpus, dictionary=lda_model_tfidf.id2word)
    return vis