"""Custom math utils for langchain function implementation."""
from typing import List, Optional, Tuple, Union

import numpy as np
from scipy.spatial.distance import cdist

from telemedicine.core.thread import multithreading

Matrix = Union[List[List[float]], List[np.ndarray], np.ndarray]


def cosine_similarity(X: Matrix, Y: Matrix) -> np.ndarray:
    """Faster Row-wise cosine similarity between two equal-width matrices."""
    if len(X) == 0 or len(Y) == 0:
        return np.array([])

    X = np.array(X)
    Y = np.array(Y)
    if X.shape[1] != Y.shape[1]:
        raise ValueError(
            f"Number of columns in X and Y must be the same. X has shape {X.shape} "
            f"and Y has shape {Y.shape}."
        )
    similarity = 1 - cdist(X, Y, metric='cosine')
    return similarity


def cosine_similarity_top_k(
    X: Matrix,
    Y: Matrix,
    top_k: Optional[int] = 5,
    score_threshold: Optional[float] = None,
) -> Tuple[List[Tuple[int, int]], List[float]]:
    """Row-wise cosine similarity with optional top-k and score threshold filtering.

    Args:
        X: Matrix.
        Y: Matrix, same width as X.
        top_k: Max number of results to return.
        score_threshold: Minimum cosine similarity of results.

    Returns:
        Tuple of two lists. First contains two-tuples of indices (X_idx, Y_idx),
            second contains corresponding cosine similarities.
    """
    if len(X) == 0 or len(Y) == 0:
        return [], []
    score_array = cosine_similarity(X, Y)
    score_threshold = score_threshold or -1.0
    score_array[score_array < score_threshold] = 0
    top_k = min(top_k or len(score_array), np.count_nonzero(score_array))
    top_k_idxs = np.argpartition(score_array, -top_k, axis=None)[-top_k:]
    top_k_idxs = top_k_idxs[np.argsort(score_array.ravel()[top_k_idxs])][::-1]
    ret_idxs = np.unravel_index(top_k_idxs, score_array.shape)
    scores = score_array.ravel()[top_k_idxs].tolist()
    return list(zip(*ret_idxs)), scores  # type: ignore

def maximal_marginal_relevance(
    query_embedding: np.ndarray,
    embedding_list: list,
    lambda_mult: float = 0.5,
    k: int = 4,
) -> List[int]:
    """Calculate maximal marginal relevance."""
    try:
        if min(k, len(embedding_list)) <= 0:
            return []
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        similarity_to_query = cosine_similarity(query_embedding, embedding_list)[0]
        most_similar = int(np.argmax(similarity_to_query))
        idxs = [most_similar]
        selected = np.array([embedding_list[most_similar]])

        def compute_equation_score(i, query_score):
            if i in idxs:
                return -np.inf, i
            redundant_score = max(similarity_to_selected[i])
            equation_score = (
                lambda_mult * query_score - (1 - lambda_mult) * redundant_score
            )
            return equation_score, i

        while len(idxs) < min(k, len(embedding_list)):
            best_score = -np.inf
            idx_to_add = -1
            similarity_to_selected = cosine_similarity(embedding_list, selected)

            results = multithreading(
                compute_equation_score, 
                range(len(embedding_list)), 
                similarity_to_query
            )
            
            for score, i in results:
                if score > best_score:
                    best_score = score
                    idx_to_add = i

            idxs.append(idx_to_add)
            selected = np.append(selected, [embedding_list[idx_to_add]], axis=0)
        return idxs
    except Exception as e:
        print(f"Error in maximal_marginal_relevance: {str(e)}")
        raise Exception(f"Error in maximal_marginal_relevance: {str(e)}") from e
    
def maximal_marginal_relevance_with_formatted_tag(
    query_embedding: np.ndarray,
    embedding_list: list,
    formatted_tag_embedding_list: list,
    lambda_mult: float = 0.5,
    k: int = 4,
) -> List[int]:
    """Calculate maximal marginal relevance."""
    try:
        if min(k, len(embedding_list)) <= 0:
            return []
        if min(k, len(formatted_tag_embedding_list)) <= 0:
            return []
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        def calculate_similarity_to_query(x):
            return cosine_similarity(query_embedding, x)[0]
        similarity_to_query = multithreading(
            calculate_similarity_to_query, [embedding_list, formatted_tag_embedding_list]
        )
        similarity_to_query = (2*similarity_to_query[0] + similarity_to_query[1])/3
        most_similar = int(np.argmax(similarity_to_query))
        idxs = [most_similar]
        selected = np.array([embedding_list[most_similar]])

        def compute_equation_score(i, query_score):
            if i in idxs:
                return -np.inf, i
            redundant_score = max(similarity_to_selected[i])
            equation_score = (
                lambda_mult * query_score - (1 - lambda_mult) * redundant_score
            )
            return equation_score, i

        while len(idxs) < min(k, len(embedding_list)):
            best_score = -np.inf
            idx_to_add = -1
            similarity_to_selected = 2*cosine_similarity(embedding_list, selected)
            similarity_to_selected += cosine_similarity(formatted_tag_embedding_list, selected)
            similarity_to_selected /= 3

            results = multithreading(
                compute_equation_score, 
                range(len(embedding_list)), 
                similarity_to_query
            )
            
            for score, i in results:
                if score > best_score:
                    best_score = score
                    idx_to_add = i

            idxs.append(idx_to_add)
            selected = np.append(selected, [embedding_list[idx_to_add]], axis=0)
        return idxs
    except Exception as e:
        print(f"Error in maximal_marginal_relevance: {str(e)}")
        raise Exception(f"Error in maximal_marginal_relevance: {str(e)}") from e
    
def average_between_percentiles(data: List[float], 
                                lower_percentile: float = 0.2, 
                                upper_percentile: float = 0.8) -> float:
    """
    Calculate the average of data points between specified percentiles.

    Args:
        data (List[float]): The list of data points.
        lower_percentile (float, optional): The lower percentile. Defaults to 0.2.
        upper_percentile (float, optional): The upper percentile. Defaults to 0.8.

    Returns:
        float: The average of the data points between the specified percentiles.
    """
    sorted_data = sorted(data)
    
    lower_index = int(lower_percentile * len(sorted_data))
    upper_index = int(upper_percentile * len(sorted_data))
    
    filtered_data = sorted_data[lower_index:upper_index]
    
    if len(filtered_data) == 0:
        return 0
    
    average = sum(filtered_data) / len(filtered_data)
    return average


