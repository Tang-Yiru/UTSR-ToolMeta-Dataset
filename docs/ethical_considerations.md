# Ethical Considerations

UTSR-ToolMeta is intended for controlled academic research on model-visible tool declarations and LLM-Agent tool-use behavior.

## Potential Risks

The dataset can support research on perturbing tool metadata. Such techniques may reveal vulnerabilities in tool selection, planning, or parameter generation. They should not be used to attack real tool registries, production agent systems, or third-party services.

## Recommended Use

Researchers should:

- run experiments in controlled environments;
- avoid deploying generated perturbations to real tool ecosystems;
- preserve source metadata and attribution;
- report vulnerabilities responsibly when real systems are involved;
- avoid using the dataset to infer private system behavior.

## Privacy

The dataset is constructed from public or research-oriented tool metadata and does not include private user data, credentials, or runtime execution traces.

## Scope

The dataset describes static tool declarations. It does not certify the safety, correctness, or behavior of any underlying tool implementation.

