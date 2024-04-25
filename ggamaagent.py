from __future__ import annotations
from pathlib import Path
from typing import Optional

import pickle
import os
import toml

from llama_index.core import GPTVectorStoreIndex
from llama_index.readers.github import GithubClient, GithubRepositoryReader

from ggamaconfig import Config
            

class Agent:
    def __init__(self, config: Config):
        self.knowledge = None
        self.query_engine = None
        self.index = None
        self.config = config

    def load(self):
        config = self.config
        try:
            self.knowledge = pickle.load(config.vector_file.open("rb"))
        except (OSError, TypeError):
            self.knowledge = None
            print(f"-- couldn't load existing knowledge file {config.vector_file}")

        if self.knowledge is None:
            print("-- creating new knowledge file")
            client = GithubClient(self.config.github_token)
            knowledge = GithubRepositoryReader(
                        client,
                        owner=self.config.github_user, repo=self.config.github_repos,
                        use_parser=True,
                        verbose=False,
                        filter_directories=(self.config.github_dirs, GithubRepositoryReader.FilterType.INCLUDE),
                        filter_file_extensions=(self.config.github_extensions, GithubRepositoryReader.FilterType.INCLUDE)
            ).load_data(branch=config.github_branch)

            pickle.dump(knowledge, config.vector_file.open("wb"))
            print(f"-- Generated new knowledge file {self.config.vector_file}")

            self.knowledge = knowledge

        self.index = GPTVectorStoreIndex.from_documents(self.knowledge)
        self.query_engine = self.index.as_query_engine()

    def answer_question(self, question: str) -> str:
        return self.query_engine.query(question).response.strip()
