def gender_feature(name):
   return {'first_letter': name[0],
           'last_letter': name[-1],
           'mid_letter': name[len(name) // 2]}
   # 提取姓名中的首字母、中位字母、末尾字母为特征


import nltk
import random
from nltk.corpus import names

# 获取名字-性别的数据列表
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]
names_all = male_names + female_names
random.shuffle(names_all)

# 生成特征集
feature_set = [(gender_feature(n), g) for (n, g) in names_all]

# 拆分为训练集和测试集
train_set_size = int(len(feature_set) * 0.7)
train_set = feature_set[:train_set_size]
test_set = feature_set[train_set_size:]

classifier = nltk.NaiveBayesClassifier.train(train_set)
for name in ['Ann','Sherlock','Cecilia']:
   print('{}:\t{}'.format(name,classifier.classify(gender_feature(name))))
