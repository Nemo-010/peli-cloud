# Usage-ranked provider catalogue

Generated 2026-10-02 by `tools/rank.py` from `data/derived.json`. Every one of the 366 surveyed providers is here.

**Shape:** 2 vCPU / 4 GiB RAM / 20 GiB disk. **Assumptions:** CPU 50%, RAM 50%, no persistent disk, no egress. Prices are list prices in USD for the whole horizon. Free *monthly* credits are applied; one-time credits are not. Each horizon is the cheapest eligible split into sessions of at least 30 minutes; `sessions`/`session_min` per provider and horizon are in `data/derived.json`. Required features and product classes are **not** applied: this is a shape ranking.

Horizons: **1 h** = 1 h, **10 h** = 10 h, **1 day** = 24 h, **1 week** = 168 h, **10 h/d x30** = 300 h, **24/7 x30** = 720 h.

Main table is ranked by **10 h/d x30** (the realistic agent month). A dash means the shape cannot be priced on that provider/horizon.

## Every surveyed provider, ranked by the realistic agent month (10 h/day x 30)

| # | Provider | Type | 1 h | 10 h | 1 day | 1 week | 10 h/d x30 | 24/7 x30 | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.0014 | $0.014 | $0.033 | $0.230 | $0.411 | $0.986 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 2 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.0085 | $0.085 | $0.204 | $1.43 | $2.55 | $6.12 | egress unpublished |
| 3 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $0.010 | $0.103 | $0.247 | $1.73 | $3.09 | $7.41 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 4 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $0.010 | $0.104 | $0.250 | $1.75 | $3.12 | $6.49 |  |
| 5 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | $0 | $0 | $0 | $3.60 | $16.20 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 6 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.014 | $0.137 | $0.329 | $2.30 | $4.11 | $9.86 | egress unpublished |
| 7 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0 | $0 | $0 | $0.144 | $4.36 | $17.77 | $5.22/mo free credit |
| 8 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $0.015 | $0.148 | $0.355 | $2.48 | $4.44 | $10.65 |  |
| 9 | [netcup VPS](https://www.netcup.com/en/server/vps) | hyperscaler/vm | $5.03 | $5.03 | $5.03 | $5.03 | $5.03 | $5.03 | entry row is VPS Lite 1 (6-month min); VPS 500 is $8.51/mo; price is one month's rent at every horizon |
| 10 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $0 | $0 | $0.984 | $5.68 | $20.64 | $5/mo free credit |
| 11 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $0.019 | $0.193 | $0.464 | $3.25 | $5.80 | $13.92 | disk beyond 0 GiB: price unknown |
| 12 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $0.020 | $0.200 | $0.480 | $3.36 | $6.00 | $14.40 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 13 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $0.020 | $0.200 | $0.480 | $3.36 | $6.00 | $14.40 | egress unpublished |
| 14 | [UpCloud](https://upcloud.com/pricing/) | hyperscaler/vm | $0.021 | $0.209 | $0.500 | $3.50 | $6.25 | $14.00 |  |
| 15 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $0.022 | $0.218 | $0.524 | $3.67 | $6.55 | $15.72 | Medium only: runtime fixes 4 vCPU / 4 GiB |
| 16 | [Contabo](https://contabo.com/en-us/pricing/) | hyperscaler/vm | $6.60 | $6.60 | $6.60 | $6.60 | $6.60 | $6.60 | visible $4.40 is a 24-month intro, list is $6.60; price is one month's rent at every horizon |
| 17 | [Fly.io Machines](https://fly.io/pricing) | paas/firecracker | $0.025 | $0.253 | $0.607 | $4.25 | $7.58 | $18.20 |  |
| 18 | [OVHcloud Public Cloud](https://us.ovhcloud.com/public-cloud/prices/) | hyperscaler/vm | $0.026 | $0.256 | $0.614 | $4.30 | $7.68 | $18.43 |  |
| 19 | [Scaleway Instances](https://www.scaleway.com/en/pricing/virtual-instances/) | hyperscaler/vm | $0.026 | $0.259 | $0.623 | $4.36 | $7.78 | $18.67 | Stardust disk is billed on top of the instance rate |
| 20 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $0 | $0 | $0 | $0.038 | $7.92 | $33.02 | $10/mo free credit |
| 21 | [Kamatera](https://www.kamatera.com/pricing/) | hyperscaler/vm | $0.028 | $0.274 | $0.658 | $4.60 | $8.22 | $19.73 |  |
| 22 | [Upstash Box](https://upstash.com/pricing/box) | agent-sandbox/container | $0.103 | $1.03 | $2.47 | $8.46 | $8.82 | $9.97 | egress unpublished; flat pool, billed whether used or not |
| 23 | [Civo Compute](https://www.civo.com/pricing) | hyperscaler/vm | $0.030 | $0.298 | $0.714 | $5.00 | $8.93 | $21.43 |  |
| 24 | [Vultr Cloud Compute](https://www.vultr.com/pricing/) | hyperscaler/vm | $0.030 | $0.298 | $0.715 | $5.01 | $8.94 | $20.00 |  |
| 25 | [Together Code Sandbox](https://www.together.ai/pricing) | agent-sandbox/firecracker | $0.030 | $0.300 | $0.720 | $5.04 | $9.00 | $21.60 | no machine size published, not shape-comparable; egress unpublished |
| 26 | [Alibaba Cloud ECS International](https://www.alibabacloud.com/en/product/ecs/pricing) | hyperscaler/vm | $0.030 | $0.302 | $0.725 | $5.08 | $9.06 | $14.48 |  |
| 27 | [Ubicloud](https://www.ubicloud.com/docs/about/pricing) | hyperscaler/vm | $0.031 | $0.312 | $0.749 | $5.24 | $9.36 | $22.46 |  |
| 28 | [Anchor Browser](https://anchorbrowser.io/pricing) | browser/dedicated-vm | $0 | $0 | $0 | $3.41 | $10.01 | $31.01 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 29 | [Prized](https://prized.dev/docs/billing) | dev-env/vm | $10.00 | $10.00 | $10.00 | $10.00 | $10.27 | $24.66 | $10/mo minimum, fee is a usage credit; egress unpublished |
| 30 | [KakaoCloud Virtual Machine](https://www.kakaocloud.com/services/virtual-machine/pricing) | hyperscaler/vm | $0.035 | $0.349 | $0.838 | $5.86 | $10.47 | $25.13 |  |
| 31 | [IBM Cloud VPC](https://www.ibm.com/products/virtual-servers/pricing) | hyperscaler/vm | $0.035 | $0.352 | $0.844 | $5.91 | $10.55 | $25.33 |  |
| 32 | [DigitalOcean Droplets](https://www.digitalocean.com/pricing/droplets) | hyperscaler/vm | $0.036 | $0.357 | $0.857 | $6.00 | $10.71 | $24.00 |  |
| 33 | [Akamai Cloud / Linode](https://www.akamai.com/cloud/pricing) | hyperscaler/vm | $0.036 | $0.360 | $0.864 | $6.05 | $10.80 | $24.00 |  |
| 34 | [Tencent Cloud Studio](https://cloud.tencent.cn/document/product/1039/131894) | dev-env/container | $0.037 | $0.373 | $0.894 | $6.26 | $11.18 | $26.82 | disk beyond 0 GiB: price unknown; egress unpublished |
| 35 | [Azure Virtual Machines (Linux)](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/) | hyperscaler/vm | $0.040 | $0.397 | $0.952 | $6.66 | $11.90 | $28.55 |  |
| 36 | [Paperspace](https://docs.digitalocean.com/products/paperspace/pricing/) | gpu-cloud/vm | $0.043 | $0.427 | $1.03 | $7.18 | $12.82 | $30.77 |  |
| 37 | [Kernel](https://www.onkernel.com/pricing) | browser/firecracker | $0 | $0 | $0 | $5.08 | $13.00 | $38.20 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 38 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $0 | $0 | $5.09 | $13.01 | $38.21 | $5/mo free credit; egress unpublished |
| 39 | [tama](https://tama.computer/) | agent-sandbox/vm | $0.045 | $0.454 | $1.09 | $7.63 | $13.62 | $32.70 | egress unpublished |
| 40 | [E2E Networks](https://www.e2enetworks.com/pricing) | hyperscaler/vm | $0.047 | $0.467 | $1.12 | $7.85 | $14.02 | $33.65 | egress unpublished |
| 41 | [Exoscale](https://www.exoscale.com/pricing/) | hyperscaler/vm | $0.050 | $0.495 | $1.19 | $8.31 | $14.84 | $35.61 |  |
| 42 | [Hostinger VPS](https://www.hostinger.com/vps-hosting) | hyperscaler/vm | $14.99 | $14.99 | $14.99 | $14.99 | $14.99 | $14.99 | price is one month's rent at every horizon |
| 43 | [Coasty](https://coasty.ai/pricing) | agent-sandbox/vm | $0.050 | $0.500 | $1.20 | $8.40 | $15.00 | $30.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 44 | [exe.dev](https://exe.dev/pricing) | dev-env/vm | $15.00 | $15.00 | $15.00 | $15.00 | $15.00 | $15.00 | $15/mo minimum, fee is a usage credit; flat pool, billed whether used or not |
| 45 | [Mosaic Sandbox](https://sandbox.mosaicos.com/) | agent-sandbox/firecracker | $0.050 | $0.500 | $1.20 | $8.40 | $15.00 | $36.00 | egress unpublished |
| 46 | [AWS EC2 (reference VMs)](https://aws.amazon.com/ec2/pricing/on-demand/) | hyperscaler/vm | $0.051 | $0.513 | $1.23 | $8.62 | $15.39 | $36.93 |  |
| 47 | [STACKIT Compute Engine](https://pim.api.stackit.cloud/v1/skus) | hyperscaler/vm | $0.051 | $0.513 | $1.23 | $8.62 | $15.40 | $36.95 | egress unpublished |
| 48 | [Nebius](https://docs.nebius.com/compute/resources/pricing) | gpu-cloud/vm | $0.051 | $0.515 | $1.24 | $8.66 | $15.46 | $37.11 |  |
| 49 | [machine0](https://machine0.io/) | agent-sandbox/vm | $0.052 | $0.520 | $1.25 | $8.74 | $15.60 | $37.44 |  |
| 50 | [Jarvislabs](https://jarvislabs.ai/pricing) | gpu-cloud/vm | $0.053 | $0.527 | $1.27 | $8.86 | $15.82 | $37.97 |  |
| 51 | [Verda (formerly DataCrunch)](https://verda.com/pricing) | gpu-cloud/vm | $0.053 | $0.535 | $1.28 | $8.98 | $16.04 | $38.51 | egress unpublished |
| 52 | [Runtime (withruntime.com)](https://withruntime.com/pricing) | agent-sandbox/firecracker | $0.055 | $0.550 | $1.32 | $9.24 | $16.50 | $39.60 |  |
| 53 | [Railway](https://railway.com/pricing) | agent-sandbox/vm | $5.00 | $5.00 | $5.00 | $9.34 | $16.68 | $40.02 | disk beyond 0 GiB: price unknown; $5/mo minimum, fee is a usage credit |
| 54 | [Alibaba Cloud Agent Sandbox / FC / AgentRun](https://help.aliyun.com/zh/agent-sandbox/product-overview/billing-overview) | agent-sandbox/- | $0.056 | $0.562 | $1.35 | $9.44 | $16.86 | $40.46 | egress unpublished |
| 55 | [AWS Fargate](https://aws.amazon.com/fargate/pricing/) | hyperscaler/firecracker | $0.058 | $0.581 | $1.39 | $9.76 | $17.43 | $41.83 |  |
| 56 | [Celesto Cloud](https://celesto.ai/pricing) | agent-sandbox/vm | $0.060 | $0.600 | $1.44 | $10.08 | $18.00 | $43.20 | egress unpublished |
| 57 | [Sandbox0](https://sandbox0.ai/pricing) | agent-sandbox/gvisor | $0.060 | $0.606 | $1.45 | $10.17 | $18.16 | $43.59 |  |
| 58 | [Runpod](https://www.runpod.io/pricing) | gpu-cloud/container | $0.063 | $0.627 | $1.51 | $10.54 | $18.82 | $45.17 |  |
| 59 | [Lightpanda Cloud](https://lightpanda.io/pricing) | browser/container | $19.00 | $19.00 | $19.00 | $19.00 | $19.00 | $52.60 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 0.25 h, needs restarts |
| 60 | [UCloud Agent Sandbox](https://astraflow.ucloud.cn/docs/agent-sandbox) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | $19.31 | $46.35 | disk beyond 10 GiB: price unknown; egress unpublished |
| 61 | [PPIO Agent Sandbox](https://ppio.com/docs/sandbox/pricing.md) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | $19.31 | $46.35 | session cap 1 h, needs restarts; egress unpublished |
| 62 | [Volcano Engine AgentKit / veFaaS sandbox](https://docs.volcengine.com/docs/agentkit/Billing_items?lang=zh) | agent-sandbox/vm | $0.065 | $0.653 | $1.57 | $10.98 | $19.60 | $47.05 |  |
| 63 | [boat.dev](https://docs.boat.dev/pricing) | agent-sandbox/vm | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | disk beyond 12 GiB: price unknown; $20/mo minimum, fee is a usage credit |
| 64 | [Notte](https://www.notte.cc/pricing) | browser/container | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; $20/mo minimum, fee is a usage credit |
| 65 | [OpenComputer](https://opencomputer.dev/sandboxes) | agent-sandbox/vm | $0.378 | $3.78 | $9.07 | $20.00 | $20.00 | $92.16 | disk beyond 16 GiB: price unknown; egress unpublished |
| 66 | [Google Compute Engine (Linux VMs)](https://cloud.google.com/products/compute/pricing/general-purpose) | hyperscaler/vm | $0.070 | $0.698 | $1.67 | $11.72 | $20.93 | $50.22 | free tier is a resource allowance, not modelled (see card) |
| 67 | [GitHub Actions hosted runners](https://docs.github.com/en/billing/reference/actions-runner-pricing) | macos/vm | $0 | $0 | $0 | $21.00 | $21.00 | $21.00 | disk beyond 14 GiB: price unknown; session cap 6 h, needs restarts |
| 68 | [Gologin Cloud Browser](https://gologin.com/cloud-browser/) | browser/container | $14.00 | $14.00 | $14.00 | $14.00 | $21.00 | $50.40 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; free tier is a resource allowance, not modelled (see card) |
| 69 | [Northflank Sandboxes](https://northflank.com/pricing) | agent-sandbox/vm | $0.071 | $0.706 | $1.69 | $11.86 | $21.18 | $50.84 |  |
| 70 | [AWS CodeBuild](https://aws.amazon.com/codebuild/pricing/) | paas/container | $0.072 | $0.720 | $1.73 | $12.10 | $21.60 | $51.84 | egress unpublished |
| 71 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $0 | $0 | $0 | $4.13 | $21.81 | $78.07 | $18.38/mo free credit |
| 72 | [Crusoe](https://www.crusoe.ai/cloud/pricing) | gpu-cloud/vm | $0.082 | $0.822 | $1.97 | $13.81 | $24.66 | $59.18 |  |
| 73 | [Sprites (Fly.io)](https://fly.io/pricing) | agent-sandbox/firecracker | $0.083 | $0.826 | $1.98 | $13.87 | $24.76 | $59.43 |  |
| 74 | [smol machines](https://smolmachines.com/pricing) | agent-sandbox/vm | $0.084 | $0.844 | $2.03 | $14.18 | $25.32 | $60.77 |  |
| 75 | [orkestr Sandboxes](https://orkestr.eu/sandboxes) | agent-sandbox/vm | $0.085 | $0.853 | $2.05 | $14.34 | $25.60 | $61.44 | disk beyond 0 GiB: price unknown; egress unpublished |
| 76 | [Red Hat OpenShift (Harbor backend)](https://www.redhat.com/en/technologies/cloud-computing/openshift/pricing) | paas/container | $0.086 | $0.855 | $2.05 | $14.36 | $25.65 | $61.56 | disk beyond 0 GiB: price unknown; egress unpublished |
| 77 | [Buddy Sandboxes](https://buddy.works/pricing) | agent-sandbox/vm | $0 | $0.736 | $1.98 | $14.73 | $26.43 | $63.64 | egress unpublished |
| 78 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $0 | $0 | $0 | $1.91 | $26.98 | $107 | $30/mo free credit |
| 79 | [Sandbox as a Service](https://sandbox-as-a-service.com/pricing) | agent-sandbox/vm | $0.090 | $0.900 | $2.16 | $15.12 | $27.00 | $64.80 | egress unpublished |
| 80 | [Clever Cloud](https://www.clever.cloud/pricing/) | paas/vm | $0.092 | $0.918 | $2.20 | $15.43 | $27.55 | $66.12 | disk beyond 0 GiB: price unknown; egress unpublished |
| 81 | [Samsung SDS Cloud Platform](https://cloud.samsungsds.com/serviceportal/pricing.html) | hyperscaler/vm | $0.092 | $0.925 | $2.22 | $15.53 | $27.74 | $66.57 |  |
| 82 | [Prime Intellect Sandboxes](https://www.primeintellect.ai/sandboxes) | agent-sandbox/vm | $0.094 | $0.940 | $2.26 | $15.79 | $28.20 | $67.68 | egress unpublished |
| 83 | [Sakura Internet Cloud](https://cloud.sakura.ad.jp/products/server/) | hyperscaler/vm | $0.139 | $1.39 | $3.35 | $23.42 | $28.61 | $31.17 | price is one month's rent at every horizon |
| 84 | [Koyeb Sandboxes](https://www.koyeb.com/pricing) | agent-sandbox/vm | $29.00 | $29.00 | $29.00 | $29.00 | $29.00 | $39.74 |  |
| 85 | [Alibaba Cloud AgentBay](https://www.alibabacloud.com/help/en/agentbay/product-overview/agentbay-billing-instructions) | agent-sandbox/container | $0.099 | $0.992 | $2.38 | $16.67 | $29.76 | $71.42 | disk beyond 0 GiB: price unknown |
| 86 | [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | browser/firecracker | $0.100 | $1.00 | $2.40 | $16.80 | $30.00 | $72.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 12 h, needs restarts |
| 87 | [Morph Cloud](https://cloud.morph.so/web/subscribe) | agent-sandbox/vm | $0.100 | $1.00 | $2.40 | $16.80 | $30.00 | $62.00 | disk beyond 16 GiB: price unknown; egress unpublished |
| 88 | [Cloudflare Browser Run / Kitesurf](https://developers.cloudflare.com/browser-run/pricing/) | browser/container | $5.00 | $5.00 | $6.26 | $19.22 | $31.10 | $68.90 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 89 | [Hetzner Dedicated AX / EX](https://www.hetzner.com/dedicated-rootserver/) | hyperscaler/dedicated-host | $0.107 | $1.07 | $2.58 | $18.06 | $32.25 | $67.10 |  |
| 90 | [Blacksmith (GitHub Actions runners)](https://www.blacksmith.sh/pricing) | macos/vm | $0 | $0 | $0 | $13.20 | $33.00 | $96.00 | $12/mo free credit; egress unpublished |
| 91 | [Isorun](https://docs.isorun.ai/getting-started/pricing) | agent-sandbox/vm | $0.110 | $1.10 | $2.65 | $18.55 | $33.13 | $79.52 |  |
| 92 | [Novita AI Agent Sandbox](https://docs.novita.ai/guides/sandbox-pricing) | agent-sandbox/firecracker | $0.117 | $1.17 | $2.80 | $19.60 | $34.99 | $83.98 | egress unpublished |
| 93 | [CreateOS Sandbox (NodeOps)](https://createos.sh/products/sandbox) | agent-sandbox/firecracker | $10.00 | $10.00 | $10.00 | $20.47 | $36.56 | $87.74 | $10/mo minimum, fee is a usage credit |
| 94 | [Render](https://render.com/pricing) | paas/container | $0.123 | $1.23 | $2.96 | $20.71 | $36.99 | $88.77 |  |
| 95 | [Amazon Bedrock AgentCore (Runtime / Code Interpreter / Browser)](https://aws.amazon.com/bedrock/agentcore/pricing/) | hyperscaler/firecracker | $0.127 | $1.27 | $3.06 | $21.39 | $38.19 | $91.66 | disk beyond 10 GiB: price unknown; session cap 8 h, needs restarts |
| 96 | [Collimate](https://collimate.ai/pricing) | agent-sandbox/firecracker | $0.128 | $1.28 | $3.07 | $21.50 | $38.40 | $92.16 | disk beyond 0 GiB: price unknown |
| 97 | [Open Telekom Cloud / T Cloud Public](https://www.open-telekom-cloud.com/en/prices) | hyperscaler/vm | $0.133 | $1.32 | $3.18 | $22.26 | $39.75 | $95.40 |  |
| 98 | [Docker Cloud Sandboxes](https://www.docker.com/blog/introducing-cloud-sandboxes-start-on-your-laptop-finish-in-the-cloud/) | agent-sandbox/vm | $0.140 | $1.40 | $3.36 | $23.52 | $42.00 | $101 |  |
| 99 | [NAVER Cloud / LINE-NAVER scope](https://www.ncloud.com/product/compute/server) | hyperscaler/vm | $0.141 | $1.41 | $3.39 | $23.75 | $42.42 | $102 | disk beyond 0 GiB: price unknown; egress unpublished |
| 100 | [Tencent Cloud Agent Runtime — Agent Sandbox](https://cloud.tencent.com/document/product/1814/133249) | agent-sandbox/- | $0.142 | $1.42 | $3.41 | $23.88 | $42.64 | $102 | egress unpublished |
| 101 | [Cloudflare Sandbox SDK / Containers](https://developers.cloudflare.com/containers/platform/pricing/) | agent-sandbox/vm | $5.00 | $5.59 | $7.42 | $26.29 | $43.59 | $98.62 |  |
| 102 | [Deno Sandbox](https://deno.com/deploy/pricing) | agent-sandbox/firecracker | $20.00 | $20.00 | $20.00 | $23.13 | $44.25 | - | disk beyond 10 GiB: price unknown; session cap 0.5 h, needs restarts |
| 103 | [Dedalus Labs](https://www.dedaluslabs.ai/pricing) | agent-sandbox/vm | $0.151 | $1.51 | $3.62 | $25.37 | $45.31 | $109 | egress unpublished |
| 104 | [MIOSA](https://miosa.ai/pricing) | agent-sandbox/firecracker | $0.155 | $1.55 | $3.72 | $26.07 | $46.56 | $112 | disk beyond 10 GiB: price unknown |
| 105 | [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | dev-env/vm | $0 | $0 | $0 | $21.33 | $46.58 | $127 |  |
| 106 | [boxd](https://boxd.sh/pricing) | agent-sandbox/vm | $0.156 | $1.56 | $3.75 | $26.28 | $46.92 | $113 | egress unpublished |
| 107 | [Latitude.sh](https://www.latitude.sh/pricing) | hyperscaler/dedicated-host | $0.190 | $1.90 | $4.56 | $31.92 | $48.33 | $48.33 | price is one month's rent at every horizon |
| 108 | [microsandbox](https://microsandbox.dev/pricing) | agent-sandbox/vm | $49.00 | $49.00 | $49.00 | $49.00 | $49.00 | $112 | egress unpublished |
| 109 | [Shardflux](https://shardflux.dev/#pricing) | agent-sandbox/firecracker | $9.00 | $9.00 | $9.00 | $12.04 | $49.00 | $105 | egress unpublished |
| 110 | [E2B](https://e2b.dev/pricing) | agent-sandbox/firecracker | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | egress unpublished |
| 111 | [Leap0](https://leap0.dev/) | agent-sandbox/firecracker | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 10 GiB: price unknown; session cap 8 h, needs restarts; egress unpublished |
| 112 | [Omnara](https://www.omnara.com/pricing) | agent-sandbox/- | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 0 GiB: price unknown; egress unpublished |
| 113 | [OpenReward Sandboxes](https://openreward.ai/pricing) | agent-sandbox/container | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 0 GiB: price unknown; egress unpublished |
| 114 | [Daytona](https://www.daytona.io/pricing) | agent-sandbox/container | $0.167 | $1.67 | $4.01 | $28.09 | $50.17 | $120 | egress unpublished |
| 115 | [Tenki Sandbox](https://tenki.cloud/pricing) | agent-sandbox/vm | $0.167 | $1.67 | $4.01 | $28.09 | $50.17 | $120 | egress unpublished |
| 116 | [Hopx](https://hopx.ai/pricing) | agent-sandbox/firecracker | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 117 | [Runta](https://runta.com/pricing/) | agent-sandbox/vm | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 118 | [Superserve](https://superserve.ai/pricing) | agent-sandbox/firecracker | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 119 | [Declaw](https://docs.declaw.ai/platform/billing) | agent-sandbox/firecracker | $0.169 | $1.69 | $4.05 | $28.33 | $50.58 | $121 | egress unpublished |
| 120 | [Blaxel](https://blaxel.ai/pricing) | agent-sandbox/firecracker | $0.169 | $1.69 | $4.05 | $28.37 | $50.67 | $122 |  |
| 121 | [Cua Fleet](https://cua.ai/pricing) | agent-sandbox/vm | $0.178 | $1.78 | $4.28 | $29.99 | $53.55 | $129 | disk beyond 0 GiB: price unknown; egress unpublished |
| 122 | [WarpBuild (GitHub Actions runners)](https://www.warpbuild.com/pricing) | macos/vm | $0.180 | $1.80 | $4.32 | $30.24 | $54.00 | $130 | egress unpublished |
| 123 | [Opensteer](https://opensteer.com/pricing) | browser/- | $0 | $0 | $0 | $28.60 | $55.00 | $139 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 124 | [Hyperbeam](https://hyperbeam.com/) | browser/- | $0 | $0 | $0 | $0.560 | $56.00 | $232 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 125 | [Arker](https://arker.ai/docs/pricing) | agent-sandbox/vm | $0.188 | $1.88 | $4.51 | $31.54 | $56.32 | $135 | egress unpublished |
| 126 | [Bitrise (mobile CI)](https://bitrise.io/pricing) | macos/vm | $218 | $219 | $221 | $240 | $59.00 | $59.00 | session cap 3.5 h, needs restarts; egress unpublished; price is one month's rent at every horizon |
| 127 | [RunsOn](https://runs-on.com/pricing/) | paas/vm | $29.28 | $30.25 | $31.76 | $47.31 | $61.57 | $107 | egress unpublished |
| 128 | [Google Agent Runtime / Agent Engine](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing) | hyperscaler/gvisor | $0.206 | $2.06 | $4.94 | $34.61 | $61.80 | $148 | disk beyond 0 GiB: price unknown; egress unpublished |
| 129 | [Vercel Sandbox](https://vercel.com/docs/sandbox/pricing) | agent-sandbox/firecracker | $20.00 | $20.00 | $20.00 | $35.75 | $63.84 | $153 | $20/mo minimum, fee is a usage credit |
| 130 | [Azure Container Apps Sandboxes](https://learn.microsoft.com/en-us/azure/container-apps/sandboxes-overview) | hyperscaler/vm | $0.216 | $2.16 | $5.18 | $36.29 | $64.80 | $156 |  |
| 131 | [Beam](https://www.beam.cloud/pricing) | agent-sandbox/gvisor | $0.227 | $2.27 | $5.45 | $38.16 | $68.15 | $164 | disk beyond 0 GiB: price unknown |
| 132 | [Sealos DevBox](https://sealos.io/pricing/) | dev-env/container | $70.00 | $70.00 | $70.00 | $70.00 | $70.00 | $70.00 | disk beyond 0 GiB: price unknown; egress unpublished; flat pool, billed whether used or not |
| 133 | [PandaStack](https://www.pandastack.ai/pricing/) | agent-sandbox/firecracker | $0 | $0 | $0.650 | $36.95 | $70.23 | $176 |  |
| 134 | [Remote Browser](https://remote-browser.dev/pricing) | browser/container | $0 | $2.21 | $4.90 | $38.71 | $71.05 | $174 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 135 | [OpenPond Cloud Sandboxes](https://openpond.ai/pricing) | agent-sandbox/firecracker | $0.238 | $2.38 | $5.70 | $39.92 | $71.28 | $171 | disk beyond 10 GiB: price unknown; egress unpublished |
| 136 | [StarSling](https://starsling.dev/pricing) | dev-env/firecracker | $0.240 | $2.40 | $5.76 | $40.32 | $72.00 | $173 | disk beyond 0 GiB: price unknown; session cap 6 h, needs restarts; egress unpublished |
| 137 | [GKE Agent Sandbox](https://cloud.google.com/kubernetes-engine/docs/concepts/agent-sandbox) | hyperscaler/gvisor | $73.00 | $73.00 | $73.00 | $73.00 | $73.00 | $73.00 | disk beyond 0 GiB: price unknown; egress unpublished |
| 138 | [Ona (formerly Gitpod)](https://ona.com/pricing) | dev-env/vm | $20.00 | $20.00 | $20.00 | $42.00 | $75.00 | $180 | disk beyond 0 GiB: price unknown; $20/mo minimum, fee is a usage credit; egress unpublished |
| 139 | [AWS Lambda MicroVMs](https://aws.amazon.com/lambda/pricing/) | hyperscaler/firecracker | $0.252 | $2.52 | $6.05 | $42.37 | $75.66 | $182 | session cap 8 h, needs restarts |
| 140 | [Namespace](https://namespace.so/pricing) | dev-env/vm | $0.258 | $2.58 | $6.19 | $43.30 | $77.33 | $186 | egress unpublished |
| 141 | [AgentComputer](https://agentcomputer.ai/pricing) | agent-sandbox/firecracker | $0.259 | $2.59 | $6.21 | $43.45 | $77.60 | $186 | egress unpublished |
| 142 | [Amazon WorkSpaces Personal (Windows)](https://aws.amazon.com/workspaces/desktop-as-a-service/pricing/) | windows/vm | $0.287 | $2.81 | $6.73 | $47.05 | $84.01 | $202 |  |
| 143 | [Rivet (Actors & agentOS)](https://rivet.dev/pricing/) | agent-sandbox/- | $20.00 | $20.00 | $20.00 | $48.32 | $86.29 | $207 |  |
| 144 | [CircleCI](https://circleci.com/pricing/price-list/) | macos/vm | $0 | $0 | $0 | $42.48 | $90.00 | $241 | $15/mo minimum, fee is a usage credit; session cap 5 h, needs restarts |
| 145 | [Google Cloud Build](https://cloud.google.com/build/pricing) | paas/vm | $0 | $0 | $0 | $45.48 | $93.00 | $244 | egress unpublished |
| 146 | [Islo](https://islo.dev/pricing) | agent-sandbox/vm | $0.314 | $3.14 | $7.54 | $52.75 | $94.20 | $226 | egress unpublished |
| 147 | [Runloop](https://www.runloop.ai/pricing) | agent-sandbox/vm | $0.324 | $3.24 | $7.77 | $54.37 | $97.09 | $233 | egress unpublished |
| 148 | [Browserbase](https://www.browserbase.com/pricing) | browser/vm | $99.00 | $99.00 | $99.00 | $99.00 | $99.00 | $121 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 6 h, needs restarts |
| 149 | [Orgo](https://www.orgo.ai/pricing) | agent-sandbox/vm | $99.00 | $99.00 | $99.00 | $99.00 | $99.00 | $99.00 | disk beyond 0 GiB: price unknown; egress unpublished; flat pool, billed whether used or not |
| 150 | [Hyperstack](https://www.hyperstack.cloud/gpu-pricing) | gpu-cloud/vm | $0.350 | $3.50 | $8.40 | $58.80 | $105 | $252 |  |
| 151 | [Amika](https://www.amika.dev/pricing) | agent-sandbox/vm | $0 | $0 | $3.99 | $57.90 | $107 | $265 | egress unpublished |
| 152 | [GitLab.com hosted runners](https://docs.gitlab.com/ci/pipelines/compute_minutes/) | macos/vm | $0 | $2.00 | $10.40 | $29.80 | $109 | $361 | session cap 3 h, needs restarts; egress unpublished |
| 153 | [Depot (GitHub Actions runners)](https://depot.dev/pricing) | macos/vm | $20.00 | $20.00 | $20.00 | $68.48 | $116 | $267 | egress unpublished |
| 154 | [Huawei Cloud AgentArts](https://support.huaweicloud.com/price-agentarts/agentarts-price-pdf.pdf) | agent-sandbox/container | $0.397 | $3.97 | $9.53 | $66.74 | $119 | $286 |  |
| 155 | [Expo](https://expo.dev) | macos/vm | $19.00 | $19.00 | $19.00 | $58.00 | $124 | $334 | disk beyond 0 GiB: price unknown; session cap 2 h, needs restarts; egress unpublished |
| 156 | [boxes.dev](https://boxes.dev/) | dev-env/firecracker | $99.00 | $99.00 | $99.00 | $99.00 | $129 | $381 | egress unpublished |
| 157 | [Buildkite hosted agents](https://buildkite.com/pricing) | macos/vm | $0 | $0 | $3.52 | $72.64 | $136 | $338 | session cap 8 h, needs restarts; egress unpublished |
| 158 | [Ellipsis](https://www.ellipsis.dev/pricing) | agent-sandbox/qemu-kvm | $0.457 | $4.57 | $10.96 | $76.73 | $137 | $329 | disk beyond 0 GiB: price unknown; session cap 1 h, needs restarts; egress unpublished |
| 159 | [Intuned](https://intunedhq.com/pricing) | browser/vm | $120 | $120 | $120 | $120 | $145 | $250 | disk beyond 0 GiB: price unknown; session cap 6 h, needs restarts; egress unpublished |
| 160 | [InstaVM](https://instavm.io/pricing) | agent-sandbox/firecracker | $100 | $102 | $104 | $128 | $150 | $221 | egress unpublished |
| 161 | [Baponi](https://baponi.ai/pricing/) | agent-sandbox/container | $97.00 | $97.00 | $97.00 | $128 | $160 | $262 | session cap 1 h, needs restarts |
| 162 | [Bitbucket Pipelines](https://www.atlassian.com/software/bitbucket/pricing) | paas/container | $0.100 | $5.50 | $13.90 | $94.05 | $173 | $425 | session cap 12 h, needs restarts; egress unpublished |
| 163 | [CodeSandbox SDK](https://codesandbox.io/docs/sdk/pricing) | agent-sandbox/firecracker | $170 | $170 | $170 | $171 | $191 | $253 | $5.944/mo free credit; egress unpublished |
| 164 | [Replicas](https://replicas.dev) | agent-sandbox/vm | $50.48 | $54.80 | $61.52 | $131 | $194 | $396 | egress unpublished |
| 165 | [Surfsky](https://surfsky.io/pricing) | browser/container | $199 | $199 | $199 | $199 | $199 | $199 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; $199/mo minimum, fee is a usage credit |
| 166 | [Solari](https://docs.getsolari.com/pricing) | agent-sandbox/vm | $200 | $200 | $200 | $200 | $200 | $200 | disk beyond 4 GiB: price unknown; egress unpublished |
| 167 | [SF Compute (GPU market + Autoresearch sandboxes)](https://autoresearch.sfcompute.com/) | gpu-cloud/vm | $0.732 | $7.32 | $17.56 | $123 | $219 | $527 | disk beyond 0 GiB: price unknown |
| 168 | [BrowserCloud](https://browsercloud.io/pricing) | browser/container | $249 | $249 | $249 | $249 | $249 | $249 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; $249/mo minimum, fee is a usage credit |
| 169 | [Steel.dev](https://docs.steel.dev/overview/pricinglimits) | browser/container | $250 | $250 | $250 | $250 | $250 | $250 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 170 | [Tensorlake Sandboxes](https://www.tensorlake.ai/pricing) | agent-sandbox/firecracker | $250 | $250 | $250 | $250 | $250 | $250 | $250/mo minimum, fee is a usage credit |
| 171 | [OVHcloud GPU instances](https://www.ovhcloud.com/en/public-cloud/prices/) | gpu-cloud/vm | $0.880 | $8.80 | $21.12 | $148 | $264 | $634 | no machine size published, not shape-comparable |
| 172 | [Codemagic (mobile CI)](https://codemagic.io/pricing/) | macos/vm | $2.70 | $27.00 | $64.80 | $332 | $332 | $332 | disk beyond 0 GiB: price unknown; session cap 2 h, needs restarts; egress unpublished |
| 173 | [Browserless](https://www.browserless.io/pricing) | browser/container | $350 | $350 | $350 | $350 | $350 | $350 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 1 h, needs restarts |
| 174 | [StateSet Sandbox](https://sandbox.stateset.app/) | agent-sandbox/gvisor | $299 | $301 | $305 | $338 | $369 | $466 | disk beyond 0 GiB: price unknown; session cap 5 h, needs restarts |
| 175 | [Scrapeless Agent Browser](https://www.scrapeless.com/en/pricing) | browser/- | $399 | $399 | $399 | $399 | $399 | $399 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; $0.09/mo free credit |
| 176 | [Scrapfly Cloud Browser](https://scrapfly.io/pricing) | browser/- | $500 | $500 | $500 | $500 | $500 | - | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 0.5 h, needs restarts |
| 177 | [Archil](https://archil.com/pricing) | agent-sandbox/vm | $500 | $500 | $501 | $528 | $553 | $631 | egress unpublished |
| 178 | [Firecrawl Interact / Browser Sandbox](https://www.firecrawl.dev/pricing) | browser/container | $749 | $749 | $749 | $749 | $749 | $749 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 1 h, needs restarts |
| 179 | [CloudCruise](https://cloudcruise.com/pricing) | browser/dedicated-vm | $0 | $24.00 | $66.00 | $498 | $894 | $2,154 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| - | [Agency Tool Company](https://agencytool.com) | dev-env/bare-metal | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Agent Relay](https://agentrelay.com) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [ainclave](https://www.ainclave.com/pricing) | agent-sandbox/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: On-demand: needs opt-in (sales); Dedicated reserved hosts: needs opt-in (sales); egress unpublished |
| - | [Airtop](https://www.airtop.ai/pricing) | browser/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Alibaba Cloud ACK (Harbor backend)](https://www.alibabacloud.com/product/kubernetes) | hyperscaler/container | - | - | - | - | - | - | not priceable at 10 h/d x30: ACK cluster runtime: needs opt-in (alt); ACK pods on virtual nodes (ECI), per vC; egress unpublished |
| - | [Amp Orbs](https://ampcode.com/docs/orbs/sizes-and-costs) | dev-env/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Hosted orb compute, PAYG or subscription allowance: needs opt-in (alt); egress unpublished |
| - | [Apoxy](https://apoxy.dev) | paas/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Apple Xcode Cloud](https://developer.apple.com/xcode-cloud/) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Xcode Cloud compute hours (Xcode build/test only): needs opt-in (alt); egress unpublished |
| - | [Aptible](https://www.aptible.com) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt, burstable); CPU-Optimized (; egress unpublished |
| - | [Archal](https://www.archal.ai/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Arga Labs](https://www.argalabs.com/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); session cap 8 h, needs restarts; egress unpublished |
| - | [Artillery](https://www.artillery.io/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Test workers and Cloud platform: needs opt-in (alt); egress unpublished |
| - | [AutoComputer](https://www.autocomputer.ai/) | windows/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [AWS EC2 (Windows Server)](https://aws.amazon.com/ec2/pricing/on-demand/) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; spot: needs opt-in (spot) |
| - | [AWS EC2 Mac (Dedicated Host)](https://aws.amazon.com/ec2/instance-types/mac/) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Host split into 2 macOS VMs (Apple SLA cap), per-VM price: needs opt-i |
| - | [AWS Lambda](https://aws.amazon.com/lambda/pricing/) | hyperscaler/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Pay-as-you-go: sessions capped at 0.25 h; $6.87/mo free credit; session cap 0.25 h, needs restarts |
| - | [Azure Pipelines](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/) | paas/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Microsoft-hosted parallel jobs ($40 each/month, unlimited minutes): needs opt-in; session cap 6 h, needs restarts; egress unpublished |
| - | [Azure Virtual Machines (Windows Server)](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Azure Spot VM (representative East US): needs opt-in (spot) |
| - | [Baseten](https://docs.baseten.co/deployment/resources) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: T4, serverless (×1): needs opt-in (alt); L4, serverless (×1): needs opt-in (alt); egress unpublished |
| - | [Bright Data Browser API](https://brightdata.com/pricing/scraping-browser) | browser/- | $0 | $0 | $0 | $0 | $0 | $0 | unpriced: no published compute rate; browser product, bandwidth-metered; no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| - | [Brimble Sandboxes](https://brimble.io/pricing) | agent-sandbox/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; session cap 6 h, needs restarts; egress unpublished |
| - | [BrowserAct](https://www.browseract.com/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [BuildJet](https://buildjet.com/for-github-actions) | dev-env/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Butter](https://butter.dev) | agent-sandbox/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Bytebot](https://www.bytebot.ai/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Self-hosted open-source Docker desktop agent: needs opt-in (alt); egress unpublished |
| - | [Capy](https://capy.ai) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Per-thread VM, billed hourly by size while awake: needs opt-in (alt); egress unpublished |
| - | [Caution](https://caution.co/pricing.html) | paas/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Fully managed enclave: needs opt-in (sales); Managed enclave in own AWS: needs o; egress unpublished |
| - | [Cedana](https://cedana.com/) | other (checkpoint/restore software; not a compute provider)/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Cerebrium](https://cerebrium.ai/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Interruptible: needs opt-in (spot, alt); Protected compute: needs opt-in (alt); ; egress unpublished |
| - | [Chronicle Labs](https://chronicle-labs.com) | agent-sandbox/qemu-kvm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Cirrus Runners](https://cirrus-runners.app/pricing/) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Claude Managed Agents](https://platform.claude.com/docs/en/about-claude/pricing#claude-managed-agents-pricing) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Cloud sandbox session runtime ($0.08 per running session-hour, flat): needs opt-; egress unpublished |
| - | [Claw 2 Agent](https://claw2agent.com/pricing) | agent-sandbox/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [CloudAxis](https://cloudaxis.ai/pricing/) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [CloudBrowser AI](https://cloudbrowser.ai/) | browser/container | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Cloudflare Workers for Platforms](https://developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/reference/pricing/) | paas/isolate | - | - | - | - | - | - | not priceable at 10 h/d x30: needs 2 vCPU, largest option is 1; max 1 vCPU per sandbox |
| - | [cloudrouter (Manaflow)](https://cloudrouter.dev) | agent-sandbox/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Clusy](https://www.clusy.io/pricing) | dev-env/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: On-demand: needs opt-in (alt); egress unpublished |
| - | [Coder](https://coder.com/pricing) | dev-env/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Self-hosted workspaces: needs opt-in (alt); egress unpublished |
| - | [Comfy Deploy](https://app.comfydeploy.com/pricing) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Computer Use Cloud (computeruse.run)](https://computeruse.run/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [ComputerUse.space](https://computeruse.space/) | agent-sandbox/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [CoreWeave](https://www.coreweave.com/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: B300, spot (×8 node): needs opt-in (spot); B200, spot (×8 node): needs opt-in (s; egress unpublished |
| - | [Cua Fleet (Windows Server)](https://cua.ai/pricing) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Cua Cloud macOS (separate product): needs opt-in (sales); egress unpublished |
| - | [Cube Computer](https://cube.computer/) | dev-env/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Per-second VM sizes (50 GB disk): needs opt-in (promo); egress unpublished |
| - | [Cyberdesk](https://www.cyberdesk.io) | windows/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Dagger](https://dagger.io) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); Cloud Engines (hosted, ear; egress unpublished |
| - | [Datalayer Runtimes](https://datalayer.io/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Daytona (Windows sandboxes)](https://www.daytona.io/pricing) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; egress unpublished |
| - | [Dexto](https://www.dexto.ai/docs/models/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [DigitalOcean GPU Droplets](https://www.digitalocean.com/pricing/gpu-droplets) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: B300, reserved: needs opt-in (sales, commit); H200, reserved: needs opt-in (sale |
| - | [Dockup](https://getdockup.com/) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Eventual](https://www.eventual.ai/) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Daft open-source self-hosted engine: needs opt-in (alt); Eventual robotics data ; egress unpublished |
| - | [Expanse](https://expanse.sh) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [fal](https://fal.ai/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: B300, reserved: needs opt-in (sales); B200, reserved: needs opt-in (sales); H200; egress unpublished |
| - | [Ferr](https://ferr.dev/) | browser/container | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Flow Swiss Mac Bare Metal](https://doc.flow.swiss/platform/pricing/mac-bare-metal) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Mac split into 2 macOS VMs (Apple SLA cap), per-VM price: needs opt-in |
| - | [FlowDeploy](https://flowdeploy.com) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Fluidstack](https://fluidstack.io/) | gpu-cloud/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: H100, reserved: needs opt-in (alt, sales); H200, reserved: needs opt-in (alt, sa; egress unpublished |
| - | [Gemini API code execution](https://ai.google.dev/gemini-api/docs/code-execution) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Built-in code execution tool (token-billed only): needs opt-in (alt); session cap 0.00833333 h, needs restarts; egress unpublished |
| - | [GitHub Copilot cloud sandboxes](https://docs.github.com/en/billing/concepts/product-billing/cloud-and-local-sandboxes) | hyperscaler/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Cloud sandbox (copilot --cloud), per-second meters: needs opt-in (alt); egress unpublished |
| - | [Google Agent Platform Sandbox (Code Execution / Shell / Computer Use)](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Usage based: no internet access; egress unpublished |
| - | [Google Colab](https://developers.google.com/colab) | dev-env/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: On-demand: needs opt-in (alt); Colab Enterprise (GCP, us-central1): needs opt-in; session cap 12 h, needs restarts; egress unpublished |
| - | [Google Compute Engine (Windows Server)](https://cloud.google.com/compute/disks-image-pricing#windows_server_pricing) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [Google Compute Engine GPU VMs](https://cloud.google.com/products/compute/pricing/accelerator-optimized) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: a2-highgpu-1g, spot (×1): needs opt-in (spot); a2-ultragpu-1g, spot (×1): needs ; egress unpublished |
| - | [Green Mini host](https://portal.greenmini.host/checkout/order) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [H Company / Surfer / H Agents API](https://www.hcompany.ai/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Halluminate](https://halluminate.ai/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Hatchet](https://hatchet.run) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Heroic Labs](http://heroiclabs.com) | paas/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Heroku](https://www.heroku.com/pricing/) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Cedar Common Runtime dynos (Basic/Standard shared; Performance dedicated): needs; egress unpublished |
| - | [Hetzner GPU servers](https://www.hetzner.com/dedicated-rootserver/matrix-gpu/) | gpu-cloud/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: GEX45 Blackwell SFF 24GB, on-demand (×1): needs opt-in (alt); GEX131 Blackwell M |
| - | [Hoplite](https://hoplite.sh) | agent-sandbox/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [HostMyApple](https://hostmyapple.com/mac-vps-hosting) | macos/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [HUD](https://www.hud.ai/) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); HUD-hosted on Modal (CPU/GPU profiles): need; egress unpublished |
| - | [Hugging Face Jobs (hf-sandbox backend)](https://huggingface.co/docs/hub/en/jobs-pricing) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: On-demand: needs opt-in (alt); GPU: Nvidia T4: needs opt-in (alt); GPU: Nvidia L; egress unpublished |
| - | [HumanLayer](https://humanlayer.com) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Hyperbolic](https://www.hyperbolic.ai/marketplace) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Private Cloud (single-tenant, >1 year contract): needs opt-in (sales) |
| - | [Hyrex](https://www.hyrex.io) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Isle](https://www.tryisle.com/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); egress unpublished |
| - | [Jamsocket](https://jamsocket.com) | agent-sandbox/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: On-demand: needs opt-in (alt); session cap 12 h, needs restarts; egress unpublished |
| - | [Kasm Workspaces](https://kasm.com/community-edition) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Self-hosted Workspaces licence (Starter: $10/user or $20/concurrent session): ne; egress unpublished |
| - | [KubeSail](https://kubesail.com) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Lambda](https://lambda.ai/pricing) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: H100, reserved (×16 node): needs opt-in (alt, sales); H100, reserved (×64 node): |
| - | [LangSmith Sandboxes](https://www.langchain.com/pricing) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Developer: reach only an allowlist (package registries, git, AI APIs); Plus (one; egress unpublished |
| - | [Lapdev](https://lap.dev/pricing/) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); egress unpublished |
| - | [Limrun](https://lim.run) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [MacinCloud](https://www.macincloud.com/pages/dedicated.html) | macos/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Pay-as-You-Go by the day (shared managed Mac, no admin): needs opt-in ; egress unpublished |
| - | [MacStadium](https://www.macstadium.com/pricing) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Orka macOS VM cluster (Mac Cloud Compute), contact sales: needs opt-in |
| - | [Magnitude](https://magnitude.dev/) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Manufact](https://manufact.com) | paas/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt) |
| - | [Manus Cloud Computer](https://help.manus.im/en/articles/15392078-understanding-cloud-computer-plans-and-billing) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: commit regime only covers always-on instances; egress unpublished |
| - | [Maritime](https://maritime.sh/pricing) | agent-sandbox/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [Mastra](https://mastra.ai) | paas/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); Mastra Platform Starter CP |
| - | [Metorial](https://metorial.com) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Microsoft Azure GPU VMs](https://prices.azure.com/api/retail/prices) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Standard_NC24ads_A100_v4, spot (×1): needs opt-in (spot); Standard_ND96amsr_A100 |
| - | [Microsoft Dev Box (closed to new customers; retiring 2028-09-18)](https://azure.microsoft.com/en-us/products/dev-box/) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Microsoft Foundry hosted agents (East US)](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/) | hyperscaler/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: East US hosted agent compute: needs opt-in (alt); EU hosted agent compute (Swede; egress unpublished |
| - | [Minicor](https://minicor.com) | windows/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [MiniMax Agent hosting / developer API scope](https://platform.minimax.io/docs/llms.txt) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Hosted agent environment quote/spec unverified: needs opt-in (alt); egress unpublished |
| - | [Mistral Compute / AI Cloud](https://mistral.ai/products/aicloud/) | gpu-cloud/bare-metal | - | - | - | - | - | - | not priceable at 10 h/d x30: Dedicated AI capacity: needs opt-in (sales, commit); egress unpublished |
| - | [Modelence](https://modelence.com) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: App containers: needs opt-in (alt); egress unpublished |
| - | [Moonshot Kimi Hosted Agents sandbox](https://platform.kimi.com/docs/pricing/hosted-agents.md) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Hosted Agents 1C/1G sandbox: needs opt-in (alt, sales); egress unpublished |
| - | [Nebius ConTree (Token Factory Sandboxes)](https://tokenfactory.nebius.com/sandboxes/about) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; session cap 1 h, needs restarts; egress unpublished |
| - | [Nextmv](https://nextmv.io) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); session cap 0.25 h, needs restarts; egress unpublished |
| - | [Nodus Compute](https://www.nodus-compute.ai/pricing/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; egress unpublished |
| - | [OakHost](https://www.oakhost.com/mac-mini-hosting) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; "Try macOS for a week" (M2, 8+ GB), one-off 7 days: needs opt-in (prom |
| - | [Okteto](https://okteto.com) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [OmniRun](https://omnirun.io/pricing) | agent-sandbox/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: no preset with ≥2 vCPU and ≥4 GiB; egress unpublished |
| - | [OneCLI](https://onecli.sh) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [OpenAGI / Lux](https://developer.agiopen.org/docs/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Bring your own computer: needs opt-in (alt); egress unpublished |
| - | [OpenAI Containers (Code Interpreter / Hosted Shell)](https://developers.openai.com/api/docs/pricing) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: API pay as you go: reach only an allowlist (package registries, git, AI APIs); C; egress unpublished |
| - | [OpenHands Remote Sandbox / Cloud](https://docs.openhands.dev/openhands/usage/sandboxes/remote) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Managed OpenHands Cloud: needs opt-in (alt); Remote agent server on own infrastr; session cap 12 h, needs restarts; egress unpublished |
| - | [PaperPod](https://www.paperpod.dev/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); egress unpublished |
| - | [Party](https://party.build) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Pipekit](https://pipekit.io/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Pipeshift](https://pipeshift.com) | gpu-cloud/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Playgent](https://useplaygent.com) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Ploomber](https://ploomber.io/) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [PoplarML](http://poplarml.com) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Porter](https://porter.run) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); Porter Sandboxes (AWS, in your own account):; egress unpublished |
| - | [Reflex](https://reflex.dev/pricing/) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Hosted Python apps: needs opt-in (alt); egress unpublished |
| - | [Refresh](https://www.refresh.dev) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Release](https://release.com/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Enterprise BYOC: needs opt-in (sales, alt); egress unpublished |
| - | [RentaMac (rentamac.io)](https://rentamac.io/pricing) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [Replicate](https://replicate.com/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Private Cog CPU model: needs opt-in (alt); T4, serverless (×1): needs opt-in (al; egress unpublished |
| - | [Replit](https://docs.replit.com/billing/deployment-pricing) | paas/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Autoscale / Scheduled deployment (compute units while serving or running): needs |
| - | [Rescale](https://rescale.com) | gpu-cloud/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); no published per-resource ; egress unpublished |
| - | [Revyl](https://www.revyl.com) | macos/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Riza Code Interpreter](https://riza.io/pricing) | agent-sandbox/isolate | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; session cap 0.25 h, needs restarts |
| - | [Run Cloud](https://docs.run.cloud/sandboxes/index.md) | agent-sandbox/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; $15/mo free credit; egress unpublished |
| - | [RunAnywhere](https://www.runanywhere.ai/) | inference-api/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Wally hosted token-billed inference preview (not an arbitrary-code VM): needs op; egress unpublished |
| - | [RunKit](https://runkit.com/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Scaleway Apple silicon (Mac mini)](https://www.scaleway.com/en/pricing/apple-silicon/) | macos/dedicated-host | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [Scaleway GPU instances](https://www.scaleway.com/en/pricing/gpu/) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no priceable regime |
| - | [ScitiX Agent Sandbox](https://scitix.github.io/Agent-Sandbox/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Self-hosted runtime + externally billed clusters: needs opt-in (alt); Self-hoste; egress unpublished |
| - | [Scraping Bee](https://www.scrapingbee.com/pricing/) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Browser API request (not time-priced): needs opt-in (alt); session cap 0.039 h, needs restarts; egress unpublished |
| - | [SeaCloudAI Sandbox](https://sandbox-gateway.cloud.seaart.ai) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; egress unpublished |
| - | [Self-hosted bare-metal sandbox fleet (hardware floor)](https://www.hetzner.com/dedicated-rootserver/ax42/) | self-host/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Hetzner AX42 / 50% occupancy: needs opt-in (alt); Hetzner AX42 / 70% occupancy: ; egress unpublished |
| - | [Server4Agent](https://www.server4agent.com/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); egress unpublished |
| - | [SF Tensor](https://sf-tensor.com) | gpu-cloud/gvisor | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt, sales); egress unpublished |
| - | [Shadeform](https://www.shadeform.ai/) | gpu-cloud/dedicated-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Current applicable tariff unverified: price not published; Reserved commitments:; egress unpublished |
| - | [Shuttle](https://www.shuttle.dev) | paas/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Sieve](https://sievedata.com/) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Signadot](https://www.signadot.com/) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Skyhook](https://skyhook.io) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Skyvern](https://www.skyvern.com/pricing) | browser/container | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; session cap 6 h, needs restarts; egress unpublished |
| - | [Smooth](https://www.smooth.sh/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; egress unpublished |
| - | [Specific](https://specific.dev/pricing) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Hosted services: needs opt-in (alt) |
| - | [StackBlitz WebContainers](https://stackblitz.com/pricing) | dev-env/v8-isolate | - | - | - | - | - | - | not priceable at 10 h/d x30: Browser-local runtime licence: needs opt-in (alt); egress unpublished |
| - | [Strong Compute](https://strongcompute.com) | finops (GPU/LLM spend-management SaaS; legacy managed GPU training platform 'ISC')/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt) |
| - | [Tabstack](https://tabstack.ai/) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); egress unpublished |
| - | [Tart + Orchard (Cirrus Labs)](https://tart.run/licensing/) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: software licence only - bring your own Macs; egress unpublished |
| - | [Teclada](https://www.teclada.com/) | dev-env/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Tencent Cloud CubeSandbox](https://github.com/TencentCloud/CubeSandbox) | agent-sandbox/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; Self-hosted CubeSandbox (Apache-2.0): needs opt-; egress unpublished |
| - | [Tencent Cloud SCF](https://cloud.tencent.com/document/product/583/17299) | hyperscaler/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Event function: needs opt-in (alt); Web function: needs opt-in (alt); Provisione |
| - | [TensorDock](https://www.tensordock.com/) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: H100, spot: needs opt-in (spot); A100, spot: needs opt-in (spot); RTX4090, spot: |
| - | [TensorPool](https://tensorpool.dev) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Texel.ai](https://texel.ai) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Thunder Compute](https://www.thundercompute.com/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Reserved clusters (8-512+ GPUs, fixed term): needs opt-in (sales) |
| - | [Tilde.run (discontinued)](https://lakefs.io/blog/we-recently-shut-down-tilde-run/) | agent-sandbox/container | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Tilion](https://tilion.com/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: no published per-resource rate; session cap 12 h, needs restarts; egress unpublished |
| - | [Tinfoil](https://tinfoil.sh) | paas/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); Confidential GPU enclave (; egress unpublished |
| - | [TinyFish](https://www.tinyfish.ai/pricing) | browser/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt);; egress unpublished |
| - | [Together AI](https://www.together.ai/pricing) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: H100 HGX/SXM, spot (×8 node): needs opt-in (spot); H200 HGX/SXM, spot (×8 node): |
| - | [Trainy](https://trainy.ai/) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Trigger.dev](https://trigger.dev/pricing) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Managed tasks: needs opt-in (alt); egress unpublished |
| - | [Unikraft Cloud](https://unikraft.com/pricing) | agent-sandbox/firecracker | $0 | $0 | $0 | $0 | $0 | $0 | unpriced: no published compute rate; flat pool, no per-shape rate; disk beyond 0 GiB: price unknown; egress unpublished |
| - | [use.computer](https://use.computer/) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; egress unpublished |
| - | [Vast.ai](https://github.com/vast-ai/docs/blob/main/guides/pricing.mdx) | gpu-cloud/container | - | - | - | - | - | - | not priceable at 10 h/d x30: RTX4090, on-demand: needs opt-in (alt); RTX5090, on-demand: needs opt-in (alt);  |
| - | [Veertu Anka Build Cloud](https://docs.veertu.com/anka/licensing/) | macos/apple-vm | - | - | - | - | - | - | not priceable at 10 h/d x30: Anka Build licence on your own Macs (contact sales): needs opt-in (alt, sales); ; egress unpublished |
| - | [Vibrant Labs](https://vibrantlabs.com/) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native service: needs opt-in (alt); egress unpublished |
| - | [Voltage Park](https://www.voltagepark.com/pricing) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: HGX H100 on-demand InfiniBand (8+ GPUs): needs opt-in (sales) |
| - | [Vultr Cloud Compute (Windows Server)](https://docs.vultr.com/support/platform/billing/is-a-windows-license-included-in-the-monthly-price) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux |
| - | [Vultr Cloud GPU](https://api.vultr.com/v2/plans?type=vcg) | gpu-cloud/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: vcg-a16-2c-8g-2vram, on-demand (×1): needs opt-in (alt); vcg-a16-2c-16g-4vram, o; egress unpublished |
| - | [Wasmer](https://wasmer.io/pricing) | paas/isolate | - | - | - | - | - | - | not priceable at 10 h/d x30: WebAssembly Edge: needs opt-in (alt) |
| - | [webapp.io](https://webapp.io) | dev-env/- | - | - | - | - | - | - | not priceable at 10 h/d x30: discontinued / closed to new customers; egress unpublished |
| - | [Windmill](https://www.windmill.dev/pricing) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Cloud Team execution credits: needs opt-in (alt); Dedicated Cloud Enterprise: ne; egress unpublished |
| - | [Windows 365 Cloud PC (Business / Enterprise)](https://www.microsoft.com/en-us/windows-365/business/compare-plans-pricing) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; Windows 365 Enterprise GPU Standard: needs opt-in (sales); Windows 365; egress unpublished |
| - | [Windows 365 for Agents](https://learn.microsoft.com/en-us/windows-365/agents/pricing-paygo-always-available) | windows/vm | - | - | - | - | - | - | not priceable at 10 h/d x30: no Linux; egress unpublished |
| - | [YepCode Run](https://yepcode.io/pricing/) | paas/firecracker | - | - | - | - | - | - | not priceable at 10 h/d x30: Process execution on Starter (per-second Yeps): needs opt-in (alt); Process exec; session cap 12 h, needs restarts; egress unpublished |
| - | [Zeabur](https://zeabur.com/pricing) | paas/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Bring or buy server; compute separately billed: needs opt-in (alt) |
| - | [Zenrows Browser Sessions](https://www.zenrows.com/pricing) | browser/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Free: regime not sold on this plan; Build B1: regime not sold on this plan; Buil; session cap 0.25 h, needs restarts |
| - | [Zhipu Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview.md) | agent-sandbox/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Managed Agent sandbox, temporary free runtime fee: needs opt-in (alt); egress unpublished |
| - | [Zibra Labs](https://zibralabs.ai/) | gpu-cloud/- | - | - | - | - | - | - | not priceable at 10 h/d x30: Native product; see regime notes: needs opt-in (alt); egress unpublished |
| - | [Zo Computer](https://www.zo.computer/pricing) | dev-env/container | - | - | - | - | - | - | not priceable at 10 h/d x30: Zo Basic subscription, one always-on computer (4 cores / 32 GB) - $18/mo: needs ; egress unpublished |

## Sandbox & container providers only (`agent-sandbox` category)

80 of the 179 priceable providers are sandbox products. Same shape and sort as above; hyperscaler VMs, PaaS and CI runners are excluded here but present in the full table.

| # | Provider | Type | 1 h | 10 h | 1 day | 1 week | 10 h/d x30 | 24/7 x30 | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.0085 | $0.085 | $0.204 | $1.43 | $2.55 | $6.12 | egress unpublished |
| 2 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.014 | $0.137 | $0.329 | $2.30 | $4.11 | $9.86 | egress unpublished |
| 3 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $0 | $0 | $0.984 | $5.68 | $20.64 | $5/mo free credit |
| 4 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $0.020 | $0.200 | $0.480 | $3.36 | $6.00 | $14.40 | egress unpublished |
| 5 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $0.022 | $0.218 | $0.524 | $3.67 | $6.55 | $15.72 | Medium only: runtime fixes 4 vCPU / 4 GiB |
| 6 | [Upstash Box](https://upstash.com/pricing/box) | agent-sandbox/container | $0.103 | $1.03 | $2.47 | $8.46 | $8.82 | $9.97 | egress unpublished; flat pool, billed whether used or not |
| 7 | [Together Code Sandbox](https://www.together.ai/pricing) | agent-sandbox/firecracker | $0.030 | $0.300 | $0.720 | $5.04 | $9.00 | $21.60 | no machine size published, not shape-comparable; egress unpublished |
| 8 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $0 | $0 | $5.09 | $13.01 | $38.21 | $5/mo free credit; egress unpublished |
| 9 | [tama](https://tama.computer/) | agent-sandbox/vm | $0.045 | $0.454 | $1.09 | $7.63 | $13.62 | $32.70 | egress unpublished |
| 10 | [Coasty](https://coasty.ai/pricing) | agent-sandbox/vm | $0.050 | $0.500 | $1.20 | $8.40 | $15.00 | $30.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 11 | [Mosaic Sandbox](https://sandbox.mosaicos.com/) | agent-sandbox/firecracker | $0.050 | $0.500 | $1.20 | $8.40 | $15.00 | $36.00 | egress unpublished |
| 12 | [machine0](https://machine0.io/) | agent-sandbox/vm | $0.052 | $0.520 | $1.25 | $8.74 | $15.60 | $37.44 |  |
| 13 | [Runtime (withruntime.com)](https://withruntime.com/pricing) | agent-sandbox/firecracker | $0.055 | $0.550 | $1.32 | $9.24 | $16.50 | $39.60 |  |
| 14 | [Railway](https://railway.com/pricing) | agent-sandbox/vm | $5.00 | $5.00 | $5.00 | $9.34 | $16.68 | $40.02 | disk beyond 0 GiB: price unknown; $5/mo minimum, fee is a usage credit |
| 15 | [Alibaba Cloud Agent Sandbox / FC / AgentRun](https://help.aliyun.com/zh/agent-sandbox/product-overview/billing-overview) | agent-sandbox/- | $0.056 | $0.562 | $1.35 | $9.44 | $16.86 | $40.46 | egress unpublished |
| 16 | [Celesto Cloud](https://celesto.ai/pricing) | agent-sandbox/vm | $0.060 | $0.600 | $1.44 | $10.08 | $18.00 | $43.20 | egress unpublished |
| 17 | [Sandbox0](https://sandbox0.ai/pricing) | agent-sandbox/gvisor | $0.060 | $0.606 | $1.45 | $10.17 | $18.16 | $43.59 |  |
| 18 | [UCloud Agent Sandbox](https://astraflow.ucloud.cn/docs/agent-sandbox) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | $19.31 | $46.35 | disk beyond 10 GiB: price unknown; egress unpublished |
| 19 | [PPIO Agent Sandbox](https://ppio.com/docs/sandbox/pricing.md) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | $19.31 | $46.35 | session cap 1 h, needs restarts; egress unpublished |
| 20 | [Volcano Engine AgentKit / veFaaS sandbox](https://docs.volcengine.com/docs/agentkit/Billing_items?lang=zh) | agent-sandbox/vm | $0.065 | $0.653 | $1.57 | $10.98 | $19.60 | $47.05 |  |
| 21 | [boat.dev](https://docs.boat.dev/pricing) | agent-sandbox/vm | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | $20.00 | disk beyond 12 GiB: price unknown; $20/mo minimum, fee is a usage credit |
| 22 | [OpenComputer](https://opencomputer.dev/sandboxes) | agent-sandbox/vm | $0.378 | $3.78 | $9.07 | $20.00 | $20.00 | $92.16 | disk beyond 16 GiB: price unknown; egress unpublished |
| 23 | [Northflank Sandboxes](https://northflank.com/pricing) | agent-sandbox/vm | $0.071 | $0.706 | $1.69 | $11.86 | $21.18 | $50.84 |  |
| 24 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $0 | $0 | $0 | $4.13 | $21.81 | $78.07 | $18.38/mo free credit |
| 25 | [Sprites (Fly.io)](https://fly.io/pricing) | agent-sandbox/firecracker | $0.083 | $0.826 | $1.98 | $13.87 | $24.76 | $59.43 |  |
| 26 | [smol machines](https://smolmachines.com/pricing) | agent-sandbox/vm | $0.084 | $0.844 | $2.03 | $14.18 | $25.32 | $60.77 |  |
| 27 | [orkestr Sandboxes](https://orkestr.eu/sandboxes) | agent-sandbox/vm | $0.085 | $0.853 | $2.05 | $14.34 | $25.60 | $61.44 | disk beyond 0 GiB: price unknown; egress unpublished |
| 28 | [Buddy Sandboxes](https://buddy.works/pricing) | agent-sandbox/vm | $0 | $0.736 | $1.98 | $14.73 | $26.43 | $63.64 | egress unpublished |
| 29 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $0 | $0 | $0 | $1.91 | $26.98 | $107 | $30/mo free credit |
| 30 | [Sandbox as a Service](https://sandbox-as-a-service.com/pricing) | agent-sandbox/vm | $0.090 | $0.900 | $2.16 | $15.12 | $27.00 | $64.80 | egress unpublished |
| 31 | [Prime Intellect Sandboxes](https://www.primeintellect.ai/sandboxes) | agent-sandbox/vm | $0.094 | $0.940 | $2.26 | $15.79 | $28.20 | $67.68 | egress unpublished |
| 32 | [Koyeb Sandboxes](https://www.koyeb.com/pricing) | agent-sandbox/vm | $29.00 | $29.00 | $29.00 | $29.00 | $29.00 | $39.74 |  |
| 33 | [Alibaba Cloud AgentBay](https://www.alibabacloud.com/help/en/agentbay/product-overview/agentbay-billing-instructions) | agent-sandbox/container | $0.099 | $0.992 | $2.38 | $16.67 | $29.76 | $71.42 | disk beyond 0 GiB: price unknown |
| 34 | [Morph Cloud](https://cloud.morph.so/web/subscribe) | agent-sandbox/vm | $0.100 | $1.00 | $2.40 | $16.80 | $30.00 | $62.00 | disk beyond 16 GiB: price unknown; egress unpublished |
| 35 | [Isorun](https://docs.isorun.ai/getting-started/pricing) | agent-sandbox/vm | $0.110 | $1.10 | $2.65 | $18.55 | $33.13 | $79.52 |  |
| 36 | [Novita AI Agent Sandbox](https://docs.novita.ai/guides/sandbox-pricing) | agent-sandbox/firecracker | $0.117 | $1.17 | $2.80 | $19.60 | $34.99 | $83.98 | egress unpublished |
| 37 | [CreateOS Sandbox (NodeOps)](https://createos.sh/products/sandbox) | agent-sandbox/firecracker | $10.00 | $10.00 | $10.00 | $20.47 | $36.56 | $87.74 | $10/mo minimum, fee is a usage credit |
| 38 | [Collimate](https://collimate.ai/pricing) | agent-sandbox/firecracker | $0.128 | $1.28 | $3.07 | $21.50 | $38.40 | $92.16 | disk beyond 0 GiB: price unknown |
| 39 | [Docker Cloud Sandboxes](https://www.docker.com/blog/introducing-cloud-sandboxes-start-on-your-laptop-finish-in-the-cloud/) | agent-sandbox/vm | $0.140 | $1.40 | $3.36 | $23.52 | $42.00 | $101 |  |
| 40 | [Tencent Cloud Agent Runtime — Agent Sandbox](https://cloud.tencent.com/document/product/1814/133249) | agent-sandbox/- | $0.142 | $1.42 | $3.41 | $23.88 | $42.64 | $102 | egress unpublished |
| 41 | [Cloudflare Sandbox SDK / Containers](https://developers.cloudflare.com/containers/platform/pricing/) | agent-sandbox/vm | $5.00 | $5.59 | $7.42 | $26.29 | $43.59 | $98.62 |  |
| 42 | [Deno Sandbox](https://deno.com/deploy/pricing) | agent-sandbox/firecracker | $20.00 | $20.00 | $20.00 | $23.13 | $44.25 | - | disk beyond 10 GiB: price unknown; session cap 0.5 h, needs restarts |
| 43 | [Dedalus Labs](https://www.dedaluslabs.ai/pricing) | agent-sandbox/vm | $0.151 | $1.51 | $3.62 | $25.37 | $45.31 | $109 | egress unpublished |
| 44 | [MIOSA](https://miosa.ai/pricing) | agent-sandbox/firecracker | $0.155 | $1.55 | $3.72 | $26.07 | $46.56 | $112 | disk beyond 10 GiB: price unknown |
| 45 | [boxd](https://boxd.sh/pricing) | agent-sandbox/vm | $0.156 | $1.56 | $3.75 | $26.28 | $46.92 | $113 | egress unpublished |
| 46 | [microsandbox](https://microsandbox.dev/pricing) | agent-sandbox/vm | $49.00 | $49.00 | $49.00 | $49.00 | $49.00 | $112 | egress unpublished |
| 47 | [Shardflux](https://shardflux.dev/#pricing) | agent-sandbox/firecracker | $9.00 | $9.00 | $9.00 | $12.04 | $49.00 | $105 | egress unpublished |
| 48 | [E2B](https://e2b.dev/pricing) | agent-sandbox/firecracker | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | egress unpublished |
| 49 | [Leap0](https://leap0.dev/) | agent-sandbox/firecracker | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 10 GiB: price unknown; session cap 8 h, needs restarts; egress unpublished |
| 50 | [Omnara](https://www.omnara.com/pricing) | agent-sandbox/- | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 0 GiB: price unknown; egress unpublished |
| 51 | [OpenReward Sandboxes](https://openreward.ai/pricing) | agent-sandbox/container | $0.166 | $1.66 | $3.97 | $27.82 | $49.68 | $119 | disk beyond 0 GiB: price unknown; egress unpublished |
| 52 | [Daytona](https://www.daytona.io/pricing) | agent-sandbox/container | $0.167 | $1.67 | $4.01 | $28.09 | $50.17 | $120 | egress unpublished |
| 53 | [Tenki Sandbox](https://tenki.cloud/pricing) | agent-sandbox/vm | $0.167 | $1.67 | $4.01 | $28.09 | $50.17 | $120 | egress unpublished |
| 54 | [Hopx](https://hopx.ai/pricing) | agent-sandbox/firecracker | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 55 | [Runta](https://runta.com/pricing/) | agent-sandbox/vm | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 56 | [Superserve](https://superserve.ai/pricing) | agent-sandbox/firecracker | $0.168 | $1.68 | $4.03 | $28.18 | $50.33 | $121 | egress unpublished |
| 57 | [Declaw](https://docs.declaw.ai/platform/billing) | agent-sandbox/firecracker | $0.169 | $1.69 | $4.05 | $28.33 | $50.58 | $121 | egress unpublished |
| 58 | [Blaxel](https://blaxel.ai/pricing) | agent-sandbox/firecracker | $0.169 | $1.69 | $4.05 | $28.37 | $50.67 | $122 |  |
| 59 | [Cua Fleet](https://cua.ai/pricing) | agent-sandbox/vm | $0.178 | $1.78 | $4.28 | $29.99 | $53.55 | $129 | disk beyond 0 GiB: price unknown; egress unpublished |
| 60 | [Arker](https://arker.ai/docs/pricing) | agent-sandbox/vm | $0.188 | $1.88 | $4.51 | $31.54 | $56.32 | $135 | egress unpublished |
| 61 | [Vercel Sandbox](https://vercel.com/docs/sandbox/pricing) | agent-sandbox/firecracker | $20.00 | $20.00 | $20.00 | $35.75 | $63.84 | $153 | $20/mo minimum, fee is a usage credit |
| 62 | [Beam](https://www.beam.cloud/pricing) | agent-sandbox/gvisor | $0.227 | $2.27 | $5.45 | $38.16 | $68.15 | $164 | disk beyond 0 GiB: price unknown |
| 63 | [PandaStack](https://www.pandastack.ai/pricing/) | agent-sandbox/firecracker | $0 | $0 | $0.650 | $36.95 | $70.23 | $176 |  |
| 64 | [OpenPond Cloud Sandboxes](https://openpond.ai/pricing) | agent-sandbox/firecracker | $0.238 | $2.38 | $5.70 | $39.92 | $71.28 | $171 | disk beyond 10 GiB: price unknown; egress unpublished |
| 65 | [AgentComputer](https://agentcomputer.ai/pricing) | agent-sandbox/firecracker | $0.259 | $2.59 | $6.21 | $43.45 | $77.60 | $186 | egress unpublished |
| 66 | [Rivet (Actors & agentOS)](https://rivet.dev/pricing/) | agent-sandbox/- | $20.00 | $20.00 | $20.00 | $48.32 | $86.29 | $207 |  |
| 67 | [Islo](https://islo.dev/pricing) | agent-sandbox/vm | $0.314 | $3.14 | $7.54 | $52.75 | $94.20 | $226 | egress unpublished |
| 68 | [Runloop](https://www.runloop.ai/pricing) | agent-sandbox/vm | $0.324 | $3.24 | $7.77 | $54.37 | $97.09 | $233 | egress unpublished |
| 69 | [Orgo](https://www.orgo.ai/pricing) | agent-sandbox/vm | $99.00 | $99.00 | $99.00 | $99.00 | $99.00 | $99.00 | disk beyond 0 GiB: price unknown; egress unpublished; flat pool, billed whether used or not |
| 70 | [Amika](https://www.amika.dev/pricing) | agent-sandbox/vm | $0 | $0 | $3.99 | $57.90 | $107 | $265 | egress unpublished |
| 71 | [Huawei Cloud AgentArts](https://support.huaweicloud.com/price-agentarts/agentarts-price-pdf.pdf) | agent-sandbox/container | $0.397 | $3.97 | $9.53 | $66.74 | $119 | $286 |  |
| 72 | [Ellipsis](https://www.ellipsis.dev/pricing) | agent-sandbox/qemu-kvm | $0.457 | $4.57 | $10.96 | $76.73 | $137 | $329 | disk beyond 0 GiB: price unknown; session cap 1 h, needs restarts; egress unpublished |
| 73 | [InstaVM](https://instavm.io/pricing) | agent-sandbox/firecracker | $100 | $102 | $104 | $128 | $150 | $221 | egress unpublished |
| 74 | [Baponi](https://baponi.ai/pricing/) | agent-sandbox/container | $97.00 | $97.00 | $97.00 | $128 | $160 | $262 | session cap 1 h, needs restarts |
| 75 | [CodeSandbox SDK](https://codesandbox.io/docs/sdk/pricing) | agent-sandbox/firecracker | $170 | $170 | $170 | $171 | $191 | $253 | $5.944/mo free credit; egress unpublished |
| 76 | [Replicas](https://replicas.dev) | agent-sandbox/vm | $50.48 | $54.80 | $61.52 | $131 | $194 | $396 | egress unpublished |
| 77 | [Solari](https://docs.getsolari.com/pricing) | agent-sandbox/vm | $200 | $200 | $200 | $200 | $200 | $200 | disk beyond 4 GiB: price unknown; egress unpublished |
| 78 | [Tensorlake Sandboxes](https://www.tensorlake.ai/pricing) | agent-sandbox/firecracker | $250 | $250 | $250 | $250 | $250 | $250 | $250/mo minimum, fee is a usage credit |
| 79 | [StateSet Sandbox](https://sandbox.stateset.app/) | agent-sandbox/gvisor | $299 | $301 | $305 | $338 | $369 | $466 | disk beyond 0 GiB: price unknown; session cap 5 h, needs restarts |
| 80 | [Archil](https://archil.com/pricing) | agent-sandbox/vm | $500 | $500 | $501 | $528 | $553 | $631 | egress unpublished |

## All surveyed providers, cheapest first at each horizon

### 1 h — 179 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Amika](https://www.amika.dev/pricing) | agent-sandbox/vm | $0 | egress unpublished |
| 2 | [Anchor Browser](https://anchorbrowser.io/pricing) | browser/dedicated-vm | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 3 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 4 | [Blacksmith (GitHub Actions runners)](https://www.blacksmith.sh/pricing) | macos/vm | $0 | $12/mo free credit; egress unpublished |
| 5 | [Buddy Sandboxes](https://buddy.works/pricing) | agent-sandbox/vm | $0 | egress unpublished |
| 6 | [Buildkite hosted agents](https://buildkite.com/pricing) | macos/vm | $0 | session cap 8 h, needs restarts; egress unpublished |
| 7 | [CircleCI](https://circleci.com/pricing/price-list/) | macos/vm | $0 | $15/mo minimum, fee is a usage credit; session cap 5 h, needs restarts |
| 8 | [CloudCruise](https://cloudcruise.com/pricing) | browser/dedicated-vm | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 9 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $0 | $18.38/mo free credit |
| 10 | [GitHub Actions hosted runners](https://docs.github.com/en/billing/reference/actions-runner-pricing) | macos/vm | $0 | disk beyond 14 GiB: price unknown; session cap 6 h, needs restarts |
| 11 | [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | dev-env/vm | $0 |  |
| 12 | [GitLab.com hosted runners](https://docs.gitlab.com/ci/pipelines/compute_minutes/) | macos/vm | $0 | session cap 3 h, needs restarts; egress unpublished |
| 13 | [Google Cloud Build](https://cloud.google.com/build/pricing) | paas/vm | $0 | egress unpublished |
| 14 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0 | $5.22/mo free credit |
| 15 | [Hyperbeam](https://hyperbeam.com/) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 16 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $0 | $10/mo free credit |
| 17 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $5/mo free credit |
| 18 | [Kernel](https://www.onkernel.com/pricing) | browser/firecracker | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 19 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $0 | $30/mo free credit |
| 20 | [Opensteer](https://opensteer.com/pricing) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 21 | [PandaStack](https://www.pandastack.ai/pricing/) | agent-sandbox/firecracker | $0 |  |
| 22 | [Remote Browser](https://remote-browser.dev/pricing) | browser/container | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 23 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $5/mo free credit; egress unpublished |
| 24 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.0014 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 25 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.0085 | egress unpublished |

### 10 h — 179 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Amika](https://www.amika.dev/pricing) | agent-sandbox/vm | $0 | egress unpublished |
| 2 | [Anchor Browser](https://anchorbrowser.io/pricing) | browser/dedicated-vm | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 3 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 4 | [Blacksmith (GitHub Actions runners)](https://www.blacksmith.sh/pricing) | macos/vm | $0 | $12/mo free credit; egress unpublished |
| 5 | [Buildkite hosted agents](https://buildkite.com/pricing) | macos/vm | $0 | session cap 8 h, needs restarts; egress unpublished |
| 6 | [CircleCI](https://circleci.com/pricing/price-list/) | macos/vm | $0 | $15/mo minimum, fee is a usage credit; session cap 5 h, needs restarts |
| 7 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $0 | $18.38/mo free credit |
| 8 | [GitHub Actions hosted runners](https://docs.github.com/en/billing/reference/actions-runner-pricing) | macos/vm | $0 | disk beyond 14 GiB: price unknown; session cap 6 h, needs restarts |
| 9 | [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | dev-env/vm | $0 |  |
| 10 | [Google Cloud Build](https://cloud.google.com/build/pricing) | paas/vm | $0 | egress unpublished |
| 11 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0 | $5.22/mo free credit |
| 12 | [Hyperbeam](https://hyperbeam.com/) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 13 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $0 | $10/mo free credit |
| 14 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $5/mo free credit |
| 15 | [Kernel](https://www.onkernel.com/pricing) | browser/firecracker | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 16 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $0 | $30/mo free credit |
| 17 | [Opensteer](https://opensteer.com/pricing) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 18 | [PandaStack](https://www.pandastack.ai/pricing/) | agent-sandbox/firecracker | $0 |  |
| 19 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $5/mo free credit; egress unpublished |
| 20 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.014 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 21 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.085 | egress unpublished |
| 22 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $0.103 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 23 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $0.104 |  |
| 24 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.137 | egress unpublished |
| 25 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $0.148 |  |

### 1 day — 179 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Anchor Browser](https://anchorbrowser.io/pricing) | browser/dedicated-vm | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 2 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 3 | [Blacksmith (GitHub Actions runners)](https://www.blacksmith.sh/pricing) | macos/vm | $0 | $12/mo free credit; egress unpublished |
| 4 | [CircleCI](https://circleci.com/pricing/price-list/) | macos/vm | $0 | $15/mo minimum, fee is a usage credit; session cap 5 h, needs restarts |
| 5 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $0 | $18.38/mo free credit |
| 6 | [GitHub Actions hosted runners](https://docs.github.com/en/billing/reference/actions-runner-pricing) | macos/vm | $0 | disk beyond 14 GiB: price unknown; session cap 6 h, needs restarts |
| 7 | [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | dev-env/vm | $0 |  |
| 8 | [Google Cloud Build](https://cloud.google.com/build/pricing) | paas/vm | $0 | egress unpublished |
| 9 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0 | $5.22/mo free credit |
| 10 | [Hyperbeam](https://hyperbeam.com/) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 11 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $0 | $10/mo free credit |
| 12 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $5/mo free credit |
| 13 | [Kernel](https://www.onkernel.com/pricing) | browser/firecracker | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 14 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $0 | $30/mo free credit |
| 15 | [Opensteer](https://opensteer.com/pricing) | browser/- | $0 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 16 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $5/mo free credit; egress unpublished |
| 17 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.033 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 18 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.204 | egress unpublished |
| 19 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $0.247 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 20 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $0.250 |  |
| 21 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.329 | egress unpublished |
| 22 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $0.355 |  |
| 23 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $0.464 | disk beyond 0 GiB: price unknown |
| 24 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $0.480 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 25 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $0.480 | egress unpublished |

### 1 week — 179 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 2 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $0.038 | $10/mo free credit |
| 3 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0.144 | $5.22/mo free credit |
| 4 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.230 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 5 | [Hyperbeam](https://hyperbeam.com/) | browser/- | $0.560 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 6 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0.984 | $5/mo free credit |
| 7 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $1.43 | egress unpublished |
| 8 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $1.73 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 9 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $1.75 |  |
| 10 | [Modal](https://modal.com/pricing) | agent-sandbox/gvisor | $1.91 | $30/mo free credit |
| 11 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $2.30 | egress unpublished |
| 12 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $2.48 |  |
| 13 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $3.25 | disk beyond 0 GiB: price unknown |
| 14 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $3.36 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 15 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $3.36 | egress unpublished |
| 16 | [Anchor Browser](https://anchorbrowser.io/pricing) | browser/dedicated-vm | $3.41 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown |
| 17 | [UpCloud](https://upcloud.com/pricing/) | hyperscaler/vm | $3.50 |  |
| 18 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $3.67 | Medium only: runtime fixes 4 vCPU / 4 GiB |
| 19 | [Freestyle](https://www.freestyle.sh/pricing) | agent-sandbox/bare-metal-vm | $4.13 | $18.38/mo free credit |
| 20 | [Fly.io Machines](https://fly.io/pricing) | paas/firecracker | $4.25 |  |
| 21 | [OVHcloud Public Cloud](https://us.ovhcloud.com/public-cloud/prices/) | hyperscaler/vm | $4.30 |  |
| 22 | [Scaleway Instances](https://www.scaleway.com/en/pricing/virtual-instances/) | hyperscaler/vm | $4.36 | Stardust disk is billed on top of the instance rate |
| 23 | [Kamatera](https://www.kamatera.com/pricing/) | hyperscaler/vm | $4.60 |  |
| 24 | [Civo Compute](https://www.civo.com/pricing) | hyperscaler/vm | $5.00 |  |
| 25 | [Vultr Cloud Compute](https://www.vultr.com/pricing/) | hyperscaler/vm | $5.01 |  |

### 10 h/d x30 — 179 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.411 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 2 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $2.55 | egress unpublished |
| 3 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $3.09 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 4 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $3.12 |  |
| 5 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $3.60 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 6 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $4.11 | egress unpublished |
| 7 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $4.36 | $5.22/mo free credit |
| 8 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $4.44 |  |
| 9 | [netcup VPS](https://www.netcup.com/en/server/vps) | hyperscaler/vm | $5.03 | entry row is VPS Lite 1 (6-month min); VPS 500 is $8.51/mo; price is one month's rent at every horizon |
| 10 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $5.68 | $5/mo free credit |
| 11 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $5.80 | disk beyond 0 GiB: price unknown |
| 12 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $6.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 13 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $6.00 | egress unpublished |
| 14 | [UpCloud](https://upcloud.com/pricing/) | hyperscaler/vm | $6.25 |  |
| 15 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $6.55 | Medium only: runtime fixes 4 vCPU / 4 GiB |
| 16 | [Contabo](https://contabo.com/en-us/pricing/) | hyperscaler/vm | $6.60 | visible $4.40 is a 24-month intro, list is $6.60; price is one month's rent at every horizon |
| 17 | [Fly.io Machines](https://fly.io/pricing) | paas/firecracker | $7.58 |  |
| 18 | [OVHcloud Public Cloud](https://us.ovhcloud.com/public-cloud/prices/) | hyperscaler/vm | $7.68 |  |
| 19 | [Scaleway Instances](https://www.scaleway.com/en/pricing/virtual-instances/) | hyperscaler/vm | $7.78 | Stardust disk is billed on top of the instance rate |
| 20 | [InsForge (InstaCloud)](https://www.instacloud.com/pricing) | paas/vm | $7.92 | $10/mo free credit |
| 21 | [Kamatera](https://www.kamatera.com/pricing/) | hyperscaler/vm | $8.22 |  |
| 22 | [Upstash Box](https://upstash.com/pricing/box) | agent-sandbox/container | $8.82 | egress unpublished; flat pool, billed whether used or not |
| 23 | [Civo Compute](https://www.civo.com/pricing) | hyperscaler/vm | $8.93 |  |
| 24 | [Vultr Cloud Compute](https://www.vultr.com/pricing/) | hyperscaler/vm | $8.94 |  |
| 25 | [Together Code Sandbox](https://www.together.ai/pricing) | agent-sandbox/firecracker | $9.00 | no machine size published, not shape-comparable; egress unpublished |

### 24/7 x30 — 177 priceable, top 25

| # | Provider | Type | Cost | Notes |
|---|---|---|---|---|
| 1 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.986 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 2 | [netcup VPS](https://www.netcup.com/en/server/vps) | hyperscaler/vm | $5.03 | entry row is VPS Lite 1 (6-month min); VPS 500 is $8.51/mo; price is one month's rent at every horizon |
| 3 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $6.12 | egress unpublished |
| 4 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $6.49 |  |
| 5 | [Contabo](https://contabo.com/en-us/pricing/) | hyperscaler/vm | $6.60 | visible $4.40 is a 24-month intro, list is $6.60; price is one month's rent at every horizon |
| 6 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $7.41 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 7 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $9.86 | egress unpublished |
| 8 | [Upstash Box](https://upstash.com/pricing/box) | agent-sandbox/container | $9.97 | egress unpublished; flat pool, billed whether used or not |
| 9 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $10.65 |  |
| 10 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $13.92 | disk beyond 0 GiB: price unknown |
| 11 | [UpCloud](https://upcloud.com/pricing/) | hyperscaler/vm | $14.00 |  |
| 12 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $14.40 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 13 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $14.40 | egress unpublished |
| 14 | [Alibaba Cloud ECS International](https://www.alibabacloud.com/en/product/ecs/pricing) | hyperscaler/vm | $14.48 |  |
| 15 | [Hostinger VPS](https://www.hostinger.com/vps-hosting) | hyperscaler/vm | $14.99 | price is one month's rent at every horizon |
| 16 | [exe.dev](https://exe.dev/pricing) | dev-env/vm | $15.00 | $15/mo minimum, fee is a usage credit; flat pool, billed whether used or not |
| 17 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $15.72 | Medium only: runtime fixes 4 vCPU / 4 GiB |
| 18 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $16.20 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 19 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $17.77 | $5.22/mo free credit |
| 20 | [Fly.io Machines](https://fly.io/pricing) | paas/firecracker | $18.20 |  |
| 21 | [OVHcloud Public Cloud](https://us.ovhcloud.com/public-cloud/prices/) | hyperscaler/vm | $18.43 |  |
| 22 | [Scaleway Instances](https://www.scaleway.com/en/pricing/virtual-instances/) | hyperscaler/vm | $18.67 | Stardust disk is billed on top of the instance rate |
| 23 | [Kamatera](https://www.kamatera.com/pricing/) | hyperscaler/vm | $19.73 |  |
| 24 | [boat.dev](https://docs.boat.dev/pricing) | agent-sandbox/vm | $20.00 | disk beyond 12 GiB: price unknown; $20/mo minimum, fee is a usage credit |
| 25 | [Notte](https://www.notte.cc/pricing) | browser/container | $20.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; $20/mo minimum, fee is a usage credit |

## Could not be priced at the 10 h/day month (or any horizon)

| Provider | Type | Reason |
|---|---|---|
| [Agency Tool Company](https://agencytool.com) | dev-env/bare-metal | Native product; see regime notes: needs opt-in (alt) |
| [Agent Relay](https://agentrelay.com) | paas/- | Native product; see regime notes: needs opt-in (alt) |
| [ainclave](https://www.ainclave.com/pricing) | agent-sandbox/firecracker | On-demand: needs opt-in (sales); Dedicated reserved hosts: needs opt-in (sales) |
| [Airtop](https://www.airtop.ai/pricing) | browser/vm | no preset with ≥2 vCPU and ≥4 GiB |
| [Alibaba Cloud ACK (Harbor backend)](https://www.alibabacloud.com/product/kubernetes) | hyperscaler/container | ACK cluster runtime: needs opt-in (alt); ACK pods on virtual nodes (ECI), per vCPU/GiB: needs opt-in (alt) |
| [Amp Orbs](https://ampcode.com/docs/orbs/sizes-and-costs) | dev-env/vm | Hosted orb compute, PAYG or subscription allowance: needs opt-in (alt) |
| [Veertu Anka Build Cloud](https://docs.veertu.com/anka/licensing/) | macos/apple-vm | Anka Build licence on your own Macs (contact sales): needs opt-in (alt, sales); Anka Build AMI on AWS EC2 Mac (Marketplace hourly software fee): needs opt-in (a |
| [Apoxy](https://apoxy.dev) | paas/gvisor | Native product; see regime notes: needs opt-in (alt) |
| [Aptible](https://www.aptible.com) | paas/container | Native product; see regime notes: needs opt-in (alt, burstable); CPU-Optimized (C) container profile: needs opt-in (alt, burstable); Memory Optimized (R) contai |
| [Archal](https://www.archal.ai/) | agent-sandbox/container | Native product; see regime notes: needs opt-in (alt) |
| [Arga Labs](https://www.argalabs.com/) | agent-sandbox/container | Native product; see regime notes: needs opt-in (alt) |
| [Artillery](https://www.artillery.io/pricing) | dev-env/container | Test workers and Cloud platform: needs opt-in (alt) |
| [AutoComputer](https://www.autocomputer.ai/) | windows/firecracker | Native product; see regime notes: needs opt-in (alt) |
| [AWS EC2 Mac (Dedicated Host)](https://aws.amazon.com/ec2/instance-types/mac/) | macos/dedicated-host | no Linux; Host split into 2 macOS VMs (Apple SLA cap), per-VM price: needs opt-in (alt) |
| [AWS EC2 (Windows Server)](https://aws.amazon.com/ec2/pricing/on-demand/) | windows/vm | no Linux; spot: needs opt-in (spot) |
| [AWS Lambda](https://aws.amazon.com/lambda/pricing/) | hyperscaler/firecracker | Pay-as-you-go: sessions capped at 0.25 h |
| [Microsoft Dev Box (closed to new customers; retiring 2028-09-18)](https://azure.microsoft.com/en-us/products/dev-box/) | windows/vm | discontinued / closed to new customers |
| [Microsoft Foundry hosted agents (East US)](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/) | hyperscaler/vm | East US hosted agent compute: needs opt-in (alt); EU hosted agent compute (Sweden Central, France Central, UK South): needs opt-in (alt) |
| [Microsoft Azure GPU VMs](https://prices.azure.com/api/retail/prices) | gpu-cloud/vm | Standard_NC24ads_A100_v4, spot (×1): needs opt-in (spot); Standard_ND96amsr_A100_v4, spot (×8 node): needs opt-in (spot); Standard_ND96isr_H100_v5, spot (×8 nod |
| [Azure Pipelines](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/) | paas/vm | Microsoft-hosted parallel jobs ($40 each/month, unlimited minutes): needs opt-in (alt); Microsoft-hosted macOS parallel jobs ($40 each/month, unlimited minutes) |
| [Azure Virtual Machines (Windows Server)](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/) | windows/vm | no Linux; Azure Spot VM (representative East US): needs opt-in (spot) |
| [Baseten](https://docs.baseten.co/deployment/resources) | gpu-cloud/container | T4, serverless (×1): needs opt-in (alt); L4, serverless (×1): needs opt-in (alt); A10G, serverless (×1): needs opt-in (alt); A100-80GB, serverless (×1): needs o |
| [Brimble Sandboxes](https://brimble.io/pricing) | agent-sandbox/gvisor | no published per-resource rate |
| [BrowserAct](https://www.browseract.com/pricing) | browser/- | no preset with ≥2 vCPU and ≥4 GiB |
| [BuildJet](https://buildjet.com/for-github-actions) | dev-env/- | discontinued / closed to new customers |
| [Butter](https://butter.dev) | agent-sandbox/gvisor | Native product; see regime notes: needs opt-in (alt) |
| [Bytebot](https://www.bytebot.ai/) | agent-sandbox/container | Self-hosted open-source Docker desktop agent: needs opt-in (alt) |
| [Capy](https://capy.ai) | agent-sandbox/vm | Per-thread VM, billed hourly by size while awake: needs opt-in (alt) |
| [Caution](https://caution.co/pricing.html) | paas/vm | Fully managed enclave: needs opt-in (sales); Managed enclave in own AWS: needs opt-in (sales, alt); AGPL self-host: needs opt-in (alt) |
| [Cedana](https://cedana.com/) | other (checkpoint/restore software; not a compute provider)/- | Native product; see regime notes: needs opt-in (alt) |
| [Cerebrium](https://cerebrium.ai/pricing) | gpu-cloud/container | Interruptible: needs opt-in (spot, alt); Protected compute: needs opt-in (alt); B200, serverless: needs opt-in (spot); H200, serverless: needs opt-in (spot); H1 |
| [Chronicle Labs](https://chronicle-labs.com) | agent-sandbox/qemu-kvm | Native service: needs opt-in (alt) |
| [Cirrus Runners](https://cirrus-runners.app/pricing/) | macos/apple-vm | discontinued / closed to new customers |
| [Claude Managed Agents](https://platform.claude.com/docs/en/about-claude/pricing#claude-managed-agents-pricing) | agent-sandbox/container | Cloud sandbox session runtime ($0.08 per running session-hour, flat): needs opt-in (alt); Self-hosted sandbox environment (your infra, Anthropic orchestration): |
| [Claw 2 Agent](https://claw2agent.com/pricing) | agent-sandbox/dedicated-vm | no preset with ≥2 vCPU and ≥4 GiB |
| [CloudAxis](https://cloudaxis.ai/pricing/) | browser/- | no preset with ≥2 vCPU and ≥4 GiB |
| [CloudBrowser AI](https://cloudbrowser.ai/) | browser/container | no preset with ≥2 vCPU and ≥4 GiB |
| [Cloudflare Workers for Platforms](https://developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/reference/pricing/) | paas/isolate | needs 2 vCPU, largest option is 1; max 1 vCPU per sandbox |
| [cloudrouter (Manaflow)](https://cloudrouter.dev) | agent-sandbox/firecracker | discontinued / closed to new customers |
| [Clusy](https://www.clusy.io/pricing) | dev-env/firecracker | On-demand: needs opt-in (alt) |
| [Coder](https://coder.com/pricing) | dev-env/- | Self-hosted workspaces: needs opt-in (alt) |
| [Comfy Deploy](https://app.comfydeploy.com/pricing) | gpu-cloud/- | discontinued / closed to new customers |
| [Computer Use Cloud (computeruse.run)](https://computeruse.run/) | agent-sandbox/- | discontinued / closed to new customers |
| [ComputerUse.space](https://computeruse.space/) | agent-sandbox/dedicated-host | no preset with ≥2 vCPU and ≥4 GiB |
| [CoreWeave](https://www.coreweave.com/pricing) | gpu-cloud/container | B300, spot (×8 node): needs opt-in (spot); B200, spot (×8 node): needs opt-in (spot); H100, spot (×8 node): needs opt-in (spot); H200, spot (×8 node): needs opt |
| [Cua Fleet (Windows Server)](https://cua.ai/pricing) | windows/vm | no Linux; Cua Cloud macOS (separate product): needs opt-in (sales) |
| [Cube Computer](https://cube.computer/) | dev-env/vm | Per-second VM sizes (50 GB disk): needs opt-in (promo) |
| [Cyberdesk](https://www.cyberdesk.io) | windows/- | Native product; see regime notes: needs opt-in (alt) |
| [Dagger](https://dagger.io) | dev-env/container | Native product; see regime notes: needs opt-in (alt); Cloud Engines (hosted, early access): needs opt-in (alt) |
| [Datalayer Runtimes](https://datalayer.io/pricing) | dev-env/container | no preset with ≥2 vCPU and ≥4 GiB |
| [Daytona (Windows sandboxes)](https://www.daytona.io/pricing) | windows/vm | no Linux |
| [Dexto](https://www.dexto.ai/docs/models/) | agent-sandbox/- | Native product; see regime notes: needs opt-in (alt) |
| [DigitalOcean GPU Droplets](https://www.digitalocean.com/pricing/gpu-droplets) | gpu-cloud/vm | B300, reserved: needs opt-in (sales, commit); H200, reserved: needs opt-in (sales, commit); H100, reserved: needs opt-in (sales, commit); MI350X, reserved: need |
| [Dockup](https://getdockup.com/) | paas/container | Native service: needs opt-in (alt) |
| [Eventual](https://www.eventual.ai/) | paas/- | Daft open-source self-hosted engine: needs opt-in (alt); Eventual robotics data platform: needs opt-in (sales, alt) |
| [Expanse](https://expanse.sh) | gpu-cloud/- | Native product; see regime notes: needs opt-in (alt) |
| [fal](https://fal.ai/pricing) | gpu-cloud/container | B300, reserved: needs opt-in (sales); B200, reserved: needs opt-in (sales); H200, reserved: needs opt-in (sales); H100, reserved: needs opt-in (sales); RTX-PRO- |
| [Ferr](https://ferr.dev/) | browser/container | no preset with ≥2 vCPU and ≥4 GiB |
| [Flow Swiss Mac Bare Metal](https://doc.flow.swiss/platform/pricing/mac-bare-metal) | macos/dedicated-host | no Linux; Mac split into 2 macOS VMs (Apple SLA cap), per-VM price: needs opt-in (alt); CI Engine (managed ephemeral macOS CI runners on M4 Pro), monthly per co |
| [FlowDeploy](https://flowdeploy.com) | gpu-cloud/- | discontinued / closed to new customers |
| [Fluidstack](https://fluidstack.io/) | gpu-cloud/dedicated-host | H100, reserved: needs opt-in (alt, sales); H200, reserved: needs opt-in (alt, sales); B200, reserved: needs opt-in (alt, sales); GB200, reserved: needs opt-in ( |
| [Google Compute Engine GPU VMs](https://cloud.google.com/products/compute/pricing/accelerator-optimized) | gpu-cloud/vm | a2-highgpu-1g, spot (×1): needs opt-in (spot); a2-ultragpu-1g, spot (×1): needs opt-in (spot); a3-highgpu-1g, spot (x1 H100): needs opt-in (spot); a3-highgpu-8g |
| [Google Compute Engine (Windows Server)](https://cloud.google.com/compute/disks-image-pricing#windows_server_pricing) | windows/vm | no Linux |
| [Gemini API code execution](https://ai.google.dev/gemini-api/docs/code-execution) | agent-sandbox/container | Built-in code execution tool (token-billed only): needs opt-in (alt) |
| [GitHub Copilot cloud sandboxes](https://docs.github.com/en/billing/concepts/product-billing/cloud-and-local-sandboxes) | hyperscaler/firecracker | Cloud sandbox (copilot --cloud), per-second meters: needs opt-in (alt) |
| [Google Colab](https://developers.google.com/colab) | dev-env/vm | On-demand: needs opt-in (alt); Colab Enterprise (GCP, us-central1): needs opt-in (alt) |
| [Green Mini host](https://portal.greenmini.host/checkout/order) | macos/dedicated-host | no Linux |
| [H Company / Surfer / H Agents API](https://www.hcompany.ai/pricing) | browser/- | no preset with ≥2 vCPU and ≥4 GiB |
| [Halluminate](https://halluminate.ai/) | agent-sandbox/- | Native product; see regime notes: needs opt-in (alt) |
| [Hatchet](https://hatchet.run) | paas/container | Native product; see regime notes: needs opt-in (alt) |
| [Heroic Labs](http://heroiclabs.com) | paas/dedicated-vm | Native product; see regime notes: needs opt-in (alt) |
| [Heroku](https://www.heroku.com/pricing/) | paas/container | Cedar Common Runtime dynos (Basic/Standard shared; Performance dedicated): needs opt-in (alt); Eco dynos: $5 flat for a 1,000 dyno-hour pool (personal apps only |
| [Hetzner GPU servers](https://www.hetzner.com/dedicated-rootserver/matrix-gpu/) | gpu-cloud/dedicated-host | GEX45 Blackwell SFF 24GB, on-demand (×1): needs opt-in (alt); GEX131 Blackwell Max-Q 96GB, on-demand (×1): needs opt-in (alt); no preset with ≥2 vCPU and ≥4 GiB |
| [Hoplite](https://hoplite.sh) | agent-sandbox/gvisor | Native service: needs opt-in (alt) |
| [HostMyApple](https://hostmyapple.com/mac-vps-hosting) | macos/vm | no Linux |
| [HUD](https://www.hud.ai/) | agent-sandbox/vm | Native service: needs opt-in (alt); HUD-hosted on Modal (CPU/GPU profiles): needs opt-in (alt) |
| [Hugging Face Jobs (hf-sandbox backend)](https://huggingface.co/docs/hub/en/jobs-pricing) | paas/container | On-demand: needs opt-in (alt); GPU: Nvidia T4: needs opt-in (alt); GPU: Nvidia L4: needs opt-in (alt); GPU: Nvidia L40S: needs opt-in (alt); GPU: Nvidia A10G: n |
| [HumanLayer](https://humanlayer.com) | agent-sandbox/- | Native product; see regime notes: needs opt-in (alt) |
| [Hyperbolic](https://www.hyperbolic.ai/marketplace) | gpu-cloud/vm | Private Cloud (single-tenant, >1 year contract): needs opt-in (sales) |
| [Hyrex](https://www.hyrex.io) | paas/- | Native product; see regime notes: needs opt-in (alt) |
| [Isle](https://www.tryisle.com/) | agent-sandbox/- | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt) |
| [Jamsocket](https://jamsocket.com) | agent-sandbox/gvisor | discontinued / closed to new customers |
| [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks) | dev-env/container | On-demand: needs opt-in (alt) |
| [Kasm Workspaces](https://kasm.com/community-edition) | dev-env/container | Self-hosted Workspaces licence (Starter: $10/user or $20/concurrent session): needs opt-in (alt, commit); Kasm-managed Workspaces as a Service (minimum 25 users |
| [KubeSail](https://kubesail.com) | paas/- | discontinued / closed to new customers |
| [Lambda](https://lambda.ai/pricing) | gpu-cloud/vm | H100, reserved (×16 node): needs opt-in (alt, sales); H100, reserved (×64 node): needs opt-in (alt, sales); H100, reserved (×256 node): needs opt-in (alt, sales |
| [LangSmith Sandboxes](https://www.langchain.com/pricing) | agent-sandbox/vm | Developer: reach only an allowlist (package registries, git, AI APIs); Plus (one seat): reach only an allowlist (package registries, git, AI APIs); Enterprise:  |
| [Lapdev](https://lap.dev/pricing/) | dev-env/container | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt) |
| [Limrun](https://lim.run) | macos/apple-vm | Native product; see regime notes: needs opt-in (alt) |
| [MacinCloud](https://www.macincloud.com/pages/dedicated.html) | macos/vm | no Linux; Pay-as-You-Go by the day (shared managed Mac, no admin): needs opt-in (alt); Managed Server plan (shared managed Mac account), monthly: needs opt-in ( |
| [MacStadium](https://www.macstadium.com/pricing) | macos/dedicated-host | no Linux; Orka macOS VM cluster (Mac Cloud Compute), contact sales: needs opt-in (sales); Orka Burst elastic nodes (add-on to an Orka cluster): needs opt-in (sa |
| [Magnitude](https://magnitude.dev/) | browser/- | discontinued / closed to new customers |
| [Manufact](https://manufact.com) | paas/firecracker | Native product; see regime notes: needs opt-in (alt) |
| [Manus Cloud Computer](https://help.manus.im/en/articles/15392078-understanding-cloud-computer-plans-and-billing) | agent-sandbox/vm | commit regime only covers always-on instances |
| [Maritime](https://maritime.sh/pricing) | agent-sandbox/firecracker | no preset with ≥2 vCPU and ≥4 GiB |
| [Mastra](https://mastra.ai) | paas/dedicated-vm | Native product; see regime notes: needs opt-in (alt); Mastra Platform Starter CPU-time meter: needs opt-in (alt); Mastra Platform Teams CPU-time meter: needs op |
| [Metorial](https://metorial.com) | paas/container | Native service: needs opt-in (alt) |
| [Minicor](https://minicor.com) | windows/dedicated-vm | Native product; see regime notes: needs opt-in (alt) |
| [MiniMax Agent hosting / developer API scope](https://platform.minimax.io/docs/llms.txt) | agent-sandbox/- | Hosted agent environment quote/spec unverified: needs opt-in (alt) |
| [Mistral Compute / AI Cloud](https://mistral.ai/products/aicloud/) | gpu-cloud/bare-metal | Dedicated AI capacity: needs opt-in (sales, commit) |
| [Modelence](https://modelence.com) | paas/container | App containers: needs opt-in (alt) |
| [Moonshot Kimi Hosted Agents sandbox](https://platform.kimi.com/docs/pricing/hosted-agents.md) | agent-sandbox/- | Hosted Agents 1C/1G sandbox: needs opt-in (alt, sales) |
| [Nebius ConTree (Token Factory Sandboxes)](https://tokenfactory.nebius.com/sandboxes/about) | agent-sandbox/vm | no published per-resource rate |
| [Nextmv](https://nextmv.io) | paas/container | Native product; see regime notes: needs opt-in (alt) |
| [Nodus Compute](https://www.nodus-compute.ai/pricing/) | agent-sandbox/- | no published per-resource rate |
| [OakHost](https://www.oakhost.com/mac-mini-hosting) | macos/dedicated-host | no Linux; "Try macOS for a week" (M2, 8+ GB), one-off 7 days: needs opt-in (promo, stock) |
| [Okteto](https://okteto.com) | dev-env/container | Native product; see regime notes: needs opt-in (alt) |
| [OmniRun](https://omnirun.io/pricing) | agent-sandbox/firecracker | no preset with ≥2 vCPU and ≥4 GiB |
| [OneCLI](https://onecli.sh) | agent-sandbox/vm | Native product; see regime notes: needs opt-in (alt) |
| [OpenAGI / Lux](https://developer.agiopen.org/docs/pricing) | browser/- | Bring your own computer: needs opt-in (alt) |
| [OpenAI Containers (Code Interpreter / Hosted Shell)](https://developers.openai.com/api/docs/pricing) | agent-sandbox/vm | API pay as you go: reach only an allowlist (package registries, git, AI APIs); ChatGPT Plus: regime not sold on this plan; ChatGPT Pro $100: regime not sold on  |
| [OpenHands Remote Sandbox / Cloud](https://docs.openhands.dev/openhands/usage/sandboxes/remote) | dev-env/container | Managed OpenHands Cloud: needs opt-in (alt); Remote agent server on own infrastructure: needs opt-in (alt) |
| [PaperPod](https://www.paperpod.dev/) | agent-sandbox/container | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt) |
| [Party](https://party.build) | agent-sandbox/container | Native product; see regime notes: needs opt-in (alt) |
| [Pipekit](https://pipekit.io/pricing) | dev-env/container | Native product; see regime notes: needs opt-in (alt) |
| [Pipeshift](https://pipeshift.com) | gpu-cloud/dedicated-vm | Native product; see regime notes: needs opt-in (alt) |
| [Playgent](https://useplaygent.com) | agent-sandbox/- | Native product; see regime notes: needs opt-in (alt) |
| [Ploomber](https://ploomber.io/) | paas/- | Native product; see regime notes: needs opt-in (alt) |
| [PoplarML](http://poplarml.com) | gpu-cloud/- | Native product; see regime notes: needs opt-in (alt) |
| [Porter](https://porter.run) | paas/container | Native service: needs opt-in (alt); Porter Sandboxes (AWS, in your own account): needs opt-in (alt) |
| [Reflex](https://reflex.dev/pricing/) | paas/container | Hosted Python apps: needs opt-in (alt) |
| [Refresh](https://www.refresh.dev) | agent-sandbox/- | Native service: needs opt-in (alt) |
| [Release](https://release.com/pricing) | dev-env/container | Enterprise BYOC: needs opt-in (sales, alt) |
| [RentaMac (rentamac.io)](https://rentamac.io/pricing) | macos/dedicated-host | no Linux |
| [Replicate](https://replicate.com/pricing) | gpu-cloud/container | Private Cog CPU model: needs opt-in (alt); T4, serverless (×1): needs opt-in (alt); A100-80GB, serverless (×1): needs opt-in (alt); H100, serverless (×1): needs |
| [Replit](https://docs.replit.com/billing/deployment-pricing) | paas/vm | Autoscale / Scheduled deployment (compute units while serving or running): needs opt-in (alt); commit regime only covers always-on instances |
| [Rescale](https://rescale.com) | gpu-cloud/dedicated-vm | Native product; see regime notes: needs opt-in (alt); no published per-resource rate |
| [Revyl](https://www.revyl.com) | macos/container | Native product; see regime notes: needs opt-in (alt) |
| [Riza Code Interpreter](https://riza.io/pricing) | agent-sandbox/isolate | discontinued / closed to new customers |
| [Run Cloud](https://docs.run.cloud/sandboxes/index.md) | agent-sandbox/firecracker | discontinued / closed to new customers |
| [RunAnywhere](https://www.runanywhere.ai/) | inference-api/- | Wally hosted token-billed inference preview (not an arbitrary-code VM): needs opt-in (alt) |
| [RunKit](https://runkit.com/) | agent-sandbox/- | discontinued / closed to new customers |
| [Scaleway Apple silicon (Mac mini)](https://www.scaleway.com/en/pricing/apple-silicon/) | macos/dedicated-host | no Linux |
| [Scaleway GPU instances](https://www.scaleway.com/en/pricing/gpu/) | gpu-cloud/vm | no priceable regime |
| [ScitiX Agent Sandbox](https://scitix.github.io/Agent-Sandbox/) | agent-sandbox/container | Self-hosted runtime + externally billed clusters: needs opt-in (alt); Self-hosted container backend: needs opt-in (alt); Self-hosted microVM backend: needs opt- |
| [Scraping Bee](https://www.scrapingbee.com/pricing/) | browser/- | Browser API request (not time-priced): needs opt-in (alt) |
| [SeaCloudAI Sandbox](https://sandbox-gateway.cloud.seaart.ai) | agent-sandbox/container | no published per-resource rate |
| [Self-hosted bare-metal sandbox fleet (hardware floor)](https://www.hetzner.com/dedicated-rootserver/ax42/) | self-host/firecracker | Hetzner AX42 / 50% occupancy: needs opt-in (alt); Hetzner AX42 / 70% occupancy: needs opt-in (alt); Hetzner AX42 / 90% occupancy: needs opt-in (alt); Hetzner EX |
| [Server4Agent](https://www.server4agent.com/pricing) | dev-env/container | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt) |
| [SF Tensor](https://sf-tensor.com) | gpu-cloud/gvisor | Native product; see regime notes: needs opt-in (alt, sales) |
| [Shadeform](https://www.shadeform.ai/) | gpu-cloud/dedicated-vm | Current applicable tariff unverified: price not published; Reserved commitments: negotiated plan |
| [Shuttle](https://www.shuttle.dev) | paas/- | discontinued / closed to new customers |
| [Sieve](https://sievedata.com/) | gpu-cloud/- | discontinued / closed to new customers |
| [Signadot](https://www.signadot.com/) | dev-env/container | Native product; see regime notes: needs opt-in (alt) |
| [Skyhook](https://skyhook.io) | paas/container | Native service: needs opt-in (alt) |
| [Skyvern](https://www.skyvern.com/pricing) | browser/container | no published per-resource rate |
| [Smooth](https://www.smooth.sh/pricing) | browser/- | no published per-resource rate |
| [Specific](https://specific.dev/pricing) | paas/container | Hosted services: needs opt-in (alt) |
| [Strong Compute](https://strongcompute.com) | finops (GPU/LLM spend-management SaaS; legacy managed GPU training platform 'ISC')/container | Native product; see regime notes: needs opt-in (alt) |
| [Tabstack](https://tabstack.ai/) | browser/- | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt) |
| [Tart + Orchard (Cirrus Labs)](https://tart.run/licensing/) | macos/apple-vm | software licence only - bring your own Macs |
| [Teclada](https://www.teclada.com/) | dev-env/- | Native product; see regime notes: needs opt-in (alt) |
| [Tencent Cloud CubeSandbox](https://github.com/TencentCloud/CubeSandbox) | agent-sandbox/vm | no published per-resource rate; Self-hosted CubeSandbox (Apache-2.0): needs opt-in (alt) |
| [Tencent Cloud SCF](https://cloud.tencent.com/document/product/583/17299) | hyperscaler/container | Event function: needs opt-in (alt); Web function: needs opt-in (alt); Provisioned concurrency (idle): needs opt-in (alt) |
| [TensorDock](https://www.tensordock.com/) | gpu-cloud/vm | H100, spot: needs opt-in (spot); A100, spot: needs opt-in (spot); RTX4090, spot: needs opt-in (spot); size list not published |
| [TensorPool](https://tensorpool.dev) | gpu-cloud/- | discontinued / closed to new customers |
| [Texel.ai](https://texel.ai) | gpu-cloud/- | Native product; see regime notes: needs opt-in (alt) |
| [Thunder Compute](https://www.thundercompute.com/pricing) | gpu-cloud/container | Reserved clusters (8-512+ GPUs, fixed term): needs opt-in (sales) |
| [Tilde.run (discontinued)](https://lakefs.io/blog/we-recently-shut-down-tilde-run/) | agent-sandbox/container | discontinued / closed to new customers |
| [Tilion](https://tilion.com/pricing) | browser/- | no published per-resource rate |
| [Tinfoil](https://tinfoil.sh) | paas/vm | Native product; see regime notes: needs opt-in (alt); Confidential GPU enclave (monthly contract): needs opt-in (alt, sales) |
| [TinyFish](https://www.tinyfish.ai/pricing) | browser/- | Native product meter; not a general-purpose 4-vCPU/8-GiB VM: needs opt-in (alt); Monitor (Page/Topic change tracking): needs opt-in (alt) |
| [Together AI](https://www.together.ai/pricing) | gpu-cloud/container | H100 HGX/SXM, spot (×8 node): needs opt-in (spot); H200 HGX/SXM, spot (×8 node): needs opt-in (spot); B200 HGX/SXM, spot (×8 node): needs opt-in (spot); B300 HG |
| [Trainy](https://trainy.ai/) | paas/container | Native product; see regime notes: needs opt-in (alt) |
| [Trigger.dev](https://trigger.dev/pricing) | paas/container | Managed tasks: needs opt-in (alt) |
| [use.computer](https://use.computer/) | macos/apple-vm | no Linux |
| [Vast.ai](https://github.com/vast-ai/docs/blob/main/guides/pricing.mdx) | gpu-cloud/container | RTX4090, on-demand: needs opt-in (alt); RTX5090, on-demand: needs opt-in (alt); RTX-PRO-6000, on-demand: needs opt-in (alt); A100-80GB, on-demand: needs opt-in  |
| [Google Agent Platform Sandbox (Code Execution / Shell / Computer Use)](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing) | agent-sandbox/container | Usage based: no internet access |
| [Vibrant Labs](https://vibrantlabs.com/) | agent-sandbox/- | Native service: needs opt-in (alt) |
| [Voltage Park](https://www.voltagepark.com/pricing) | gpu-cloud/vm | HGX H100 on-demand InfiniBand (8+ GPUs): needs opt-in (sales) |
| [Vultr Cloud GPU](https://api.vultr.com/v2/plans?type=vcg) | gpu-cloud/vm | vcg-a16-2c-8g-2vram, on-demand (×1): needs opt-in (alt); vcg-a16-2c-16g-4vram, on-demand (×1): needs opt-in (alt); vcg-a40-1c-5g-2vram, on-demand (×1): needs op |
| [Vultr Cloud Compute (Windows Server)](https://docs.vultr.com/support/platform/billing/is-a-windows-license-included-in-the-monthly-price) | windows/vm | no Linux |
| [Wasmer](https://wasmer.io/pricing) | paas/isolate | WebAssembly Edge: needs opt-in (alt) |
| [webapp.io](https://webapp.io) | dev-env/- | discontinued / closed to new customers |
| [StackBlitz WebContainers](https://stackblitz.com/pricing) | dev-env/v8-isolate | Browser-local runtime licence: needs opt-in (alt) |
| [Windmill](https://www.windmill.dev/pricing) | paas/container | Cloud Team execution credits: needs opt-in (alt); Dedicated Cloud Enterprise: needs opt-in (sales, alt); Self-hosted software: needs opt-in (alt) |
| [Windows 365 for Agents](https://learn.microsoft.com/en-us/windows-365/agents/pricing-paygo-always-available) | windows/vm | no Linux |
| [Windows 365 Cloud PC (Business / Enterprise)](https://www.microsoft.com/en-us/windows-365/business/compare-plans-pricing) | windows/vm | no Linux; Windows 365 Enterprise GPU Standard: needs opt-in (sales); Windows 365 Flex: needs opt-in (sales); Windows 365 Reserve: needs opt-in (sales) |
| [Apple Xcode Cloud](https://developer.apple.com/xcode-cloud/) | macos/apple-vm | Xcode Cloud compute hours (Xcode build/test only): needs opt-in (alt) |
| [YepCode Run](https://yepcode.io/pricing/) | paas/firecracker | Process execution on Starter (per-second Yeps): needs opt-in (alt); Process execution on Growth (per-second Yeps): needs opt-in (alt) |
| [Zeabur](https://zeabur.com/pricing) | paas/container | Bring or buy server; compute separately billed: needs opt-in (alt) |
| [Zenrows Browser Sessions](https://www.zenrows.com/pricing) | browser/container | Free: regime not sold on this plan; Build B1: regime not sold on this plan; Build B2: regime not sold on this plan; Build B3: regime not sold on this plan; Laun |
| [Zhipu Z Managed Agents](https://docs.bigmodel.cn/cn/managed-agents/overview.md) | agent-sandbox/- | Managed Agent sandbox, temporary free runtime fee: needs opt-in (alt) |
| [Zibra Labs](https://zibralabs.ai/) | gpu-cloud/- | Native product; see regime notes: needs opt-in (alt) |
| [Zo Computer](https://www.zo.computer/pricing) | dev-env/container | Zo Basic subscription, one always-on computer (4 cores / 32 GB) - $18/mo: needs opt-in (alt); Zo Pro subscription, one always-on computer (16 cores / 128 GB) -  |
| [Bright Data Browser API](https://brightdata.com/pricing/scraping-browser) | browser/- | no published compute rate (meter is bandwidth/pool) |
| [Unikraft Cloud](https://unikraft.com/pricing) | agent-sandbox/firecracker | no published compute rate (meter is bandwidth/pool) |
