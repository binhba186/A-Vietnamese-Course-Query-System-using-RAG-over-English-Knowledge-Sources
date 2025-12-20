
from copy import deepcopy
from typing import List, Optional

import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

from ..utils.config_utils import BaseConfig
from ..utils.logging_utils import get_logger
from .base import BaseEmbeddingModel, EmbeddingConfig

logger = get_logger(__name__)

def mean_pooling(token_embeddings: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
    return sum_embeddings / sum_mask

class HFE5EmbeddingModel(BaseEmbeddingModel):
    """HuggingFace E5 (multilingual) embedding model.

    Notes:
      - E5 expects prefix tokens:
        * queries:   'query: <text>'
        * passages:  'passage: <text>'
      - In this codebase, query encoding calls usually pass `instruction=...`.
        We treat any non-empty instruction as a query. If you need to force
        passage/query behavior, pass `as_query=True/False`.
    """

    def __init__(self, global_config: Optional[BaseConfig] = None, embedding_model_name: Optional[str] = None) -> None:
        super().__init__(global_config=global_config)

        if embedding_model_name is not None:
            self.embedding_model_name = embedding_model_name
            logger.debug(f"Overriding {self.__class__.__name__}'s embedding_model_name with: {self.embedding_model_name}")

        self._init_embedding_config()

        logger.debug(f"Initializing {self.__class__.__name__}'s embedding model with params: {self.embedding_config.model_init_params}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.embedding_model_name)
        self.embedding_model = AutoModel.from_pretrained(**self.embedding_config.model_init_params)
        self.embedding_model.eval()
        self.embedding_dim = getattr(self.embedding_model.config, 'hidden_size', None) or self.embedding_model.get_input_embeddings().embedding_dim

    def _init_embedding_config(self) -> None:
        config_dict = {
            "embedding_model_name": self.embedding_model_name,
            "norm": self.global_config.embedding_return_as_normalized,
            "model_init_params": {
                "pretrained_model_name_or_path": self.embedding_model_name,
                "trust_remote_code": True,
                "device_map": "auto",
            },
            "encode_params": {
                "max_length": self.global_config.embedding_max_seq_len,
                "instruction": "",
                "batch_size": self.global_config.embedding_batch_size,
            }
        }
        self.embedding_config = EmbeddingConfig.from_dict(config_dict)

    def _add_prefix(self, texts: List[str], as_query: bool) -> List[str]:
        prefix = "query: " if as_query else "passage: "
        return [prefix + t for t in texts]

    def encode(self, texts: List[str], *, as_query: bool, max_length: int) -> torch.Tensor:
        # --- Clamp max_length to what the model actually supports ---
        # XLM-R / RoBERTa-style models typically support 512 (+ special tokens → buffer 514)
        model_limit = getattr(self.embedding_model.config, "max_position_embeddings", 512)
        tok_limit = getattr(self.tokenizer, "model_max_length", 512)

        # protect against weird values like very large ints
        safe_limit = 512
        max_length = int(max_length) if max_length is not None else safe_limit
        max_length = min(max_length, int(model_limit), int(tok_limit), safe_limit)

        with torch.no_grad():
            inputs = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            ).to(self.embedding_model.device)

            outputs = self.embedding_model(**inputs)
            embeddings = mean_pooling(outputs[0], inputs["attention_mask"])

        return embeddings

    def batch_encode(self, texts: List[str], **kwargs):
        if isinstance(texts, str):
            texts = [texts]

        params = deepcopy(self.embedding_config.encode_params)
        if kwargs:
            params.update(kwargs)

        # Decide query vs passage
        as_query = bool(params.get('as_query', False))
        instruction = params.get('instruction', '')
        if not as_query:
            # In this repo, query encoding passes a non-empty instruction string.
            as_query = bool(instruction)

        max_length = int(params.get('max_length', self.global_config.embedding_max_seq_len))
        batch_size = int(params.get('batch_size', 16))

        # Apply E5 prefix
        texts_prefixed = self._add_prefix(texts, as_query=as_query)

        logger.debug(f"Calling {self.__class__.__name__} as_query={as_query} batch_size={batch_size} max_length={max_length}")

        results = []
        with tqdm(total=len(texts_prefixed), desc="Batch Encoding", disable=(len(texts_prefixed) < 64)) as pbar:
            for i in range(0, len(texts_prefixed), batch_size):
                batch = texts_prefixed[i:i + batch_size]
                results.append(self.encode(batch, as_query=as_query, max_length=max_length))
                pbar.update(len(batch))

        results = torch.cat(results, dim=0)

        if isinstance(results, torch.Tensor):
            results = results.cpu().numpy()

        if self.embedding_config.norm:
            norms = np.linalg.norm(results, axis=1, keepdims=True)
            norms = np.clip(norms, 1e-12, None)
            results = results / norms

        return results
