"""
.. _example_interpreting_gap_encoder:

==========================================
Feature interpretation with the GapEncoder
==========================================

In this notebook, we will explore the output and inner workings of the
|GapEncoder|, one of the encoders provided by skrub.


.. |GapEncoder| replace::
     :class:`~skrub.GapEncoder`

.. |SimilarityEncoder| replace::
     :class:`~skrub.SimilarityEncoder`
"""

###############################################################################
# The |GapEncoder| is a better encoder than the |SimilarityEncoder| in the
# sense that it is more scalable and interpretable,
# which we will demonstrate now.
#
# First, let's retrieve the dataset:

from skrub.datasets import fetch_employee_salaries

dataset = fetch_employee_salaries()

# Alias X and y
X, y = dataset.X, dataset.y

dataset.description

###############################################################################
# And carry out some basic preprocessing

# Overload `employee_position_title` with 'underfilled_job_title',
# as the latter gives more accurate job titles when specified
X["employee_position_title"] = X["underfilled_job_title"].fillna(
    X["employee_position_title"]
)
X.drop(labels=["underfilled_job_title"], axis="columns", inplace=True)

X

###############################################################################
# Let's also get the dirty column we want to encode

X_dirty = X[["employee_position_title"]]
X_dirty.head()

###############################################################################
# Encoding dirty job titles
# -------------------------
#
# Then, we'll create an instance of the |GapEncoder| with 10 components:

from skrub import GapEncoder

enc = GapEncoder(n_components=10, random_state=42)

###############################################################################
# Finally, we'll fit the model on the dirty categorical data and transform it
# in order to obtain encoded vectors of size 10:

X_enc = enc.fit_transform(X_dirty)
X_enc.shape

###############################################################################
# Interpreting encoded vectors
# ----------------------------
#
# The |GapEncoder| can be understood as a continuous encoding
# on a set of latent topics estimated from the data. The latent topics
# are built by capturing combinations of substrings that frequently
# co-occur, and encoded vectors correspond to their activations.
# To interpret these latent topics, we select for each of them a few labels
# from the input data with the highest activations.
# In the example below we select 3 labels to summarize each topic.

topic_labels = enc.get_feature_names_out(n_labels=3)
for k, labels in enumerate(topic_labels):
    print(f"Topic n°{k}: {labels}")

###############################################################################
# As expected, topics capture labels that frequently co-occur. For instance,
# the labels "firefighter", "rescuer", "rescue" appear together in
# "Firefighter/Rescuer III", or "Fire/Rescue Lieutenant".
#
# This enables us to understand the encoding of different samples

import matplotlib.pyplot as plt

encoded_labels = enc.transform(X_dirty[:20])
plt.figure(figsize=(8, 10))
plt.imshow(encoded_labels)
plt.xlabel("Latent topics", size=12)
plt.xticks(range(0, 10), labels=topic_labels, rotation=50, ha="right")
plt.ylabel("Data entries", size=12)
plt.yticks(range(0, 20), labels=X_dirty[:20].to_numpy().flatten())
plt.colorbar().set_label(label="Topic activations", size=12)
plt.tight_layout()
plt.show()

###############################################################################
# As we can see, each dirty category encodes on a small number of topics,
# These can thus be reliably used to summarize each topic, which are in
# effect latent categories captured from the data.
