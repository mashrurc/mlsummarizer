from rake_nltk import Rake, Metric
from collections import Counter
r = Rake(max_length=3) # Uses stopwords for english from NLTK, and all puntuation characters.

document='The function of this library is automatic summarization using a kind of natural language processing and neural network language model. This library enable you to create a summary with the major points of the original document or web-scraped text that filtered by text clustering. And this library applies pydbm to implement Encoder/Decoder based on LSTM (with an Attention mechanism) improving the accuracy of summarization by Sequence-to-Sequence(Seq2Seq) learning.'

r.extract_keywords_from_text(document)

# print(r.get_ranked_phrases_with_scores()) # To get keyword phrases ranked highest to lowest.

print(Counter(document.split()).most_common())

for i in range(len(r.get_ranked_phrases_with_scores())):
    t=0
    for w in r.get_ranked_phrases_with_scores()[i][1].split(" "):
        t+=document.count(w)
    print(t*r.get_ranked_phrases_with_scores()[i][0], r.get_ranked_phrases_with_scores()[i][1])
    print(r.get_ranked_phrases_with_scores()[i][0], r.get_ranked_phrases_with_scores()[i][1])
    print("-----------------------------------")


# from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
# from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
# from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# # Object of automatic summarization.
# auto_abstractor = AutoAbstractor()
# # Set tokenizer.
# auto_abstractor.tokenizable_doc = SimpleTokenizer()
# # Set delimiter for making a list of sentence.
# auto_abstractor.delimiter_list = [".", "\n"]
# # Object of abstracting and filtering document.
# abstractable_doc = TopNRankAbstractor()
# # Summarize document.
# result_dict = auto_abstractor.summarize(document, abstractable_doc)

# # Output result.
# for sentence in result_dict["summarize_result"]:
#     print(sentence)