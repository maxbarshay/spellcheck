# spellchecker
Implementation of a fast spellchecker in Python based on the Fast and Accurate Spellchecker Medium article that can be found here: 

## Environment Setup
```bash
conda create -n spellchecker python=3.10.11
conda activate spellchecker
poetry install
```

## Simple Test
See the file `tests/test_spellchecker.py` for a simple test of the spellchecker. You can adjust the text in the test to see how the spellchecker behaves on different inputs. Don't forget to run `python spellcheck/generate_dictionary.py` to generate the dictionary before running the test!

## Unit Tests
To run 30 test corrections of the spellchecker, run the following command:
```bash
pytest tests/pytest_spellchecker.py
``````
