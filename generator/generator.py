import random
import spacy

from spacy.lang.en import English
from sense2vec import Sense2Vec
from typing import List


class Generator:
    def __init__(self, path_to_model: str) -> None:
        self.s2v_model = Sense2Vec().from_disk(path_to_model)
        self.ner_model = spacy.load("en_core_web_sm")
        self.sentencizer = English()
        self.sentencizer.add_pipe("sentencizer")

    def get_most_similar_words(
        self, keyword: str, number_of_similar_words: int
    ) -> List[str]:
        keyword_with_sense = self.s2v_model.get_best_sense(
            keyword.lower().replace(" ", "_")
        )
        if keyword_with_sense:
            most_similar_word_with_sense_list = self.s2v_model.most_similar(
                keyword_with_sense, n=number_of_similar_words
            )
            return list(
                set(
                    [
                        similar_word[0].split("|")[0].replace("_", " ")
                        for similar_word in most_similar_word_with_sense_list
                        if similar_word[0].split("|")[1]
                        == keyword_with_sense.split("|")[1]
                    ]
                )
            )
        else:
            return []

    def get_distractors(
        self, keyword: str, number_of_similar_words: int, number_of_distractors: int = 3
    ) -> List[str]:
        most_similar_word_list = self.get_most_similar_words(
            keyword, number_of_similar_words
        )
        if len(most_similar_word_list) >= number_of_distractors:
            distractor_candidates_list = [
                similar_word
                for similar_word in most_similar_word_list
                if keyword not in similar_word
            ]
            return random.sample(distractor_candidates_list, k=number_of_distractors)
        else:
            return []

    def get_person_or_gpe(self, text: str) -> List[str]:
        doc = self.ner_model(text)
        return [ent.text for ent in doc.ents if ent.label_ in ["GPE", "PERSON"]]

    def generate_mcq(self, text: str):
        sentence_list = [sent.text.strip() for sent in self.sentencizer(text).sents]
        keyword_list = self.get_person_or_gpe(text)
        sentence_to_keyword_mapping = {
            sentence: [keyword for keyword in keyword_list if keyword in sentence]
            for sentence in sentence_list
        }
        mcq_list = []
        for sentence in sentence_to_keyword_mapping.keys():
            for keyword in sentence_to_keyword_mapping[sentence]:
                distractors = self.get_distractors(keyword, 10)
                if len(distractors) != 0:
                    mcq_list.append(
                        {
                            "sentence": sentence.replace(keyword, "<blank>"),
                            "answer": keyword,
                            "distractors": distractors,
                        }
                    )

        return mcq_list


if __name__ == "__main__":
    g = Generator("s2v_models/s2v_old")
    text = 'Michael Joseph Jackson (August 29, 1958 - June 25, 2009) was an American singer, songwriter, dancer, and philanthropist. Dubbed the "King of Pop", he is regarded as one of the most significant cultural figures of the 20th century. Over a four-decade career, his contributions to music, dance, and fashion, along with his publicized personal life, made him a global figure in popular culture. Jackson influenced artists across many music genres; through stage and video performances, he popularized complicated dance moves such as the moonwalk, to which he gave the name, as well as the robot. He is the most awarded individual music artist in history.'
    print(g.generate_mcq(text))
