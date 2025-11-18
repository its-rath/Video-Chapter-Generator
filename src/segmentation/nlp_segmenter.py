from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from typing import List, Dict, Tuple
import logging
from src.transcription.whisper_asr import TranscriptSegment

logger = logging.getLogger(__name__)

class NLPSegmenter:
    """
    Segment transcript into chapters using NLP embeddings and clustering.
    """

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        min_chapter_duration: int = 60,
        max_chapters: int = 20
    ):
        logger.info(f"Loading embedding model: {embedding_model}")
        self.encoder = SentenceTransformer(embedding_model)
        self.min_chapter_duration = min_chapter_duration
        self.max_chapters = max_chapters

    def generate_embeddings(
        self,
        segments: List[TranscriptSegment]
    ) -> np.ndarray:
        """Generate sentence embeddings for all segments."""
        texts = [seg.text for seg in segments]
        embeddings = self.encoder.encode(texts, show_progress_bar=False)
        logger.info(f"Generated embeddings: {embeddings.shape}")
        return embeddings

    def cluster_segments(
        self,
        embeddings: np.ndarray,
        method: str = "kmeans",
        n_clusters: int = None
    ) -> np.ndarray:
        """
        Cluster embeddings to identify topic boundaries.
        Args:
            embeddings: Segment embeddings
            method: 'kmeans' or 'dbscan'
            n_clusters: Number of clusters (auto if None)
        Returns:
            Cluster labels for each segment
        """
        if n_clusters is None:
            n_clusters = self._determine_optimal_clusters(embeddings)

        if method == "kmeans":
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = clusterer.fit_predict(embeddings)
        elif method == "dbscan":
            clusterer = DBSCAN(eps=0.5, min_samples=3, metric='cosine')
            labels = clusterer.fit_predict(embeddings)
        else:
            raise ValueError(f"Unknown method: {method}")

        logger.info(f"Clustering: {len(set(labels))} clusters found")
        return labels

    def _determine_optimal_clusters(
        self,
        embeddings: np.ndarray
    ) -> int:
        """Use silhouette analysis to find optimal cluster count."""
        max_k = min(self.max_chapters, len(embeddings) // 3)
        best_k = 3
        best_score = -1

        for k in range(3, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)

            if score > best_score:
                best_score = score
                best_k = k

        logger.info(f"Optimal clusters: {best_k} (score: {best_score:.3f})")
        return best_k

    def identify_chapter_boundaries(
        self,
        segments: List[TranscriptSegment],
        labels: np.ndarray
    ) -> List[int]:
        """
        Identify segment indices where topic changes occur.
        Returns:
            List of boundary indices
        """
        boundaries = [0]  # Always start at 0

        for i in range(1, len(labels)):
            # Topic change detected
            if labels[i] != labels[i - 1]:
                # Check minimum duration constraint
                if segments[i].start - segments[boundaries[-1]].start >= self.min_chapter_duration:
                    boundaries.append(i)

        # Merge very short final segment
        if len(boundaries) > 1:
            last_duration = segments[-1].end - segments[boundaries[-1]].start
            if last_duration < self.min_chapter_duration / 2:
                boundaries.pop()

        logger.info(f"Identified {len(boundaries)} chapter boundaries")
        return boundaries

    def extract_topics_nmf(
        self,
        segments: List[TranscriptSegment],
        n_topics: int = 10,
        n_words: int = 3
    ) -> List[str]:
        """
        Extract topics using NMF for chapter naming.
        Returns:
            List of topic keywords for each topic
        """
        texts = [seg.text for seg in segments]

        # TF-IDF vectorization
        tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        tfidf_matrix = tfidf.fit_transform(texts)

        # NMF topic modeling
        nmf = NMF(n_components=n_topics, random_state=42)
        nmf.fit(tfidf_matrix)

        # Extract top words for each topic
        feature_names = tfidf.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(nmf.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            topics.append(" ".join(top_words))

        logger.info(f"Extracted {len(topics)} topics")
        return topics
