# ML/AI ENGINEER — MASTER STUDY PLAN v2

**Target:** Remote ML/AI Engineering roles with US and international teams  
**Portfolio Project:** AURA — Automotive Understanding & Reasoning Agent (Edge AI Copilot)  
**Career Stage:** Pivoting from Data Science / Statistical Modeling → ML Engineering / AI Systems  
**Author:** Guilherme  
**Last Updated:** April 2026

---

## Career Context

This plan prepares for ML/AI Engineering roles that span the full stack — from model training and RAG systems through inference optimization and edge deployment. The target is remote positions with US or international teams (e.g., Factored, FuelTech AI roles, inference-focused engineering teams).

AURA serves as the primary learning and testing ground: every topic in this plan maps to a real component in the project. This avoids studying in the abstract — each concept gets implemented, profiled, and benchmarked against hardware constraints.

**Covered role families:**
- ML Engineer (RAGs/LLMs) — e.g., Factored
- AI Specialist (Conversational AI / Data Analysis) — e.g., FuelTech
- AI Systems Engineer (Inference & Edge) — inference optimization, model serving, edge deployment

---

## 1. PYTHON PROGRAMMING

### 1.1 Object-Oriented Programming
- Classes and objects (`__init__`, `self`, instantiation)
- Instance vs. class attributes
- Inheritance (single, multiple, MRO)
- Polymorphism
- Encapsulation and properties (`@property`, `@setter`)
- Abstract base classes (`ABC`, `@abstractmethod`)
- Dunder/magic methods (`__repr__`, `__str__`, `__eq__`, `__add__`, `__len__`, `__getitem__`, `__contains__`, `__hash__`, `__call__`, `__iter__`)

**AURA touchpoint:** Agent tool base class hierarchy, `VehicleProfile` and `SessionContext` dataclasses, `__call__` on tool objects.

### 1.2 Core Data Structures
- Lists (operations, slicing, time complexity)
- Dictionaries (hash maps, `.get()`, `.items()`, comprehensions)
- Sets (membership, union, intersection, difference)
- Tuples (immutability, unpacking)
- `defaultdict`, `Counter`, `deque` from collections
- Time complexity for each structure (O(1), O(n) operations)

### 1.3 Comprehensions and Generators
- List comprehensions (with filtering, nested)
- Dict comprehensions
- Set comprehensions
- Generator expressions (lazy evaluation)
- Generator functions with `yield`

**AURA touchpoint:** Generators for streaming OBD-II sensor reads, lazy document loading in RAG ingestion pipeline.

### 1.4 Decorators
- Function decorators (wrapper pattern)
- `@staticmethod`, `@classmethod`
- `@property`

### 1.5 Error Handling
- `try` / `except` / `else` / `finally`
- Custom exception classes

### 1.6 Clean Code Practices
- Descriptive variable and function names
- Docstrings for functions and classes
- Comments explaining WHY, not WHAT
- Modular design (small, focused functions)
- Edge case handling

### 1.7 Performance & Scalability for ML Systems

> This section bridges Python fundamentals with production ML concerns. Study alongside §8–9 (Embeddings + RAG) and §14 (Inference Optimization) so every exercise maps to a real component.

#### 1.7.1 Profiling & Optimization
- Profiling with `cProfile`, `line_profiler` — applied to data preprocessing and embedding pipelines
- Memory profiling (`tracemalloc`, `memory_profiler`) for large document ingestion (§9.2 Indexing Pipeline)
- Efficient batching patterns for embedding API calls (§8.1, §11.1)
- `numpy` vectorization vs Python loops for similarity computations (§8.2)
- `__slots__` in high-frequency objects (e.g., `SensorReading` in telemetry streams)
- `functools.lru_cache` for repeated computations (DTC lookups, maintenance schedule queries)

**AURA touchpoint:** Profile the RAG indexing pipeline end-to-end — chunking, embedding, ChromaDB insertion. Identify whether bottleneck is CPU (chunking), network (API calls), or I/O (DB writes).

#### 1.7.2 Concurrency for ML Workloads
- `asyncio` + `httpx` for concurrent LLM API calls — the #1 practical use case for ML engineer interviews
- `concurrent.futures.ProcessPoolExecutor` for CPU-bound preprocessing (tokenization, text cleaning at scale)
- `concurrent.futures.ThreadPoolExecutor` for I/O-bound tasks (document loading, file parsing)
- `asyncio.Semaphore` for rate-limiting API calls (cost management, §12.4)
- `asyncio.Queue` for producer-consumer patterns in streaming RAG pipelines (query → retrieve → generate)
- `threading` vs `multiprocessing` vs `asyncio` — when to use each, GIL implications

**AURA touchpoint:** Parallel document chunking during corpus ingestion. Async embedding API calls with rate limiting. Producer-consumer pattern: OBD-II sensor polling (producer) → anomaly detection (consumer).

#### 1.7.3 Data Processing at Scale
- Generators for lazy document processing (huge PDF/CSV corpora)
- Chunked reading with pandas for large datasets before embedding
- `polars` as faster alternative for tabular preprocessing
- Batch insertion into vector DBs (§8.3) — throughput vs latency tradeoffs
- File format choices: Parquet vs JSON lines vs CSV for preprocessed chunks
- `itertools` for memory-efficient pipelines

**AURA touchpoint:** Process 500-800 RAG chunks efficiently. Batch insert into ChromaDB. Store telemetry sessions in SQLite with efficient time-series patterns.

#### 1.7.4 Architecture Patterns for Serving
- FastAPI async endpoints serving RAG queries (§12.2)
- Redis caching for repeated queries and embedding results (§12.2, §12.4)
- Background task queues (Celery + Redis) for async indexing of new documents
- Connection pooling for vector DB and PostgreSQL/pgvector
- Docker resource management for ML serving containers (§12.2)

**AURA touchpoint:** FastAPI + HTMX web UI serving chat + live sensor dashboard. Caching frequent DTC lookups and maintenance schedule queries. Background indexing when new forum content is scraped.

#### 1.7.5 C++ Interop Awareness
- Why inference runtimes are C++ under the hood (ONNX Runtime, llama.cpp, Triton)
- `pybind11` basics — how Python wraps C++ for performance-critical paths
- When Python becomes the bottleneck in a serving stack
- Understanding `llama-cpp-python` as a binding layer over C++ inference

**AURA touchpoint:** `llama-cpp-python` is the primary edge LLM runtime. Understanding the binding layer helps debug latency issues and configure memory mapping.

---

## 2. DATA STRUCTURES & ALGORITHMS

### 2.1 Big O Notation
- O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ)
- Time vs. space complexity
- Analyzing loops and nested loops

### 2.2 Linked Lists
- Node structure
- Append, traverse, reverse (in-place)
- Singly vs. doubly linked

### 2.3 Stacks and Queues
- Stack: LIFO, push/pop, Python list as stack
- Queue: FIFO, enqueue/dequeue, `deque` as queue
- Classic problem: valid parentheses

### 2.4 Binary Trees
- Node structure (val, left, right)
- Binary Search Tree (BST) property
- Traversals: inorder, preorder, postorder, level-order (BFS)
- Max depth, invert tree

### 2.5 Hash Maps
- How hash maps work (hashing, collision handling)
- Two Sum pattern
- Frequency counting pattern
- Group Anagrams pattern

### 2.6 Sorting Algorithms
- Merge sort (divide and conquer, O(n log n))
- Quick sort (pivot, partition)
- Python's built-in `sorted()` and `.sort()` (Timsort)

### 2.7 Searching
- Binary search (iterative implementation)
- When and why O(log n)

---

## 3. MATHEMATICS

### 3.1 Linear Algebra
- Vectors: addition, scalar multiplication, dot product
- Dot product as similarity measure
- Vector norms: L1 (Manhattan), L2 (Euclidean)
- L1/L2 connection to regularization
- Matrices: shape, transpose, multiplication rules
- Matrix multiplication: inner dims must match, result shape
- Identity matrix, inverse matrix
- Normal equation: w = (XᵀX)⁻¹Xᵀy
- Eigenvalues and eigenvectors (conceptual, connection to PCA)
- NumPy broadcasting rules

### 3.2 Calculus
- Derivatives: rate of change
- Key rules: power, chain, sum, exponential, logarithm
- Chain rule (foundation of backpropagation)
- Partial derivatives
- Gradient: vector of partial derivatives, direction of steepest increase
- Gradient descent: w = w - α × ∂Loss/∂w
- Sigmoid derivative: σ'(x) = σ(x)(1 - σ(x))
- Convexity: bowl shape, global minimum guaranteed

### 3.3 Probability
- Basic rules: addition, multiplication, complement
- Independence
- Conditional probability: P(A|B)
- Bayes' theorem (with disease testing example)
- Expected value: E[X], linearity of expectation
- Variance: Var(X) = E[X²] - (E[X])²

### 3.4 Probability Distributions
- Bernoulli (single binary trial)
- Binomial (n trials, k successes)
- Normal/Gaussian (bell curve, 68-95-99.7 rule)
- Poisson (events per time interval)
- Uniform

### 3.5 Descriptive Statistics
- Mean, median, mode
- Variance and standard deviation
- Covariance
- Correlation (Pearson, -1 to +1)

### 3.6 Hypothesis Testing
- Null hypothesis (H₀) vs. alternative (H₁)
- p-value interpretation
- Significance level (α = 0.05)
- Type I error (false positive) and Type II error (false negative)
- t-test, chi-squared, ANOVA (conceptual)

### 3.7 Information Theory
- Entropy (uncertainty measure)
- Cross-entropy (classification loss function)
- KL divergence (distance between distributions)

### 3.8 Maximum Likelihood Estimation
- Concept: find parameters that maximize data probability
- Connection to loss functions (cross-entropy, MSE)

---

## 4. MACHINE LEARNING FUNDAMENTALS

### 4.1 Learning Paradigms
- Supervised learning (classification, regression)
- Unsupervised learning (clustering, dimensionality reduction)
- Semi-supervised learning
- Reinforcement learning (conceptual)

### 4.2 ML Workflow
- Problem definition → data collection → EDA → preprocessing → feature engineering → train/val/test split → model training → evaluation → hyperparameter tuning → deployment → monitoring

### 4.3 Data Splitting
- Train / validation / test split (rationale, typical ratios)
- Why validation set exists (prevent data leakage)
- K-fold cross-validation (K=5 or K=10)
- Stratified splitting for imbalanced data

### 4.4 Bias-Variance Trade-Off
- Bias: model too simple → underfitting
- Variance: model too complex → overfitting
- Total error = Bias² + Variance + Noise
- Detection: training vs. validation performance
- Fixes for underfitting vs. overfitting

### 4.5 Supervised Learning Algorithms
- Linear Regression (MSE loss, normal equation, gradient descent)
- Logistic Regression (sigmoid, cross-entropy loss, classification)
- Decision Trees (Gini impurity, information gain, pruning)
- Random Forest (bagging, feature randomness, ensemble)
- Support Vector Machines (margin, support vectors, kernel trick)
- K-Nearest Neighbors (distance metrics, choosing K)
- Generalized Linear Models (link function, Poisson/Gamma for insurance)

### 4.6 Unsupervised Learning Algorithms
- K-Means (centroids, elbow method, K-means++)
- PCA (eigenvectors of covariance matrix, variance explained)
- Hierarchical clustering (conceptual)

### 4.7 Gradient Descent
- Batch, stochastic (SGD), mini-batch
- Learning rate: too large, too small, just right
- Convergence

### 4.8 Regularization
- L1 / Lasso (sparse models, feature selection)
- L2 / Ridge (weight shrinkage)
- Elastic Net (L1 + L2 combination)
- Lambda (λ) controls regularization strength

### 4.9 Evaluation Metrics — Classification
- Confusion matrix (TP, TN, FP, FN)
- Accuracy (and when it's misleading)
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- F1 Score: harmonic mean
- AUC-ROC: curve and area interpretation
- When to prioritize precision vs. recall

### 4.10 Evaluation Metrics — Regression
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

### 4.11 Feature Engineering
- Normalization / standardization
- One-hot encoding
- Handling missing values
- Feature selection techniques

---

## 5. DEEP LEARNING

### 5.1 Neural Network Fundamentals
- Neuron: weighted sum + bias + activation
- Layers: input, hidden, output
- Forward pass
- Why depth matters (hierarchical feature learning)

### 5.2 Activation Functions
- ReLU: max(0, x) — default for hidden layers
- Sigmoid: 1/(1+e⁻ˣ) — binary output
- Tanh: range (-1, 1) — centered at zero
- Softmax: multi-class probabilities summing to 1
- Dying ReLU problem
- Vanishing gradient problem (sigmoid/tanh)

### 5.3 Backpropagation
- Chain rule applied layer by layer
- Forward pass → loss → backward pass → weight update
- How each weight's contribution to error is computed

### 5.4 Loss Functions
- MSE (regression)
- Binary cross-entropy (binary classification)
- Categorical cross-entropy (multi-class)

### 5.5 Optimizers
- SGD (basic)
- Momentum (velocity accumulation)
- RMSProp (adaptive per-parameter rate)
- Adam (momentum + RMSProp, default choice)
- AdamW (decoupled weight decay)
- Learning rate as most critical hyperparameter

### 5.6 Overfitting Prevention
- Dropout (randomly zero neurons during training)
- Early stopping (monitor validation loss)
- L2 regularization / weight decay
- Data augmentation
- Batch normalization

### 5.7 Key Concepts
- Epoch, batch size, learning rate
- Hyperparameters (you set) vs. parameters (model learns)
- Transfer learning (pre-trained → fine-tune)
- Training loop: forward → loss → backward → step

### 5.8 CNN (Convolutional Neural Networks)
- Convolutional layers (filters/kernels)
- Pooling layers (max pooling, average pooling)
- Fully connected layers
- Architecture pattern: Conv → ReLU → Pool → ... → FC → Softmax
- Use case: images, spatial data

### 5.9 RNN and LSTM
- Recurrent connections, hidden state
- Vanishing gradient problem in RNNs
- LSTM: forget gate, input gate, output gate, cell state
- Use case: sequences, time series (legacy, replaced by Transformers)

---

## 6. TRANSFORMERS & ATTENTION

### 6.1 Self-Attention Mechanism
- Query (Q), Key (K), Value (V) matrices
- Attention score: QKᵀ / √dₖ
- Softmax to get weights
- Weighted sum of values
- Intuition: each token decides what to attend to

### 6.2 Multi-Head Attention
- Multiple attention heads in parallel
- Each head learns different relationships
- Concatenation and projection

### 6.3 Positional Encoding
- Why needed (Transformers have no built-in order)
- Sinusoidal (original paper)
- RoPE (Rotary Position Embedding, modern)
- Learned positional embeddings

### 6.4 Architecture Variants
- Encoder-only (BERT): bidirectional, masked language modeling, understanding/classification
- Decoder-only (GPT, Claude, LLaMA): autoregressive, next-token prediction, generation
- Encoder-decoder (T5, BART): full input → generated output, translation/summarization
- Causal masking in decoder models

### 6.5 Key Models to Know
- BERT (Google, encoder-only, MLM)
- GPT-4 / GPT-4o (OpenAI, decoder-only)
- Claude (Anthropic, decoder-only, long context)
- LLaMA 2/3 (Meta, open-source)
- Mistral / Mixtral (efficient, open-source, MoE)
- T5 / FLAN-T5 (Google, encoder-decoder)
- Gemini (Google, multimodal)

---

## 7. LARGE LANGUAGE MODELS (LLMs)

### 7.1 How LLMs Work
- Pre-training on massive text data (next-token prediction)
- Scale: billions of parameters, terabytes of data
- Emergent capabilities at scale

### 7.2 Tokenization
- Subword units (not words, not characters)
- BPE (Byte Pair Encoding) — used by GPT
- WordPiece — used by BERT
- SentencePiece — used by LLaMA
- Context window (measured in tokens)
- Token counting and cost implications

### 7.3 LLM Training Pipeline
- Stage 1: Pre-training (next-token prediction, massive data)
- Stage 2: SFT (Supervised Fine-Tuning on instruction-response pairs)
- Stage 3: RLHF (Reinforcement Learning from Human Feedback)
- DPO as simpler alternative to RLHF

### 7.4 Temperature and Sampling
- Temperature: 0 = deterministic, 0.7 = balanced, 1+ = creative
- Top-k sampling
- Top-p (nucleus) sampling
- For RAG: use LOW temperature (0-0.3)

### 7.5 Fine-Tuning
- Full fine-tuning (all parameters, expensive)
- LoRA (Low-Rank Adaptation, ~99% fewer trainable params)
- QLoRA (LoRA + 4-bit quantization)
- RLHF (human preferences → reward model → PPO)
- DPO (Direct Preference Optimization)
- When to fine-tune vs. when to use RAG
- **Fine-tune → quantize pipeline:** Fine-tune for accuracy first, then quantize for deployment. These are not independent decisions — quantization-aware fine-tuning (QAT) can preserve accuracy better than post-training quantization of a fine-tuned model.

**AURA touchpoint:** Fine-tuned DTC classifier → quantize for Pi 5 deployment. LoRA on small LLM for automotive domain terminology.

---

## 8. EMBEDDINGS & VECTOR DATABASES

### 8.1 Text Embeddings
- Dense vector representations of semantic meaning
- Similar meaning → close vectors
- Embedding models: OpenAI, sentence-transformers, BGE
- Dimensions: 384, 768, 1024, 1536

### 8.2 Similarity Metrics
- Cosine similarity (most common for text, -1 to 1)
- Euclidean distance
- Dot product

### 8.3 Vector Databases
- Pinecone (managed, scalable)
- Chroma (lightweight, prototyping)
- Qdrant (high performance, filtering)
- FAISS (Meta, in-memory search library)
- pgvector (PostgreSQL extension)
- Milvus (scalable, production-grade)

### 8.4 Approximate Nearest Neighbors (ANN)
- HNSW (Hierarchical Navigable Small World)
- IVF (Inverted File Index)
- Product Quantization
- Trade-off: recall vs. speed

**AURA touchpoint:** ChromaDB with BGE-m3 embeddings. Hybrid retrieval (dense + BM25). Metadata filtering by language, source type, vehicle applicability.

---

## 9. RAG (RETRIEVAL-AUGMENTED GENERATION)

### 9.1 Why RAG Exists
- LLM hallucination problem
- Knowledge cutoff problem
- Grounding responses in real data

### 9.2 Indexing Pipeline
- Document loading (PDF, Word, HTML, CSV)
- Chunking strategies: fixed-size, semantic, recursive
- Chunk size trade-offs (precision vs. context)
- Chunk overlap (preventing information loss at boundaries)
- Embedding and storing in vector DB

**AURA touchpoint:** Section-aware chunking for VW service manuals, Q&A-pair preservation for forum threads, topic-segmented YouTube transcripts, structured DTC chunks. Bilingual corpus (en + pt-br) with language metadata.

### 9.3 Query Pipeline
- Query embedding
- Vector similarity search (top-K retrieval)
- Prompt construction with context
- LLM generation with grounding instructions
- Citation/source tracking

### 9.4 Retrieval Strategies
- Naive retrieval (embed → retrieve → generate)
- Hybrid search (BM25 keyword + semantic vector)
- Multi-query retrieval (LLM generates query variants)
- Parent-child retrieval (search small, return large)
- Re-ranking with cross-encoder models

### 9.5 RAG Evaluation (RAGAS Framework)
- Faithfulness: is the answer grounded in context?
- Answer relevance: does it address the question?
- Context precision: are retrieved chunks relevant?
- Context recall: were all needed chunks retrieved?

### 9.6 Hallucination Prevention
- Grounding instructions in system prompt
- Low temperature (0-0.3)
- Citation requirements
- Confidence thresholds
- Post-generation verification

### 9.7 Advanced RAG Patterns
- Agentic RAG (LLM decides which tools to use)
- Multi-step retrieval (complex questions → sub-queries)
- Self-reflection (model checks if context is sufficient)
- RAG + fine-tuning (domain behavior + knowledge retrieval)

### 9.8 RAG vs. Fine-Tuning vs. Long Context
- RAG: dynamic knowledge, citations, large corpus
- Fine-tuning: style, behavior, domain terminology
- Long context: entire document fits in window
- When to combine approaches

**AURA touchpoint:** AURA's entire AI agent core is an agentic RAG system with tool calling. The ReAct agent decides when to retrieve docs vs. read sensors vs. check maintenance schedules.

---

## 10. PROMPT ENGINEERING

### 10.1 Core Techniques
- Zero-shot prompting
- Few-shot prompting (with examples)
- Chain-of-thought (step-by-step reasoning)
- System prompts vs. user prompts

### 10.2 Structured Output
- JSON mode
- Pydantic validation
- Output parsing

### 10.3 RAG-Specific Prompting
- Grounding instructions ("answer ONLY from context")
- Citation instructions
- Handling "I don't know" cases
- Multi-hop question decomposition

---

## 11. PRACTICAL TOOLS & FRAMEWORKS

### 11.1 OpenAI API
- Chat completions endpoint
- Messages structure (system, user, assistant)
- Temperature, max_tokens, response_format
- Embeddings endpoint
- Token counting and cost awareness

### 11.2 Hugging Face Transformers
- `pipeline()` for quick inference
- `AutoTokenizer`, `AutoModel` for loading models
- Sentiment analysis, zero-shot classification, text generation
- Model Hub for browsing pre-trained models

### 11.3 LangChain
- Document loaders (PDF, text, CSV)
- Text splitters (RecursiveCharacterTextSplitter)
- Embeddings (OpenAI, HuggingFace)
- Vector stores (Chroma, Pinecone, FAISS)
- Retrievers
- Chains (RetrievalQA)
- Chat models

### 11.4 PyTorch
- Tensors and operations
- `nn.Module` for defining models
- Training loop: forward → loss → backward → step
- `model.train()` vs. `model.eval()`
- DataLoader for batching
- **Model export for inference:** `torch.jit.trace`, `torch.jit.script`, `torch.onnx.export` — converting trained models to deployment-ready formats
- **Inference mode:** `torch.no_grad()`, `torch.inference_mode()` — disabling gradient tracking for serving
- **TorchScript:** JIT compilation for production deployment without Python runtime

**AURA touchpoint:** Export anomaly detection model (MLP/decision tree) for edge deployment. Use `torch.no_grad()` in all inference paths.

### 11.5 Cloud (AWS Preferred)
- S3 (storage)
- SageMaker (model training and hosting)
- ECS/EKS (container orchestration)
- Lambda (serverless functions)
- CloudWatch (monitoring)

### 11.6 Edge & Local Inference Tools
- `llama-cpp-python`: Python bindings for llama.cpp C++ engine
- `whisper.cpp`: C++ Whisper inference for ARM/edge
- Piper TTS: local text-to-speech with multilingual support
- Silero VAD: voice activity detection
- `sentence-transformers`: local embedding inference

**AURA touchpoint:** The entire AURA edge stack — llama-cpp-python for LLM, whisper.cpp for STT, Piper for TTS, sentence-transformers for embedding.

---

## 12. SYSTEM DESIGN

### 12.1 The 7-Step Framework
1. Clarify requirements (scale, latency, constraints)
2. High-level architecture (components and data flow)
3. Data pipeline (ingestion, storage, preprocessing)
4. Model design (which models, why, trade-offs)
5. **Serving & inference** (how models are served — hardware, batching strategy, latency target, quantization level, single vs multi-model serving)
6. Monitoring & evaluation (metrics, drift, feedback)
7. Trade-offs (cost vs. quality, latency vs. accuracy, edge vs. cloud)

### 12.2 Technology Selection
- LLMs: GPT-4, Claude, LLaMA, Mistral — when to use each
- Embedding models: OpenAI, sentence-transformers, BGE
- Vector DBs: Pinecone, Chroma, Qdrant, FAISS, pgvector
- Orchestration: LangChain, LlamaIndex, Haystack
- APIs: FastAPI (async-first for ML serving)
- Containers: Docker
- Caching: Redis
- Orchestration: AWS ECS/EKS
- **Inference serving:** Triton Inference Server, vLLM, TGI — when to use each
- **Model optimization:** ONNX Runtime, TensorRT, llama.cpp — matching runtime to hardware

### 12.3 Practice Scenarios
- Chat moderation system (confirmed question)
- Customer support chatbot with RAG
- Document search and Q&A for legal/insurance
- Real-time recommendation system
- Insurance policy Q&A system (connects to your experience)
- **Edge diagnostic assistant** (AURA — resource-constrained, multi-model, real-time sensors)
- **LLM serving backend** (high-concurrency RAG system with embedding + retrieval + generation pipeline)

### 12.4 Production Concerns
- Latency requirements (p50, p95, p99)
- Cost management (LLM API costs, compute)
- Caching strategies
- Fallback behavior when model fails
- A/B testing for model versions
- Privacy and compliance (GDPR, sensitive data)
- **Throughput under concurrency** — how latency degrades as concurrent requests increase
- **Resource budgeting** — RAM ceiling, GPU memory, CPU thermal limits
- **Edge/cloud routing decisions** — complexity classification, cost thresholds, latency SLAs

---

## 13. SOFT SKILLS & INTERVIEW TECHNIQUES

### 13.1 Elevator Pitch (2 min)
- Quick introduction
- Summarized background
- Main tech stack
- One project example with business impact
- Motivation

### 13.2 CAR Framework for Projects (3 min)
- Context (30 seconds): company, project, problem
- Action (1.5 minutes): your contributions, tech, how you solved it
- Result (1 minute): business impact with numbers

### 13.3 English Skills (Factored's 4 Metrics)
- Listening: paraphrase questions to confirm understanding
- Vocabulary: use "I" and power verbs (led, implemented, resolved)
- Fluency: calm pace, clear pronunciation
- Grammar: correct verb tenses and connectors

### 13.4 Business Acumen
- Connect technical work to business outcomes
- Use numbers: revenue, cost reduction, time saved, users impacted
- Understand how business operates, not just the model

### 13.5 Communication During Coding
- Think out loud
- Explain approach before coding
- State assumptions
- Discuss time/space complexity
- Ask clarifying questions when problem is ambiguous

### 13.6 Behavioral Questions (STAR/CAR Method)
- Career transition story
- Adapting to change
- Project you're proud of
- What you'd do differently with today's technology
- Why this role, where you see yourself in 2-3 years

---

## 14. INFERENCE OPTIMIZATION & MODEL SERVING

> This section covers everything that happens after the model exists — the gap between "I can build an ML system" and "I can ship it efficiently in production." Directly relevant to AURA Phases 3–6 and to system design interviews where inference cost and latency are real constraints.

### 14.1 Model Export & Portability
- PyTorch → ONNX export pipeline (`torch.onnx.export`, dynamic axes, opset versions)
- ONNX Runtime as portable inference backend
- Graph optimizations performed during export (operator fusion, constant folding, dead code elimination)
- TorchScript (`torch.jit.trace`, `torch.jit.script`) — JIT compilation for deployment without Python
- Why ONNX matters: decouple model framework from serving hardware
- Export validation: numerical equivalence checks between PyTorch and ONNX outputs
- Dynamic vs static shapes — implications for batching and hardware optimization

**AURA touchpoint:** Export anomaly detection model to ONNX for Pi 5. Validate that ONNX output matches PyTorch output on test data.

### 14.2 Quantization
- FP32 → FP16 → INT8 → INT4 precision ladder
- Post-Training Quantization (PTQ): fast, some accuracy loss, no retraining
- Quantization-Aware Training (QAT): simulate quantization during training, better accuracy retention
- Mixed precision inference: which layers tolerate lower precision (linear layers yes, normalization layers less so)
- Accuracy vs latency vs memory tradeoffs — how to measure degradation systematically (eval before/after on held-out set)
- GGUF format for llama.cpp: Q4_K_M, Q5_K_M, Q8_0 — what the names mean
- Calibration datasets for PTQ — representative data for range estimation
- When quantization breaks: attention layers at very low precision, small models more sensitive than large

**AURA touchpoint:** GGUF quantization for Llama 3.2 3B (Q4_K_M target). Benchmark accuracy on 30 automotive diagnostic questions at Q4 vs Q5 vs Q8. Measure RAM and latency at each level on Pi 5.

### 14.3 Inference Serving
- **Triton Inference Server:** model repository structure, dynamic batching, ensemble pipelines (chaining embedding → retrieval → generation), concurrent model execution, health checks
- **vLLM:** PagedAttention, continuous batching for LLM serving, throughput optimization for high-concurrency scenarios
- **TGI (Text Generation Inference):** Hugging Face's serving solution, simpler than Triton for LLM-only workloads
- Batching strategies: static vs dynamic batching, padding tradeoffs, optimal batch size selection
- Throughput vs latency optimization — how batch size affects both inversely
- Multi-model serving: embedding model + reranker + LLM behind one endpoint — resource isolation, priority scheduling
- Model warmup: first-request latency vs steady-state
- Horizontal scaling: load balancing across multiple inference workers

**AURA touchpoint:** On Pi 5 this is simplified (single-model, no batching), but the concepts apply to cloud fallback design and to interview system design questions. Understand how a production RAG system serves 1000 concurrent users vs AURA's single-user edge setup.

### 14.4 Profiling & Benchmarking
- **Key metrics:**
  - TTFT (Time To First Token) — critical for conversational UX
  - Tokens/second (generation throughput)
  - Throughput at concurrency N (requests/second under load)
  - Peak memory (RAM/VRAM) under inference
  - P50 / P95 / P99 latency distributions
- **Bottleneck identification:** compute-bound vs memory-bandwidth-bound vs I/O-bound
  - Compute-bound: more FLOPs needed, upgrade hardware or reduce model
  - Memory-bound: model doesn't fit, optimize with quantization or offloading
  - I/O-bound: network latency, disk reads, API calls — optimize with caching, batching, async
- **Tools:**
  - `torch.profiler` for PyTorch inference paths
  - ONNX Runtime built-in profiling
  - `llama-cpp-python` timing logs (prompt eval time, token generation time)
  - Linux `htop`, `nvidia-smi`, `vmstat` for system-level monitoring
  - Custom timing decorators around pipeline stages

**AURA touchpoint:** Profile end-to-end latency per AURA tool call. Measure Pi 5 thermal throttling under sustained 30-minute inference. Benchmark TTFT and tokens/second for Llama 3.2 3B Q4 on ARM. Profile RAM: LLM + ChromaDB + Whisper + embedding model — does it fit in 8GB?

### 14.5 Edge Deployment Constraints
- **Hard constraints:** power budget (watts), thermal envelope (sustained vs burst), RAM ceiling (no swap for real-time), storage I/O speed
- **Model selection driven by hardware:** start from hardware spec, work backward to which models fit — not the other way around
- **Latency SLAs under resource constraints:** what's achievable on CPU-only edge vs GPU edge vs cloud
- **CPU vs GPU vs NPU vs dedicated accelerator tradeoffs:**
  - CPU (Pi 5): universal, cheap, slow for large models
  - GPU (Jetson Orin Nano): 10-20x faster inference, higher cost and power
  - NPU/TPU (Coral Edge TPU): offload specific workloads (STT), limited model support
- **Memory mapping (mmap):** loading models larger than available RAM by mapping from disk — latency implications
- **Thermal management:** active cooling, clock throttling, duty cycling inference
- **Multi-model resource arbitration:** when LLM + STT + TTS compete for the same RAM and CPU cycles

**AURA touchpoint:** This IS AURA Phase 3. Pi 5 8GB as hard constraint. RAM budget: Llama 3.2 3B Q4 (~2GB) + ChromaDB (~200MB) + BGE-small (~150MB) + Whisper base (~300MB) + Piper TTS (~200MB) + OS/app overhead (~1GB). Total ~4GB — fits, but no room for larger models. Thermal profiling under Brazilian summer conditions. Jetson Orin Nano as upgrade path for <3s voice-to-voice latency.

### 14.6 LLM-Specific Inference Optimization
- **KV cache:** what it is, why it matters for autoregressive generation, memory implications
- **Speculative decoding:** draft model generates candidates, large model verifies — higher throughput
- **Continuous batching:** serve multiple requests without waiting for the longest to finish
- **Context length vs memory:** how attention memory scales quadratically, techniques to manage (sliding window, sparse attention)
- **Prompt caching:** reuse KV cache for shared prompt prefixes across requests
- **Model parallelism basics:** tensor parallelism vs pipeline parallelism (relevant for multi-GPU, not edge — but asked in interviews)

**AURA touchpoint:** KV cache management on Pi 5 — context window size directly impacts RAM. Understand why a 3B model with 4K context fits but 8K context might not.

---

## 15. AURA AS INTEGRATED LEARNING GROUND

> Every section in this plan maps to an AURA component. This section makes the mapping explicit for study prioritization.

| Study Section | AURA Phase | Component |
|---------------|------------|-----------|
| §1.7 Python Scalability | Phase 1 | RAG indexing pipeline performance |
| §8 Embeddings | Phase 1 | BGE-m3, ChromaDB, hybrid retrieval |
| §9 RAG | Phase 1 | Full RAG pipeline with bilingual corpus |
| §10 Prompt Engineering | Phase 2 | ReAct agent system prompt, tool schemas |
| §5-6 DL/Transformers | Phase 2 | Understanding the LLMs being used |
| §7 LLMs | Phase 2 | Edge/cloud model selection, fine-tuning |
| §14.2 Quantization | Phase 3 | GGUF quantization for edge LLM |
| §14.4 Profiling | Phase 3 | Latency/RAM/thermal benchmarking on Pi 5 |
| §14.5 Edge Constraints | Phase 3 | Full edge deployment under hardware limits |
| §12 System Design | Phase 3 | Edge/cloud router, architecture decisions |
| §14.3 Inference Serving | Phase 3 | FastAPI serving, cloud fallback design |
| §1.7.2 Concurrency | Phases 5-6 | STT + LLM + TTS concurrent execution |
| §14.5 Multi-model arbitration | Phases 5-6 | Whisper + LLM + Piper sharing Pi 5 resources |
| §14.1 Model Export | Stretch | ONNX export for anomaly detector |
| §13 Interview Skills | Ongoing | AURA as CAR framework project story |

### Capstone Integration Project

Build the AURA RAG indexing pipeline (Phase 1) as a standalone deliverable that exercises §1.7, §8, §9, and §14.4 simultaneously:

1. Ingest 1,000+ documents (VW manuals, forums, DTCs, YouTube transcripts)
2. Chunk concurrently with `ProcessPoolExecutor` (§1.7.2)
3. Batch embedding API calls with async + rate limiting (§1.7.2)
4. Insert into ChromaDB with throughput profiling (§1.7.3)
5. Evaluate with 80+ bilingual queries — Precision@5, MRR, Hit Rate (§9.5)
6. Profile and optimize each stage (§14.4)
7. Document all benchmarks and architecture decisions

This alone is a credible portfolio artifact and interview talking point, independent of whether the full AURA system ships.

---

## Study Sequence (Recommended Order)

| Phase | Sections | Duration | Priority |
|-------|----------|----------|----------|
| Foundation | §1.1-1.6, §2, §3 | 3-4 weeks | Core — do first |
| ML/DL Theory | §4, §5, §6, §7 | 4-5 weeks | Core — concepts before implementation |
| RAG + Embeddings + Python Perf | §8, §9, §1.7 | 3-4 weeks | High — study together, implement in AURA Phase 1 |
| Prompt Eng + Tools | §10, §11 | 2 weeks | Medium — practical, learn by building |
| System Design + Inference | §12, §14 | 3-4 weeks | High — differentiator for senior roles |
| Interview Prep | §13 | Ongoing | Continuous — practice CAR stories throughout |
| **Total** | | **~16-20 weeks** | |

---

*This document is a living reference. Update benchmarks, AURA progress, and role-specific additions as the project evolves.*
