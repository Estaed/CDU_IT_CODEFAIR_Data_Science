# Australian Dark Sky Tourism RAG LLM Project

## Overview

This project implements a comprehensive data science solution for Australian dark sky tourism, combining data cleaning, sentiment analysis, and fine-tuned language models to provide intelligent recommendations for travelers seeking stargazing experiences.

## Project Structure

### Phase 0: Data Cleaning

**Objective**: Clean and standardize review data from multiple sources.

**Files Used**:
- `scripts/clean_google_maps.py` - Cleans Google Maps reviews
- `scripts/clean_reddit.py` - Cleans Reddit comments  
- `scripts/clean_tripadvisor.py` - Cleans TripAdvisor reviews
- `scripts/merge_reviews.py` - Combines all cleaned data

**Data Sources**:
- Google Maps reviews (6 destinations)
- Reddit comments (6 destinations)
- TripAdvisor reviews (1 unified file)

**Destinations Covered**:
- Uluru-Kata Tjuta National Park
- Kakadu National Park
- Nitmiluk (Katherine Gorge)
- Devils Marbles (Karlu Karlu)
- West MacDonnell National Park
- Alice Springs Desert Park

**Output**: Clean, unified dataset saved to `data/generate_stars/processed/reviews_unified.csv`

### Phase 1: Star Rating Generation

**Objective**: Assign 1-5 star ratings to reviews using sentiment analysis.

**File Used**: `notebooks/generate_stars.ipynb`

**Technical Implementation**:
- **Model**: `nlptown/bert-base-multilingual-uncased-sentiment`
- **Method**: BERT-based sentiment classification
- **Process**: 
  - Batch processing with GPU acceleration
  - Probability distribution over 5 sentiment classes
  - Weighted average calculation for continuous scores
  - Rounding to integer star ratings (1-5)

**Results**:
- Generated `reviews_with_stars.csv` with both float and integer ratings
- High accuracy sentiment classification
- Consistent star rating system across all platforms

### Phase 2: RAG-Enhanced LLM Fine-tuning

**Objective**: Develop an intelligent recommendation system using Retrieval-Augmented Generation (RAG) and fine-tuned language models.

**File Used**: `notebooks/finetune_rag_llm.ipynb`

**Model Architecture**:
- **Base Model**: Qwen/Qwen3-0.6B (606M parameters)
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation) with PEFT
- **Retrieval System**: Sentence-BERT embeddings with FAISS indexing
- **Evaluation**: COMET ML for automated quality assessment

**Technical Implementation**:
1. **RAG Pipeline**:
   - Document embedding using `sentence-transformers/all-MiniLM-L6-v2`
   - FAISS vector database for efficient similarity search
   - Context-aware retrieval based on user queries

2. **Model Fine-tuning**:
   - Supervised fine-tuning on 10,000 synthetic training examples
   - LoRA adapters (1.67% trainable parameters: 10M out of 606M)
   - Custom chat templates for structured JSON responses

3. **Training Process**:
   - Generated synthetic SFT data using retrieval context
   - 3 epochs with 2 batch size per device
   - Learning rate: 1e-4 with AdamW optimizer
   - TensorBoard logging and evaluation

**Key Features**:
- **Source Attribution**: Shows which reviews inform recommendations
- **Context-Aware Responses**: Uses relevant review content for answers
- **Multi-Platform Integration**: Leverages data from all review sources
- **Real-time Retrieval**: Dynamic context selection based on queries

## Results and Performance

**Model Capabilities**:
- Answers questions about Australian dark sky destinations
- Provides specific recommendations based on review data
- Cites source reviews for transparency
- Handles various query types (activities, weather, family-friendly options)

**Evaluation Metrics**:
- COMET ML scoring for response quality
- Retrieval accuracy assessment
- User satisfaction through interactive testing

**Sample Queries Handled**:
- "Best waterfalls and swimming spots"
- "Family-friendly walks and sunset views"
- "Places that are not too hot"
- "Cultural experiences and wildlife viewing"
- "Scenic drives and photography spots"

## Technical Stack

- **Python 3.12**
- **Transformers & PEFT**: Model fine-tuning
- **FAISS**: Vector similarity search
- **Sentence-BERT**: Text embeddings
- **COMET ML**: Model evaluation
- **Jupyter Notebooks**: Development environment

## File Structure

```
├── data/
│   ├── raw_data/           # Original review data
│   ├── generate_stars/     # Processed data with star ratings
│   └── rag_llm/           # RAG training data
├── models/
│   └── rag_llm/           # Fine-tuned model files
├── notebooks/             # Jupyter notebooks
├── scripts/               # Data processing scripts
└── final.zip             # Compressed model files for GitHub
```

## Usage

1. **Data Processing**: Run notebooks in `notebooks/` directory
2. **Model Training**: Execute `finetune_rag_llm.ipynb`
3. **Model Loading**: The notebook automatically extracts model files from ZIP
4. **Interactive Testing**: Use the built-in chat interface

## Key Achievements

1. **Comprehensive Data Pipeline**: Successfully processed multi-source review data
2. **Advanced ML Implementation**: Implemented RAG + fine-tuned LLM architecture
3. **Production-Ready Solution**: Created deployable recommendation system
4. **Transparent AI**: Source attribution for all recommendations
5. **Scalable Architecture**: Modular design for easy extension

## Future Enhancements

- Real-time data updates from review platforms
- Multi-language support for international tourists
- Integration with booking systems
- Mobile application development
- Advanced personalization features

## Contributors

- **Data Science Team**: Charles Darwin University IT Code Fair 2025
- **Project Focus**: Australian Dark Sky Tourism Intelligence

---

*This project demonstrates the power of combining traditional data science techniques with modern language models to create intelligent, context-aware recommendation systems for the tourism industry.*