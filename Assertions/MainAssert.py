
class LabelAssertions(object):

    @staticmethod
    def check_binary_labels(original_labels, new_labels):
        assert original_labels.shape == new_labels.shape
        all_labels = zip(original_labels, new_labels)
        for o, n in all_labels:
            if o in {0, 1}:
                assert n == 0
            elif o in {2, 3}:
                assert n == 1
            else:
                raise ValueError("Invalid Original Label Value")
