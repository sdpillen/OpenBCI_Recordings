import sys
sys.path.append('..')
from Analysis import Features
import unittest
import numpy as np
import time
import random
from Analysis import Statistics


class TestDiscrete(unittest.TestCase):

    def test_assertions(self):
        lst = []
        for i in range(1, 10):
            lst.append([x + random.randint(1, 10) for x in range(i, i + 6)])

        feats = np.asarray(lst)
        # print "Features ", feats.shape, '\n', feats
        # print "Desc Feats"
        print Features.DiscretizeFeatures.discretize_features_uniform(feats, num_bins=3)
        time.sleep(1)

    def test_feature_trim(self):
        lst = []
        for i in range(1, 10):
            lst.append([x + random.randint(1, 10) for x in range(i, i + 6)])

        feats = np.asarray(lst)
        # print "Features ", feats.shape, '\n', feats
        desc_feats = Features.DiscretizeFeatures.discretize_features_uniform(feats, num_bins=3)
        # print "Original desc feats\n", desc_feats
        labels = np.asarray([random.choice([0, 1]) for _ in range(desc_feats.shape[0])])
        # print "Labs", labels.shape, desc_feats.shape
        mi_for_each_feat = Statistics.MutualInfo.calculate_mutual_info(desc_feats, labels=labels)

        desc_feats = Features.Trim.trim_on_MI(features=desc_feats, mi_for_each_feat=mi_for_each_feat, num_to_save=2)
        # print "MI for each feat\n", mi_for_each_feat
        # print "Desk Feat\n", descritzed_feat
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()
