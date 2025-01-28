import pytest
from messaging.bundling import split_llm_response  # Update import

@pytest.mark.parametrize("input_text, expected", [
    # Basic grouping tests
    ("", []),
    ("Single sentence.", ["Single sentence."]),
    ("First. Second.", ["First. Second."]),
    ("One. Two. Three.", ["One. Two. Three."]),
    ("A. B. C. D.", ["A. B. C. D."]),
    ('Check out my book "How Ukraine Survived": https://amzn.to/47gnlEf. You can also read it for free by signing up for a Kindle Unlimited trial at https://amzn.to/3QMsBr8. (I use affiliate links, meaning I earn a commission when you make a transaction through them. Even if you read for free, you are still supporting the channel.)',['Check out my book "How Ukraine Survived": https://amzn.to/47gnlEf. You can also read it for free by signing up for a Kindle Unlimited trial at https://amzn.to/3QMsBr8.',"(I use affiliate links, meaning I earn a commission when you make a transaction through them. Even if you read for free, you are still supporting the channel.)"]),
    ("Nosotros ofrecemos entrenamiento personalizado dentro de nuestras propias estaciones en gimnasios asociados. Cada usuario tiene su espacio individual para en trenar con la guía de su entrenador personal, enfocándonos principalmente en ejercicios de peso libre y desarrollo de fuerza y movilidad. Actualmente estamos en dos ubicaciones: Condesa y Narvarte. ¿Cuál te quedaría más cerca? 😊", ["Nosotros ofrecemos entrenamiento personalizado dentro de nuestras propias estaciones en gimnasios asociados. Cada usuario tiene su espacio individual para en trenar con la guía de su entrenador personal, enfocándonos principalmente en ejercicios de peso libre y desarrollo de fuerza y movilidad.", "Actualmente estamos en dos ubicaciones: Condesa y Narvarte. ¿Cuál te quedaría más cerca? 😊"])
    #
    # # Long sentence handling
    # (f"Short. {long_sentence()}. Another.", 
    #  ["Short.", f"{long_sentence()}", "Another."]),
    # (f"{long_sentence()} {long_sentence()}", 
    #  [f"{long_sentence()}", f"{long_sentence()}"]),
    # (f"One. {long_sentence(159)}. Three.", 
    #  [f"One. {long_sentence(159)}", "Three."]),  # 160-char sentence stays grouped
    #
    # # Mixed cases
    # ("A. B. C. D. E.", ["A. B.", "C. D.", "E."]),
    # (f"A. {long_sentence()}. C. D.", ["A.", f"{long_sentence()}", "C. D."]),
    # (f"{long_sentence()}. B. {long_sentence()}. D.", 
    #  [f"{long_sentence()}", "B.", f"{long_sentence()}", "D."]),
    #
    # # Punctuation variants
    # ("Hello! How are you? Fine!", ["Hello! How are you?", "Fine!"]),
    # ("Wait... Really?? Yes!", ["Wait... Really??", "Yes!"]),
    #
    # # Whitespace handling
    # ("  Start.   End  ", ["Start. End"]),
    # ("  A  .  B  .  ", ["A. B."]),
])

def test_split_llm_response(input_text, expected):
    assert split_llm_response(input_text) == expected


