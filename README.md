# Reproduction for TDC23

Written by `antiquality`

Date: 12/13/2023

>  Reproduction of `antiquality`'s work for the Test Phase of TDC23.

This document, authored by `antiquality`, details the process for reproducing the submission `test_case.json`, intended to run for the **Most Compute-Efficient special award** for the Red Teaming Track Large Model Subtrack in TDC23.



## Method Overview

Jailbreak the LLaMa2-13B model using mid-resource languages.

1. **Language Selection:** Determine the 24 mid-resource languages supported by Azure Translation API, which are hard-coded in the Python code.
2. **Translation:** Utilize the Azure API to translate `behaviors.json` and generate `test_cases.json` submission.  The output format for each prompt follows `"Answer in xx language: yy."`, where `xx` is the target language, and `yy` is the translated output from the Azure API.
3. **Detokenization:** Count the number of tokens of each prompt and reduce the length if necessary, in order to comply with the `length <= 256` limit.

As is shown above, this method relies solely on API calls and consumes network bandwich, **without requiring any GPU resources**!



## Folder Structure

```
TDC23aq
├─ behaviors.json
├─ test_cases.json
├─ tokenizer.model
├─ trans_from_raw_behavior.py
├─ requirements.txt
└─ README.md
```

Description of each file:

`behaviors.json` : Test Phase data given by [tdc2023-starter-kit](https://github.com/centerforaisafety/tdc2023-starter-kit/blob/main/red_teaming/data/test/behaviors.json).

`test_cases.json` : File generated for reproduction.

`tokenizer.model`: Token counter for LLaMa-family models from [Llama Token Counter, Hugging Face Space](https://huggingface.co/spaces/Xanthius/llama-token-counter).

`trans_from_raw_behavior.py`: Main script for reproduction.

`requirements.txt`: Python libraries for reproduction.

`README.md`: Exactly the file you are reading now, explaining `antiquality`'s work.



## Environment Setup

First, create a conda environment (or not, which depends on you).

```bash
conda create --name TDC23aq python=3.9
```

Then run the command in the `TDC23aq` directory:

```bash
pip install -r requirements.txt
```



## Reproduction

Now you only need to run

```bash
python trans_from_raw_behavior.py
```

to reproduce `antiquality`'s work in the Test Phase of the Red Teaming Track Large Model Subtrack in TDC23!

The process takes approximately $2600$ seconds to complete the $2500$ translations, based on tests conducted on the server used by author.

Note that the method in Development Phase is a little bit different, which adopts `pythia-12b-sft-v8-7k-steps` to make tautological transformation and utilize `GPT-3.5` to supervise the output quality, then translates the prompts into low-/mid-resource language.



## Note for Azure API

In the version of submission to TDC23 committee, `antiquality`'s personal API key of Azure is provided in `trans_from_raw_behavior.py`, **please ensure it remains confidential**.

For the GitHub release, this API key has been omitted and please replace it on your own!