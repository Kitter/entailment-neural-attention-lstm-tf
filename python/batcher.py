import numpy as np
import copy

class Batcher(object):
    def __init__(self, word2vec):
        self._premises = []
        self._hypothesis = []
        self._targets = []
        self.word2vec = word2vec
        self.embedding_dim = len(self.word2vec["beer"])

    def batch_generator(self, dataset, num_epochs, batch_size, sequence_length):
        ids = range(len(dataset["targets"]))
        for epoch in range(num_epochs):
            permutation = np.random.permutation(ids)
            for i, idx in enumerate(permutation):
                self._premises.append(self.preprocess(sequence=dataset["premises"][idx], sequence_length=sequence_length))
                self._hypothesis.append(self.preprocess(sequence=dataset["hypothesis"][idx], sequence_length=sequence_length))
                self._targets.append(dataset["targets"][idx])
                if len(self._targets) == batch_size or (i == (len(permutation) - 1) and epoch == (num_epochs - 1)):
                    batch = {
                                "premises": self._premises,
                                "hypothesis": self._hypothesis,
                                "targets": self._targets,
                            }

                    self._premises = []
                    self._hypothesis = []
                    self._targets = []
                    yield batch

    def preprocess(self, sequence, sequence_length):
        p_seq = copy.deepcopy(sequence)
        preprocessed = []
        diff_size = len(p_seq) - sequence_length
        if diff_size  > 0:
            start_index = np.random.randint(diff_size + 1)
            p_seq = p_seq[start_index: (start_index + sequence_length)]
        for word in p_seq[:sequence_length]:
            try:
                embedding = self.word2vec[word]
            except:
                embedding = (2 * np.random.rand(self.embedding_dim) - 1) / 20
            finally:
                preprocessed.append(embedding)

        for i in range(sequence_length - len(p_seq)):
            preprocessed.append(np.zeros(len(preprocessed[0])))
        return preprocessed
