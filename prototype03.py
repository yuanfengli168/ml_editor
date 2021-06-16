'''
This is a summary of code from the text book,
Differ from the code on Github:
https://github.com/hundredblocks/ml-powered-applications
(Which is a aggregation of the code and jupyter notebooks!)
'''


import argparse
import nltk


def parse_arguments():
    """
    :return: The text to be edited
    """

    parser = argparse.ArgumentParser(
        description="Receive text to be edited"
    )

    parser.add_argument(
        'text',
        metavar='input text',
        type=str
    )

    args = parser.parse_args()
    return args.text


def clean_input(text):
    """
    :param text: User input text
    :return: Sanitized text, without non ascii characters
    """
    # To keep things simple, let's only keep ASCII characters
    return str(text.encode().decode('ascii', errors='ignore'))


def preprocess_input(text):
    """

    :param text: Sanitised text
    :return: Text ready to be fed to analysis, by having sentences and words tokenized
    """

    sentences = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]


def get_suggestions(sentence_list):
    """

    Returns a string containing our suggestions
    :param sentence_list: a list of sentences, each being a list of words
    :return: suggestions to improve the input
    """

    told_said_usage = sum(
        (count_word_usage(tokens, ["told", "said"])
         for tokens in sentence_list)
    )

    but_and_usage = sum(
        (count_word_usage(tokens, ["but", "and"]) for tokens in sentence_list)
    )

    wh_adverbs_usage = sum(
        (
            count_word_usage(
                tokens,
                [
                    "when",
                    "where",
                    "why",
                    "whence",
                    "whereby",
                    "wherein",
                    "whereupon"
                ],
            ) for tokens in sentence_list
        )
    )

    result_str = ""
    adverb_usage = "Adverb usage: %s told/said, %s but/and, %s wh adverbs" % (
        told_said_usage,
        but_and_usage,
        wh_adverbs_usage,
    )

    result_str += adverb_usage
    average_word_length = compute_total_average_word_length(sentence_list)
    unique_words_fraction = compute_total_unique_words_fraction(sentence_list)

    word_stats = "Average word length %.2f" % (
        average_word_length, unique_words_fraction,)

    # using HTML break to later display on a webapp
    result_str += "<br/>"
    result_str += word_stats

    number_of_syllables = count_word_syllables(sentence_list)
    number_of_words = count_total_words(sentence_list)
    number_of_sentence = len(sentence_list)

    syllable_counts = "%d syllables, %d words, %d sentences" % (
        number_of_syllables,
        number_of_words,
        number_of_sentences,
    )

    result_str += "<br/>"
    result_str += syllable_counts

    flesch_score = compute_flesch_reading_ease(
        number_of_syllables, number_of_words, number_of_sentences
    )

    flesch = "%d syllables, %.2f flesch scores: %s" % (
        number_of_syllables,
        flesch_score,
        get_reading_level_from_flesch(flesch_score),
    )

    result_str += "<br/>"
    result_str += flesch

    return result_str
