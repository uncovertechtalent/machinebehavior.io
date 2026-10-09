title: OpenCode Self-Hosted LLM Configuration
summary: OpenCode connects to any self-hosted LLM that exposes an OpenAI-compatible API via the @ai-sdk/openai-compatible provider.
parent: tools
order: 100
labels: ai-agents, configuration, llm, opencode, tool
aliases: OpenCode Config | OpenCode Self-Hosted | OpenCode Provider
type: tool
created: 2026-04-25
updated: 2026-04-25
origin: SRE/tools/OpenCode Self-Hosted LLM Configuration.md
reviewed: no
---
> OpenCode connects to any self-hosted LLM that exposes an OpenAI-compatible API via the `@ai-sdk/openai-compatible` provider. Configure in `~/.config/opencode/opencode.json` globally or `./opencode.json` per project. Verify with `curl /v1/models` before wiring up the agent.

## The two configuration paths

**Quick path, env var.** If the endpoint is OpenAI-compatible (vLLM, TGI, llama.cpp server, Ollama, LM Studio, LiteLLM):

```bash
export LOCAL_ENDPOINT=https://your-internal-llm.company.internal/v1
opencode
```

OpenCode auto-discovers models. Select via `/models`.

**Explicit provider path.** More control, production shape:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "orion/azure_ai/claude-sonnet-4-6",
  "provider": {
    "orion": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Orion (Internal)",
      "options": {
        "baseURL": "https://orion.ms.org/v1",
        "apiKey": "YOUR_API_KEY_OR_TOKEN"
      },
      "models": {
        "azure_ai/claude-sonnet-4-6": {
          "name": "Claude Sonnet 4.6 (Orion)"
        }
      }
    }
  }
}
```

Top-level `model` sets the default. `provider.<name>` declares the custom provider; `npm: "@ai-sdk/openai-compatible"` is the Vercel AI SDK adapter for OpenAI-compatible endpoints. `models` enumerates what's available through the provider.

## File location

Per-project: `./opencode.json` at repo root. Takes precedence.

Global: `~/.config/opencode/opencode.json`. For a company-wide self-hosted LLM, global is the right place.

## Schema gotcha: agent vs agents

Earlier versions of the schema used `agents` (plural) as a top-level key. Current schema uses `agent` (singular), and the default model is set at the top level. Wrong key errors with `Unrecognized key: "agents"`.

Current shape for per-agent model override:

```json
{
  "agent": {
    "build": {
      "model": "orion/azure_ai/claude-sonnet-4-6"
    },
    "plan": {
      "model": "orion/azure_ai/claude-sonnet-4-6"
    }
  }
}
```

## The small_model key

OpenCode uses a separate `small_model` for lightweight tasks like session title generation (defaults to `gpt-5-nano` via Zen). To lock everything to your internal endpoint, set `"small_model": "orion/azure_ai/claude-sonnet-4-6"` at top level. Usually overkill; the main agent model is what matters.

## Verify before wiring

Before touching config, confirm the endpoint actually speaks OpenAI-compatible:

```bash
curl -s https://your-endpoint/v1/models \
  -H "Authorization: Bearer $YOUR_TOKEN" | jq .
```

Look for a `data` array with model objects. If `/v1` doesn't work, try `/api/v1` or the root. The model IDs in the response are what you put in the `models` block verbatim.

## Constraints worth knowing

**Context window:** OpenCode requires a minimum 16K context. For agentic work (file read/write, bash exec, grep, multi-step tool loops), 32K+ is the practical floor. See [[Context Window Sizes and Effective Range]].

**Tool calling support:** The real bottleneck. OpenCode depends on reliable function/tool calling. Models that work: Qwen3 Coder, Llama 3.3 70B+, Mistral Large, DeepSeek Coder V3, Claude Sonnet 4.6. Smaller or weaker-tool-calling models will hang or loop in the agentic cycle.

**Auth:** If the endpoint sits behind mTLS, SSO-protected gateway, or requires a bearer token, handle at the network layer (VPN, mesh VPN like [[Headscale Mesh VPN for Data Sovereignty]]) or via the `apiKey` option. The env var convention (`<PROVIDER_NAME>_API_KEY`) sometimes works for custom providers; test it.

## LiteLLM-style gateways

A gateway like `orion.ms.org` that proxies Azure AI, Bedrock, or other backends typically uses model names like `azure_ai/claude-sonnet-4-6` or `bedrock/claude-3-5-sonnet-20241022`. The slash in the model ID is part of the name; keep it as-is in the `models` block. The browser UI's `?model=` query parameter is cosmetic; the API endpoint itself is the base URL.

## See also
[[Memory Architecture L0-L4]] · [[LLM as Software-Defined CPU]] · [[Apple Silicon vs Desktop GPU for Inference]] · [[Headscale Mesh VPN for Data Sovereignty]] · [[Context Window Sizes and Effective Range]]
