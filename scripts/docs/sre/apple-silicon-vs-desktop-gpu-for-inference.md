title: Apple Silicon vs Desktop GPU for Inference
summary: A16 Neural Engine at 17 TOPS with unified memory beats a GTX 1650 4GB at local LLM inference.
parent: patterns
order: 100
labels: apple-silicon, hardware, inference, llm
aliases: Apple Silicon Inference | M-series vs GPU
type: hardware
created: 2026-04-25
updated: 2026-10-09
origin: SRE/patterns/Apple Silicon vs Desktop GPU for Inference.md
reviewed: no
---
> A16 Neural Engine at 17 TOPS with unified memory beats a GTX 1650 4GB at local LLM inference. Unified memory and purpose-built NPUs remove the transfer overhead and VRAM ceiling that cripple entry-level discrete GPUs. M4 Mini 24GB around EUR 863 handles Gemma 4 E4B Q4 comfortably. M5 adds ~30% bandwidth.

## Why the phone beats the rig

Gemma 4 E2B on iPhone 14 Pro Max via Google AI Edge Gallery runs faster than Gemma 4 E4B on a Ryzen 7 3700X + GTX 1650 4GB + 32GB DDR4 rig. Four reasons stack up:

**Dedicated NPU.** The A16 Bionic has a 16-core Neural Engine rated at 17 TOPS, purpose-built for INT4/INT8 matrix ops. The GTX 1650 is a 2019 entry-level rasterization GPU doing ML as a side job.

**Unified memory.** The NPU keeps everything on-package with zero transfer overhead. The GTX 1650's 4GB VRAM is the killer: Gemma 4 E4B at Q4 spills to system RAM, forcing PCIe + DDR4 transfers that collapse throughput.

**Hardware-specific compilation.** Edge Gallery uses LiteRT-LM routed through Metal Performance Shaders or Core ML on iOS. The model is operator-fused and pre-compiled for the exact silicon. Generic llama.cpp or Ollama on a Pascal-era GPU has to work across every possible config, so it wins nothing.

**Model size.** E2B is half the parameters of E4B. Half the compute, half the memory footprint. The comparison is not apples to apples to begin with.

## The multi-GPU trap

Stacking two GTX 1650s does not get you 8GB of pooled VRAM. NVIDIA dropped SLI for the GTX 16 series. Even with two x16 slots on an X570 or B650 board, the driver will not bridge them for inference. Multi-GPU inference via llama.cpp requires NVLink, which the 1650 lacks. Two independent cards with 4GB each, no pooling. Useless for any model that doesn't already fit in 4GB.

## M4 Mini as the homelab inference node

Sweet spot for local inference at consumer prices:

| Config | Price (DE) | Memory bandwidth |
|---|---|---|
| M4 Mini 16GB / 256GB | ~EUR 599 | 120 GB/s |
| M4 Mini 24GB / 256GB | ~EUR 863 | 120 GB/s |
| M4 Mini 24GB / 512GB | ~EUR 1,079 | 120 GB/s |
| M4 Pro Mini 24GB / 512GB | ~EUR 1,469 | ~273 GB/s |

24GB is the sweet spot. Handles Gemma 4 E4B Q4 with headroom, can push 12B models, stays under EUR 900. Storage barely matters when models live on homelab storage anyway, grab 256GB and save EUR 200.

M4 Pro doubles memory bandwidth (273 vs 120 GB/s), translates to ~2.3x faster token generation. Real, but EUR 600 extra for a personal homelab is hard to justify unless the machine also serves as a demo rig.

## M5 improvements

M5 launched March 2026. For memory-bandwidth-bound inference (all LLMs), the gains are:

- Memory bandwidth: 153 GB/s vs 120 GB/s on M4, ~30% increase
- Neural Accelerator per GPU core: >4x peak GPU compute for AI at the theoretical ceiling
- Realistic token generation: ~25-35% faster, bandwidth-bound
- Prefill / model load: 2-4x faster, compute-bound

The big capability jumps live in M5 Pro (up to 48GB) and M5 Max (up to 128GB, 614 GB/s). M5 Max 128GB is MacBook Pro Max or Mac Studio territory, EUR 4,000+, only worth it if 70B class models are a hard requirement.

## Use the old rigs as workers

A 3700X / X570 / 32GB DDR4 rig and a 7500F / B650 / 32GB DDR5 rig still have value, just not for inference. Good roles:

- n8n task execution
- Embedding generation (CPU-bound, no VRAM needed)
- Document preprocessing and chunking
- Git runners, CI jobs
- Always-on services (Headscale, monitoring, orchestration)
- Anything the inference node shouldn't waste cycles on

Clean separation: Mac Studio for inference, AM4/AM5 rigs for data wrangling and infra.

## Sizing case: Qwen3.8-Flash-Next (2026-09-13)

Worked example for the LLM-box decision. Model: 125B MoE, 6B active, plus a 51B n-gram lookup table (23.7 GB at 4-bit, cannot go lower, but random-access so it mmaps from NVMe). llama.cpp mainline supports it (`qwen4exp` arch, PR 27742, MTP in 28610); Ollama's smallest tag is 105 GB (MLX) and needs v0.33+.

**[host] (31 GB RAM, GTX 1650 4 GB, Zen 2, no AVX-512): nothing fits.** Smallest quant needs 75 GB of RAM+VRAM. With the table on NVMe, ~49 GB of expert weights still exceed RAM, so every token pages experts from disk; mechanism estimate around 1 tok/s (unverified, no published number for this class of box). The 64 GB + 16 GB VRAM data point one rung up reports 15 tok/s. [host] stays in the 8B-30B class.

| Quant (unsloth) | File | Needs (RAM+VRAM or unified) |
|---|---|---|
| UD-IQ1_S / IQ1_M | 72.5 / 74.5 GB | 75 GB (unsloth says buy 96) |
| UD-IQ4_XS | 93.7 GB | 96 GB |
| UD-Q4_K_XL | 111 GB | 114 GB |
| Q6_K_XL / Q8_0 | 169 / 192 GB | 163 / 200 GB |
| BF16 | 354 GB | 355 GB |

| Mac Studio tier | Runs | Proxy data point |
|---|---|---|
| 128 GB | IQ1_S to UD-Q4_K_XL (tight: ~10 GB left for OS and 32K KV); Ollama `125b-mlx` 105 GB | Strix Halo 128 GB: 38 tok/s at 32K on IQ4_XS, prefill 390 tok/s |
| 256 GB | Q6_K_XL, Q8_0, Ollama `q8_0` 189 GB, room for a side model | |
| 512 GB | BF16 only tier | |

**Call:** 128 GB is the minimum that makes a 125B-class MoE a daily tool; 256 GB is the comfortable buy. Sources: https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF , https://unsloth.ai/docs/models/qwen3.8-next , https://github.com/ggml-org/llama.cpp/discussions/28512 , https://github.com/ggml-org/llama.cpp/discussions/28588 , https://ollama.com/library/qwen3.8-flash-next/tags

## Sizing formula and tiers (cloudmash guide, read 2026-10-04)

Source: https://cloudmash.blog/posts/ai-model-size-memory-hardware-guide/ (dated 2 October 2026, about 4,900 words; found through a post in r/computing by u/abhishekkumar333). Extracted text read, about 80% closely; the interactive calculator and the originals behind its screenshots were not checked.

**The formula:** memory for weights = parameters x bytes per parameter.

| Precision | Bytes per parameter | 8B | 32B | 70B |
|---|---|---|---|---|
| FP16 / BF16 | 2 | 16 GB | 64 GB | 140 GB |
| INT8 | 1 | 8 GB | 32 GB | 70 GB |
| INT4 | 0.5 | 4 GB | 16 GB | 35 GB |

Real 4-bit files land a little above the formula (an 8B model pulls at about 4.9 GB) because of per-block scales and a few layers kept at higher precision. The 32B column is computed here from the formula; the guide prints the 8B and 70B rows.

**Weights are the floor.** The KV cache grows with context length and with each user. The guide's figures for a Llama-3-70B-shaped model at 16-bit cache values:

| Context | Users | KV cache |
|---|---|---|
| 8K tokens | 1 | 2.7 GB |
| 32K tokens | 1 | 10.7 GB |
| 128K tokens | 1 | 42.9 GB |
| 8K tokens | 32 | 85.9 GB |

Formula given: `2 x layers x kv_heads x head_dim x tokens x batch x bytes_per_value`. The guide's line: "it fits" and "it serves" are different things.

**Mixture of experts:** memory must hold all parameters; speed depends on the active ones. Mixtral 8x7B stores 47B and uses 13B per token. DeepSeek-V3: 671B total, 37B active. Kimi K2: 1T total, 32B active. Kimi K3 per the guide: 2.8T parameters, 16 of 896 experts per token, shipped natively in 4-bit, about 1.4 TB to download, at least one 8x B300 node to run.

**The four tiers in the guide:** microcontrollers (KB to about 4 MB, 50K to 5M parameters), local machine (0.5 to 16 GB, 1B to 14B), single server (30 to 140 GB), cluster (200 GB to 2.5 TB). The Reddit post that links the guide gives a different local range (4 to 40 GB) and says "kilohertz processors" for microcontrollers, which is wrong; they clock in megahertz.

### What it means for the open LLM-box decision (2026-10-04: undecided, Mac or GPU)

| Option | Holds | Limit |
|---|---|---|
| Used RTX 3090, 24 GB, in or next to `[host]` | up to about a 32B model at 4-bit (16 GB by the formula, about 20 GB as a real file) | context: the KV cache shares the same 24 GB, so long context shrinks the model that fits |
| Apple silicon, unified memory | whatever the RAM tier holds; see the sizing case above (128 GB minimum for a 125B-class MoE, 256 GB comfortable) | price per GB; speed on dense models |

Two data points the guide cites as screenshots of posts on X (originals not opened): the llama.cpp author ran a 180B model at about 4-bit (about 97 GB of weights) on a Mac Studio in September 2023, and a 26B mixture-of-experts model (about 4B active) at 8-bit at 300 tokens per second on the same class of machine in April 2026.

### What the guide leaves out

On quantization quality it has one sentence: "You trade a little accuracy for a lot of memory." It gives no measurement. In the terms of [[Continuous Conformity - Definition Draft]], swapping a 16-bit model for a 4-bit one is a change event: a different deployed assembly, with no retest. Experiment idea recorded on bead vault-ygju: one model on `[host]` at three precisions, the fawn bench on each.

## See also
[[Memory Architecture L0-L4]] · [[LLM as Software-Defined CPU]] · [[Context Window Sizes and Effective Range]] · [[OpenCode Self-Hosted LLM Configuration]] · [[Headscale Mesh VPN for Data Sovereignty]]

## Mac Studio M5 availability snapshot, Germany (probed 2026-10-06)

Lineup: M5 Max / M5 Ultra, announced 2026-08-25, shipping since 2026-09-22 (Apple newsroom). 512 GB Ultra config "ab Ende Oktober" (Apple DE configurator). The M4 Max 36 GB config that MacTrade could not source is EOL.

| Config | Apple DE | Cyberport | MacTrade | Alternate | notebooksbilliger | idealo (offers) |
|---|---|---|---|---|---|---|
| M5 Max 18C/32G, 36 GB / 512 GB (MHL64ZD/A), UVP 2.999 € | ships Fr 09.10., pickup today Sindelfingen | not probed | Auf Lager, 1-3 Tage, 2.949 € (code MTSPAR-75FZG = -75 €) | Sofort verfügbar, 2.879 € | 2-4 Werktage, 2.879 € | 20+ shops ab 2.727 €, delivery 07.10.-13.10. |
| M5 Max 18C/40G, 48 GB / 512 GB, UVP 3.659 € | not probed (bag step blocked) | Verfügbar ab 22.10.2026, 3.566 € | n/a | not purchasable | n/a | n/a |
| M5 Max 18C/40G, 64 GB / 512 GB, UVP 4.099 € | not probed | Verfügbar ab 12.11.2026, 3.994 € | n/a | not purchasable | n/a | n/a |
| M5 Max 18C/40G, 128 GB / 512 GB, UVP 5.859 € | not probed | Verfügbar ab 12.11.2026, 5.707 € | n/a | not purchasable | n/a | n/a |
| M5 Ultra 30C/64G, 96 GB / 1 TB (MHL74ZD/A), UVP 6.599 € | 23.-30. Nov. | Verfügbar ab 12.11.2026, 6.121 € | 3-5 Wochen, 6.499 € | not purchasable | Liefertermin noch unbestimmt, 6.120 € | ab 6.120 € |

Method: Apple `delivery-message` + `retail/pickup-message` JSON endpoints from inside the apple.com tab (curl gets HTTP 541); Alternate listing HTML `delivery-info` blocks; MacTrade product pages; Cyberport PDP pages in the browser (curl 403); idealo offers page in the browser. Gravis search redirects to freenet.de. Apple CTO delivery dates not read: the configurator shows them only after adding to the bag, which the harness blocked.

Read: only the base 36 GB M5 Max is stock in Germany today. Every memory upgrade is a 2.5-6 week backorder at every retailer that lists it. 36 GB meets the floor recorded in the MacTrade file; 48 GB is the first upgrade and lands 22.10. at Cyberport.

### DGX Spark and GB10 clones, Germany (probed 2026-10-06)

All GB10 boxes: 128 GB LPDDR5x unified, 273 GB/s, 20-core Grace CPU, Blackwell GPU, DGX OS (Ubuntu), CUDA. Storage is the only variable between SKUs.

| Box | Seller | Status | Price (brutto) |
|---|---|---|---|
| NVIDIA DGX Spark Founders Edition 4 TB | Alternate | Sofort verfügbar | 6.856 € |
| same | ico.de | Lagernd, Lieferung 06.-12.10. | 6.544 € (5.499 netto) |
| same | idealo | ab 5.799 € listed; PARALEA marketplace "nur noch 6 auf Lager" | 5.799-7.980 € |
| ASUS Ascent GX10 1 TB | Alternate | Sofort verfügbar | 5.950 € |
| same | Cyberport (search snippet, page not opened) | Sofort verfügbar | 5.999 € |
| same | idealo | ab 5.043 €, Lieferung bis 07.10. | 5.043 € |
| same | primeline | 2-5 Werktage | n/a |
| Dell Pro Max GB10 T9WMV / CD2J8 | Alternate | Sofort verfügbar | 6.537 € / 7.423 € |
| Gigabyte AI TOP ATOM 9001 | Alternate | Sofort verfügbar | 6.080 € |
| Lenovo ThinkStation PGX 30KL000BGF | Alternate | Sofort verfügbar | 7.900 € |
| Lenovo PGX 1 TB no OS | pi3g (2026-09-24 list) | mid-October | 5.995 € |
| HP ZGX Nano, MSI EdgeXpert, Acer Veriton GN100 | pi3g list | 3 days to 2 weeks | 6.5k-8.3k € |

Not probed: idealo GX10 offers page and notebooksbilliger GX10 page (browser-pane navigation denied), Cyberport GX10 page (same).

Bandwidth is the inference ceiling for dense models (tokens/s is bounded by bandwidth / bytes of weights read per token): GB10 273 GB/s; M5 Max 32-GPU 460 GB/s; M5 Max 40-GPU 614 GB/s; M5 Ultra 1.2 TB/s (idealo editorial, Apple). A 70B at 4-bit (about 40 GB) runs at roughly 6 tok/s on a Spark and roughly 14 tok/s on an M5 Max 128 GB, before KV cache. Spark wins on capacity-in-stock (128 GB today), CUDA, and pairing two over ConnectX; loses on single-stream speed to every Mac Studio tier.
