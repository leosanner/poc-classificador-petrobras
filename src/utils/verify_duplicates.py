import re


def tokenize_text(text: str) -> list[str]:
    regex_words = r"[.,!?;:]+"
    regex_spaces = r"\s+"

    text = re.sub(regex_words, "", text)
    text = re.sub(regex_spaces, " ", text).strip()

    return text.split()


def text_similarity(text1: str, text2: str) -> float:
    tokenized_1 = tokenize_text(text1)
    tokenized_2 = tokenize_text(text2)

    token_match = 0

    for token in tokenized_1:
        if token in tokenized_2:
            token_match += 1

    return token_match / len(tokenized_1)


if __name__ == "__main__":
    print(text_similarity("Eu como feijão com arroz 3 vezes", "Eu como feijão 2 vezes"))
