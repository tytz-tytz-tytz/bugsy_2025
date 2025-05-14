import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# --- Термины и якоря ---
with open("data/base_ontology.json", "r", encoding="utf-8") as f:
    terms = json.load(f)["terms"]

# Якоря
anchors = {
    "entities": [
        "реальный пользователь системы",
        "маркетолог или клиент",
        "бот или внешняя система",
        "участник рассылки",
        "провайдер, оператор или интеграция"
    ],
    "actions": [
        "действие, выполняемое вручную или автоматически",
        "операция в интерфейсе, такая как отправка или удаление",
        "изменение состояния рассылки или объекта",
        "ввод данных или выбор из списка",
        "команда, которую выполняет система"
    ],
    "results": [
        "результат выполнения действия",
        "состояние после запуска или завершения",
        "ошибка или успешный ответ от системы",
        "выходные данные или возвращаемое значение",
        "данные, отображаемые после выполнения сценария"
    ],
    "ui_elements": [
        "графический элемент интерфейса",
        "форма или поле ввода",
        "меню, кнопка или переключатель",
        "визуальный блок, доступный пользователю",
        "настройка, доступная в UI"
    ],
    "conditions": [
        "ограничение или правило для действия",
        "валидация ввода данных",
        "режим работы сценария или рассылки",
        "статус, блокирующий действие",
        "условие, при котором интерфейс ведёт себя иначе"
    ],
    "technical_terms": [
        "тип данных или формат",
        "структура json, csv или параметр макроса",
        "технический идентификатор или код",
        "аргумент API-запроса или события",
        "системный параметр, задающий поведение"
    ],
    "processes": [
        "логическая цепочка действий",
        "автоматизированный сценарий",
        "выполняемая последовательность операций",
        "серия событий внутри рассылки",
        "механизм работы бота или логики"
    ],
    "concepts": [
        "абстрактное понятие сценария",
        "логическая единица конфигурации",
        "бизнес-смысл внутри интерфейса",
        "настройка, не связанная напрямую с UI",
        "элемент смысловой структуры продукта"
    ],
    "objects": [
        "объект, с которым взаимодействует пользователь",
        "то, что отправляется, удаляется или настраивается",
        "цель действия — например, рассылка, сообщение или макрос",
        "единица, подлежащая изменению",
        "конкретная сущность, которую обрабатывают"
    ]
}

# --- Мусорные термины для фильтрации ---
stop_terms = {"mexico", "indian", "australia", "africa", "america", "europe", "asia", "ru", "facebook", "phone", "name"}

# --- Модель ---
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# --- Векторы якорей ---
anchor_vectors = {cat: model.encode(phrases) for cat, phrases in anchors.items()}
anchor_centroids = {cat: np.mean(vectors, axis=0) for cat, vectors in anchor_vectors.items()}

# --- Классификация с учётом близости и метки "ambiguous" ---
classified = {cat: [] for cat in anchors}
classified["ambiguous"] = []
classified["ignored"] = []

term_vectors = model.encode(terms)

for term, vec in zip(terms, term_vectors):
    if term.lower() in stop_terms:
        classified["ignored"].append(term)
        continue

    sims = {cat: cosine_similarity([vec], [centroid])[0][0] for cat, centroid in anchor_centroids.items()}
    sorted_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)

    best_cat, best_score = sorted_sims[0]
    second_cat, second_score = sorted_sims[1]

    if best_score - second_score < 0.05:
        classified["ambiguous"].append({
            "term": term,
            "options": {
                best_cat: float(round(best_score, 4)),
                second_cat: float(round(second_score, 4))
            }
        })
    else:
        classified[best_cat].append(term)

# --- Сохранение ---
with open("data/semantic_clusters.json", "w", encoding="utf-8") as f:
    json.dump(classified, f, ensure_ascii=False, indent=2)

print("Классификация завершена")
