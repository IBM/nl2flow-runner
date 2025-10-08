# NL2FLOW-RUNNER

NL2FLOW-RUNNER is an experiment runner designed to evaluate the planning capabilities of large language models (LLMs) in the context of NL2FLOW (https://github.com/IBM/nl2flow).  NL2FLOW is a PDDL compiler that translates natural language goals into formal planning problems suitable for automated planning systems.

This tool is a companion to the research paper: "Scaling LLM Planning: NL2FLOW for Parametric Problem Generation and Rigorous Evaluation" (https://arxiv.org/pdf/2507.02253).  It implements the experimental setup described in the paper and allows for reproducibility and further research.

## Citation

```
@article{kang2025scaling,
  title={Scaling LLM Planning: NL2FLOW for Parametric Problem Generation and Rigorous Evaluation},
  author={Kang, Jungkoo},
  journal={arXiv preprint arXiv:2507.02253},
  year={2025}
}
```

## Installation

```bash
pip install -e .
```

## Build Package

```bash
python -m pip install --upgrade build
python -m build
```

### VAL

Clone VAL repository.

```bash
git clone git@github.com:KCL-Planning/VAL.git
cd VAL
```

- On linux,

```bash
./scripts/linux/build_linux64.sh all release
```

- on MacOS (Make sure to install dependencies noted at `KCL-Planning/VAL.git`)

```bash
cmake .
make
```

## Install NL2FLOW-Runner Package

```bash
pip install <PATH_FOR_WHL>
```

```bash
pip install /Users/jungkookang/Documents/projects/NL2FLOW-Runner/dist/nl2flow_runner-0.0.0-py3-none-any.whl
```


## Command Line Interface (CLI)

`NL2Flow Runner` provides a user-friendly command-line interface (CLI) for generating planning data, retrieving plans from language model services, and assessing these plans. Before using the CLI, ensure that you have a running MongoDB. To ensure the CLI is correctly installed, execute the given command to access the help menu. You should expect to see output resembling the following:

```bash
nl2flow -h
```

```
usage: nl2flow [-h] [-m {generator,collector,evaluator,manager}] [-tm {planning,translation}] [-od OUTPUT_DIRECTORY_PATH] [-ak API_KEY] [-mt MAX_TOKENS] [-nt MIN_NEW_TOKENS]
               [-lmt LANGUAGE_MODEL_TEMPERATURE] [-tl TIME_LIMIT] [-nr NUM_RETRIEVALS] [-gf GENERATOR_CONFIG_FILE_PATH] [-sd RANDOM_SEED] [-tp TRAINING_PROPORTION] [-vp VALIDATION_PROPORTION]
               [-mid [MODEL_ID ...]] [-psf PLANNING_SOURCE_FILE_PATH] [-sppd {long,short}] [-mofp MODEL_OUTPUT_FILE_PATH] [-mi MODEL_IDENTIFIER]
               [-cn {llm_nl2flow,llm_concise_nl2flow,llm_json_nl2flow,validation_nl2flow,validation_concise_nl2flow,validation_json_nl2flow,nl2flowfailed,dscp2plan,dscp2planfailed,dscp2pddl,dscp2pddlfailed,pddl2plan,pddl2planfailed,pddlsymplan,pddlsymplanfailed}]
               [-mtm {delete,retrieve}]

Conversational AI Benchmark Tool

options:
  -h, --help            show this help message and exit
  -m {generator,collector,evaluator,manager}, --mode {generator,collector,evaluator,manager}
                        NL2FLOW Runner tool mode
  -tm {planning,translation}, --task_mode {planning,translation}
                        NL2FLOW Runner task mode
  -od OUTPUT_DIRECTORY_PATH, --output_directory_path OUTPUT_DIRECTORY_PATH
                        Absolute path for an output directory
  -ak API_KEY, --api_key API_KEY
                        API key
  -mt MAX_TOKENS, --max_tokens MAX_TOKENS
                        The maximum number of tokens to retrieve from a model
  -nt MIN_NEW_TOKENS, --min_new_tokens MIN_NEW_TOKENS
                        The minimum number of new tokens to retrieve from a model
  -lmt LANGUAGE_MODEL_TEMPERATURE, --language_model_temperature LANGUAGE_MODEL_TEMPERATURE
                        Language model temperature
  -tl TIME_LIMIT, --time_limit TIME_LIMIT
                        Time limit in second
  -nr NUM_RETRIEVALS, --num_retrievals NUM_RETRIEVALS
                        The number of response retrievals per sample
  -gf GENERATOR_CONFIG_FILE_PATH, --generator_config_file_path GENERATOR_CONFIG_FILE_PATH
                        Absolute path for the json file containing a generator configuration
  -sd RANDOM_SEED, --random_seed RANDOM_SEED
                        Random seed for generating data
  -tp TRAINING_PROPORTION, --training_proportion TRAINING_PROPORTION
                        The proportion of data for training
  -vp VALIDATION_PROPORTION, --validation_proportion VALIDATION_PROPORTION
                        The proportion of data for validation
  -mid [MODEL_ID ...], --model_id [MODEL_ID ...]
                        Model IDs. Currently, they are model ids for LLM_SERVICE
  -psf PLANNING_SOURCE_FILE_PATH, --planning_source_file_path PLANNING_SOURCE_FILE_PATH
                        Absolute path for a planning source file
  -sppd {long,short}, --style_planning_problem_description {long,short}
                        Style of planning problem description
  -mofp MODEL_OUTPUT_FILE_PATH, --model_output_file_path MODEL_OUTPUT_FILE_PATH
                        Absolute path for an output file from a model
  -mi MODEL_IDENTIFIER, --model_identifier MODEL_IDENTIFIER
                        Model identifier
  -cn {llm_nl2flow,llm_concise_nl2flow,llm_json_nl2flow,validation_nl2flow,validation_concise_nl2flow,validation_json_nl2flow,nl2flowfailed,dscp2plan,dscp2planfailed,dscp2pddl,dscp2pddlfailed,pddl2plan,pddl2planfailed,pddlsymplan,pddlsymplanfailed}, --collection_name {llm_nl2flow,llm_concise_nl2flow,llm_json_nl2flow,validation_nl2flow,validation_concise_nl2flow,validation_json_nl2flow,nl2flowfailed,dscp2plan,dscp2planfailed,dscp2pddl,dscp2pddlfailed,pddl2plan,pddl2planfailed,pddlsymplan,pddlsymplanfailed}
                        Collection name at MongoDB
  -mtm {delete,retrieve}, --manager_task_mode {delete,retrieve}
                        Database Manager task mode
```

### Generator

NL2FLOW's Planning Data Generator can be utilized at the command-line interface (CLI). It requires the absolute path to a JSON file containing a generator configuration as input. Here is an example of how such a configuration may look:

```json
{
  "num_agents": [
    2
  ],
  "num_var": [
    4
  ],
  "num_input_parameters": [
    1
  ],
  "num_samples": [
    2
  ],
  "num_goal_agents": [
    1
  ],
  "proportion_coupled_agents": [
    0.0
  ],
  "proportion_slot_fillable_variables": [
    0.0,
    0.5,
    1.0
  ],
  "proportion_mappable_variables": [
    0.0,
    0.5,
    1.0
  ],
  "num_var_types": [
    0
  ],
  "slot_filler_option": [
    null
  ],
  "name_generator": [
    "NUMBER"
  ],
  "error_message": [
    null
  ]
}
```

To obtain plans from model services, execute the command shown below. A sample command is also provided:

```bash
nl2flow -m generator  -gf <ABSOLTE_FILE_PATH_FOR_GENERATOR_CONFIGURATION> -sd <RANDOM_SEED> -od <ABSOLTE_PATH_FOR_OUTPUT_DIRECTORY> -tp <PROPORTION_OF_TRAINING_DATA> -vp <PROPORTION_OF_VALIDATION_DATA>
```

For instance:

```bash
nl2flow -m generator  -gf /Users/jungkookang/Documents/projects/nl2flow_runner/ai_profiling/data/data_generation/generator_input.json -sd 202406201127 -od /Users/jungkookang/Downloads/nl2flow/generator -tp 0.9 -vp 0.05
```

```
Generator starts.
Saving the dataset (1/1 shards): 100%|██████████████████████████████████████████████████████████████| 26/26 [00:00<00:00, 2796.63 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 339.32 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 440.53 examples/s]
Saving the dataset (1/1 shards): 100%|██████████████████████████████████████████████████████████████| 26/26 [00:00<00:00, 4326.25 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 187.97 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 293.73 examples/s]
Saving the dataset (1/1 shards): 100%|██████████████████████████████████████████████████████████████| 26/26 [00:00<00:00, 4143.62 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 170.19 examples/s]
Saving the dataset (1/1 shards): 100%|█████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 298.90 examples/s]

Generated files are
('/Users/jungkookang/Downloads/nl2flow/generator/planning_source_setting_08_08_2024_08_15_02.json',
 '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_no_split_08_08_2024_08_15_05.jsonl',
 '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_training_08_08_2024_08_15_05.jsonl',
 '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_validation_08_08_2024_08_15_05.jsonl',
 '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_test_08_08_2024_08_15_05.jsonl',
 ('/Users/jungkookang/Downloads/nl2flow/generator/planning_source_train_llm_planning_VERBOSE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_train_llm_planning_CONCISE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_train_LLM_SERVICE_translation_VERBOSE_08_08_2024_08_15_05.jsonl'),
 ('/Users/jungkookang/Downloads/nl2flow/generator/planning_source_validation_llm_planning_VERBOSE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_validation_llm_planning_CONCISE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_validation_LLM_SERVICE_translation_VERBOSE_08_08_2024_08_15_05.jsonl'),
 ('/Users/jungkookang/Downloads/nl2flow/generator/planning_source_test_llm_planning_VERBOSE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_test_llm_planning_CONCISE_08_08_2024_08_15_05.jsonl',
  '/Users/jungkookang/Downloads/nl2flow/generator/planning_source_test_LLM_SERVICE_translation_VERBOSE_08_08_2024_08_15_05.jsonl'))

Generator ends.
```

### Collector

The Collector performs multiple requests to a model service to retrieve plans or translates a planning problem into a structured format (JSON). At the command-line interface (CLI), the Collector requires several inputs. <TASK_NAME> can be set to `planning` or `translation`, depending on the task at hand. <DESCRIPTION_STYLE> influences the Collector only when the task is planning; its value can be either `long` or `short`, affecting the style of the planning problem description. <API_KEY> represents an API Key necessary for using a model service, while <MODEL_ID> specifies the IDs of models available at that service. Multiple model IDs can be provided to gather responses from all specified models simultaneously. After retrieving the responses, they are automatically evaluated.

The following command demonstrates the use of the Collector:

```bash
nl2flow -m collector -tm <TASK_NAME> -sppd <DESCRIPTION_STYLE> -psf <ABSOLTE_PATH_FOR_PLANNING_DATA_FILE> -od <ABSOLTE_PATH_FOR_OUTPUT_DIRECTORY> -ak <API_KEY> -mid <MODEL_ID>
```

For example:

```bash
nl2flow -m collector -tm planning -sppd long -tl 480 -psf /Users/jungkookang/Downloads/nl2flow/output/generator -od /Users/jungkookang/Downloads/nl2flow/output -ak $LLM_SERVICE_API_KEY  -mid Qwen/Qwen2.5-72B-Instruct mistralai/mixtral-8x22B-instruct-v0.1 deepseek-ai/DeepSeek-V3 ibm-granite/granite-3.3-8b-instruct meta-llama/llama-3-3-70b-instruct

nl2flow -m collector -tm translation -sppd long -tl 480 -psf /Users/jungkookang/Downloads/nl2flow/output/generator -od /Users/jungkookang/Downloads/nl2flow/output -ak $LLM_SERVICE_API_KEY  -mid Qwen/Qwen2.5-72B-Instruct
```

```
Collector starts.
Planning data length: 29

'/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_llm_response_08_08_2024_08_26_30.jsonl'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'
Error generating step predicate: 'b'

('/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_validation_08_08_2024_08_26_47.jsonl',
 '/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_validation_summary_08_08_2024_08_26_47.json',
 '/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_validation_histogram_optimal_08_08_2024_08_26_47.json',
 '/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_validation_histogram_sound_08_08_2024_08_26_47.json',
 '/Users/jungkookang/Downloads/nl2flow/collector/planning_long_plan_validation_histogram_valid_08_08_2024_08_26_47.json')

Collector ends.
```

### Evaluator

```bash
nl2flow -m evaluator -tm planning -mofp /Users/jungkookang/Downloads/nl2flow_test/output -od /Users/jungkookang/Downloads/nl2flow_test/output
nl2flow -m evaluator -tm planning -mofp /Users/jungkookang/Downloads/nl2flow/output/llm_plan_collector -od /Users/jungkookang/Downloads/nl2flow/output/llm_plan_evaluator -cf /Users/jungkookang/Downloads/nl2flow/cache -vfp /Users/jungkookang/Documents/projects/VAL/bin/Validate

nl2flow -m evaluator -tm translation -mofp /Users/jungkookang/Downloads/nl2flow_test/output -od /Users/jungkookang/Downloads/nl2flow_test/output

nl2flow -m evaluator -tm translation -mofp /Users/jungkookang/Downloads/nl2flow/output/llm_translation_collector -od /Users/jungkookang/Downloads/nl2flow/output
```

## Installation for Development

```bash
pip install -e ".[test]"
pre-commit install
```

### Environmental variable

To set up the API KEY for LLM_SERVICE, add it to your environment variables by modifying the file `~/.bash_profile` on MacOS systems.

```bash
export LLM_SERVICE_APIKEY="<YOUR_LLM_SERVICE_API_KEY>"
```

Alternatively, replace `get_environmental_variable_value("LLM_SERVICE_APIKEY")` at the input sections in pipeline scripts with your `API KEY` for LLM_SERVICE.
