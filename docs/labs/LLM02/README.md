# LLM02 — Sensitive Information Disclosure

## 1. Objective

Investigate whether user-controlled prompts can extract sensitive information placed in an LLM's application context, implement an architectural mitigation, and verify the change through retesting and an automated regression test.

**Environment:** Local AI-SecLab lab  
**Model:** Gemma 3 4B via Ollama  
**Application:** FastAPI  
**Secret:** `AI-SECLAB-DEMO-SECRET-2026` (synthetic lab value only)

## 2. Vulnerability Overview

The initial implementation embedded a simulated confidential token directly into the context sent to the LLM.

The application instructed the model not to reveal the token, but the token remained present in the model's input context.

This created an information-disclosure risk: user-controlled prompts could attempt to persuade the model to reproduce confidential information.

## 3. Attack Evidence

Three extraction strategies were tested against the original implementation.

| Test | Technique | Observed result |
|---|---|---|
| 01 | Prompt override | Token disclosed |
| 02 | Direct secret request | Request refused |
| 03 | Verbatim extraction | Token disclosed |

Evidence screenshots are stored in the `evidence/` directory.

- `evidence/01-prompt-override-disclosure.png`
- `evidence/02-direct-request-blocked.png`
- `evidence/03-verbatim-extraction-disclosure.png`

### Finding

A refusal on one request did not guarantee that other extraction attempts would fail. The model disclosed the synthetic token through two of the three tested approaches.

## 4. Root Cause

The confidential value was unnecessarily included in the prompt supplied to the LLM.

The original data flow was:

```text
Application secret
       |
       v
System context containing secret
       |
       v
LLM receives secret
       |
       v
User-controlled prompt
       |
       v
Potential disclosure in response
```

The instruction not to disclose the token was a model-level instruction, not an enforceable access-control boundary.

## 5. Mitigation Implemented

The application was changed so that the simulated secret remains in the application code but is no longer interpolated into `SYSTEM_CONTEXT`.

The context now contains general assistant instructions without the confidential token.

The updated data flow is:

```text
Application secret ----------------> Remains application-side
                                           |
                                           X
                                    Not added to LLM prompt

User prompt + non-sensitive context
                 |
                 v
                LLM
                 |
                 v
              Response
```

### Before

The LLM received both the confidential token and the user's request.

### After

The LLM receives the user's request and non-sensitive application instructions, but not the simulated secret.

### Security Principle

**Minimize sensitive data exposure.** If the LLM does not need a secret to complete a task, do not include that secret in its context.

This mitigation reduces the model's opportunity to disclose the specific secret. It does not replace application-level authorization, secure secret storage, or controls over other data flows.

## 6. Mitigation Verification

The same three extraction strategies were retested after the change.

| Test | Observed result |
|---|---|
| Prompt override | No disclosure observed |
| Direct secret request | No disclosure observed |
| Verbatim extraction | No disclosure observed |

The responses did not contain the synthetic token.

These results establish the observed outcome for the tested prompts. They do not prove that all possible disclosure paths are eliminated.

## 7. Automated Regression Test

An automated test was added at:

`tests/test_secret_disclosure.py`

The test mocks the LLM response and inspects the actual prompt passed to the model. It verifies that the synthetic token is absent from that prompt.

This is stronger than testing only whether the model refuses a request: it verifies the architectural property that the secret is not sent to the LLM through this code path.

**Test status:** Passed.

The test does not independently prove that every application endpoint, log, integration, or other code path is free of the secret.

## 8. Residual Risks and Next Tests

The following areas remain relevant:

- Search for other code paths that pass secrets to the LLM.
- Ensure secrets are not exposed in application logs or error messages.
- Verify that future features do not accidentally add sensitive values to prompts.
- Test alternate extraction attempts after confirming the actual prompt boundary.
- Use appropriate secret storage and server-side authorization for sensitive operations.

A model's refusal should not be treated as the primary security control when sensitive data can be kept outside its context.

## 9. Conclusion

The original implementation disclosed the synthetic token under two of three tested extraction strategies.

The mitigation removed the token from the LLM's application context. All three original prompts were retested without observed disclosure, and an automated regression test passed to verify that the token was absent from the prompt sent to the model.

**Result:** The tested architectural mitigation was successful. Broader security assurance requires testing additional data flows and bypass scenarios.
