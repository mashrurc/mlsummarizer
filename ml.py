from rake_nltk import Rake
r = Rake(min_length=1, max_length=2) # Uses stopwords for english from NLTK, and all puntuation characters.

document = "A major theme that presents itself throughout Shakespeare’s Hamlet is one of deceit, and whether or not what seems to be real is true. In fact, a prime example of this is Hamlet’s love for Ophelia: the audience is presented with the idea that Hamlet does love her, but throughout the play, certain actions and quotes from Hamlet suggest otherwise, generating mass skepticism around Hamlet’s true intentions. In spite of this, it will become clear that Hamlet’s heart lied with Ophelia all along, and that he did in fact truly care for and love her. To properly assess the true nature of Hamlet’s affection towards Ophelia, it is important to acknowledge three time periods during the play: before Hamlet is visited by the Ghost, when Hamlet commits to his act of insanity, and after Hamlet kills Claudius. His behaviour throughout each period helps to indicate his thought process and ultimately, whether or not he truly loved her."
r.extract_keywords_from_text(document)

print(r.get_ranked_phrases_with_scores()) # To get keyword phrases ranked highest to lowest.

print("AAAAAAAAAAAAAA")

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# Object of automatic summarization.
auto_abstractor = AutoAbstractor()
# Set tokenizer.
auto_abstractor.tokenizable_doc = SimpleTokenizer()
# Set delimiter for making a list of sentence.
auto_abstractor.delimiter_list = [".", "\n"]
# Object of abstracting and filtering document.
abstractable_doc = TopNRankAbstractor()
# Summarize document.
result_dict = auto_abstractor.summarize(document, abstractable_doc)

# Output result.
for sentence in result_dict["summarize_result"]:
    print(sentence)