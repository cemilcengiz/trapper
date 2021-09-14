# TRAPPER (Transformer wRAPPER)

A lightweight framework that aims to make it easier to train transformer based models
on downstream tasks. It wraps the `HuggingFace`'s
`transformers` library to provide the transformer model implementations and training
mechanisms conveniently.

* `allennlp`'s registry mechanism is used to provide dependency injection and enable
  reading the experiment details from training configuration files which are
  typically `json` or `jsonnet` files. Moreover, registrable base classes are
  implemented to abstract away the common operations for data processing and model
  training.

* Auto classes from `transformers` are used to provide polymorphism and make it
  possible to instantiate the actual task-specific classes (e.g. for models and
  tokenizers) from the configuration files dynamically.

## Table of Currently Supported Tasks and Models From Transformers

| model       | question_answering | token_classification |
|-------------|--------------------|----------------------|
| ALBERT      | &#10004;           | &#10004;             |
| DistillBERT | &#10004;           | &#10004;             |
| ELECTRA     | &#10004;           | &#10004;             |
| RoBERTa     | &#10004;           | &#10004;             |

## Usage

WIP

#### Registering classes from custom modules to the library

We support both file based and command line argument based approaches to register the
external modules written by the users.

##### Option 1 - File based

You should list the packages or modules (for stand-alone modules not residing inside
any package) containing the classes to be registered as plugins to a local file
named `.trapper_plugins`. This file must reside in the same directory where you run
the `trapper run` command. Moreover, it is recommended to put the plugins file where
the modules to be registered resides (e.g. the project root) for convenience since
that directory will be added to the `PYTHONPATH`. Otherwise, you need to add the
plugin module/packages to the `PYTHONPATH` manually. Another reminder is that each
listed package must have an `__init__.py` file that imports the modules containing
the custom classes to be registered.

E.g., let's say our project's root directory is `project_root` and the experiment
config file is inside the root with a name `test_experiment.jsonnet`. To run the
experiment, you should run the following commands:

```shell
cd project_root
trapper run test_experiment.jsonnet
```

Below output shows the content of the project_root directory.

```console
ls project_root

  ner
  tests
  datasets
  .trapper_plugins
  test_experiment.jsonnet
```

Additionally, here is the content of the project_root/.trapper_plugins.

```console
cat project_root/.trapper_plugins

  ner.core.models
  ner.data.dataset_readers
```

##### Option 2 - Using the command line argument

You can specify the packages and/or modules you want to be registered using the
--include-package argument. However, note that you need to repeat the argument for
each package/module to be registered.

E.g. the running the following commands is an alternative to `Option-1` to start the
experiment specified in the `test_experiment.jsonnet`.

```console
trapper run test_experiment.jsonnet \
--include-package ner.core.models \
--include-package ner.data.dataset_readers
```

## Contributing

PRs are welcomed as always :)

### Installation

    git clone https://github.com/obss/trapper.git
    cd trapper
    pip install -e .[dev]

### Tests

To tests simply run.

    python tests/run_tests.py

### Code Style

To check code style,

    python tests/run_code_style.py check

To format codebase,

    python tests/run_code_style.py format

## Contributors

- [Cemil Cengiz](https://github.com/cemilcengiz)
- [Devrim Çavuşoğlu](https://github.com/devrimcavusoglu)