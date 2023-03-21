from typing import Iterable

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class BadWordsDetector:
    def __init__(
        self,
        model_file: str = "wordsdetector/trained/model.joblib",
        csv_file: str = "wordsdetector/dataset/words.csv",
    ):
        if model_file:
            self.model = joblib.load(model_file)
        else:
            self.model = Pipeline(
                [
                    ("vectorizer", CountVectorizer()),
                    ("transformer", TfidfTransformer()),
                    ("classifier", LogisticRegression()),
                ]
            )
        self.csv_file = csv_file
        self.model_file = model_file

    async def train(self) -> None:
        data = pd.read_csv(self.csv_file, quotechar="`", engine="python")
        X = data["comment"].values
        y = data["toxic"].values
        self.model.fit(X, y)
        await self.save()

    async def predict(self, comments: tuple | str) -> tuple | int:
        if isinstance(comments, tuple):
            return tuple(map(int, self.model.predict(comments)))
        return int(self.model.predict((comments,)))

    async def save(self) -> None:
        joblib.dump(self.model, self.model_file)

    async def add_text_data(self, comment: str, toxic: int | float) -> None:
        with open(self.csv_file, "a", encoding="utf-8") as f:
            f.write(f"`{comment}`,{float(toxic)}\n")

    async def add_large_text_data(
        self, comments: Iterable[str], toxic: int | float
    ) -> None:
        with open(self.csv_file, "a", encoding="utf-8") as f:
            f.write("".join([f"`{comment}`,{float(toxic)}\n" for comment in comments]))
