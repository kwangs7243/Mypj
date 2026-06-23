# Processed Data

Preprocessed intermediate datasets live here when a workflow needs a separate processed file.

The current NSMC workflow writes converted train/test files directly to `data/splits/`, because NSMC already provides fixed train/test source files.

Expected future examples:

```text
nsmc_morph_train.csv
nsmc_morph_test.csv
nsmc_sentencepiece_train.csv
nsmc_sentencepiece_test.csv
```

Large processed CSV files are ignored by Git.
