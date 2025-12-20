# A-Vietnamese-Course-Query-System-using-RAG-over-English-Knowledge-Sources

## Input Data Structure Description

Each academic course in the dataset is represented as a structured record consisting of a unique course identifier and a comprehensive textual description. The course identifier (e.g., GEO00002) serves as the primary key and ensures unambiguous reference to the corresponding academic module. The accompanying textual field aggregates all relevant academic information into a single normalized document, including course type (elective or compulsory), semester scheduling, faculty affiliation, credit value, teaching methods, assessment structure, and prerequisite requirements.

Beyond administrative metadata, the textual description encapsulates detailed pedagogical content such as course objectives, expected learning outcomes, key thematic topics, and recommended learning materials. It also includes explicit evaluation criteria, such as attendance requirements, grading thresholds, and examination weightings. This unified representation enables downstream natural language processing models to access both semantic content and institutional constraints within a single retrieval unit, facilitating accurate query matching and response generation in academic question-answering systems.

## Core Technical Contribution: Bridging Natural Queries and Structured Academic Data

The core contribution of this project extends beyond the successful development of a question-answering application. More importantly, it operationalizes and optimizes a Vietnamese natural language processing pipeline tailored for internal academic knowledge retrieval. The research addresses the critical “semantic misalignment” between students’ diverse, informal natural language queries and the rigid, standardized structure of academic regulations and course data. By introducing a hybrid architecture that integrates Retrieval-Augmented Generation (RAG) with HippoRAG, the system effectively preserves relational context during retrieval, enabling accurate normalization of course entities and academic concepts. This design significantly mitigates hallucination, which is a critical requirement for high-stakes academic advisory systems.

## Practical Impact: A Reliable Virtual Academic Assistant for Higher Education

From a practical perspective, the system functions as a reliable 24/7 virtual academic assistant with high factual accuracy. It substantially reduces administrative workload for academic staff in the Faculty of Mathematics and Informatics while offering personalized and efficient information access for students. Unlike conventional chatbot solutions, the system ensures strict alignment between generated responses and official academic records, including course codes, prerequisites, and learning outcomes. As a result, it provides trustworthy academic guidance that can be safely integrated into institutional workflows without compromising data integrity.

## Methodological Significance: Knowledge Graph RAG for Low-Resource Languages

Beyond the scope of a single academic project, this research contributes a transferable methodological framework for building Knowledge Graph–enhanced RAG systems in low-resource languages such as Vietnamese. It demonstrates that combining structured domain knowledge with large language models is essential for handling complex internal data sources that demand absolute precision. The findings suggest strong potential for extending this architecture to other specialized domains, including healthcare, legal systems, and enterprise process management, where the balance between natural language interaction and semantic correctness is both challenging and mission-critical.
## The Core Challenge: 

### 1. Balancing Natural Interaction and Data Accuracy

The primary challenge in deploying question-answering systems in the Vietnamese context lies in maintaining a balance between conversational friendliness and absolute data accuracy. While users expect natural and flexible interactions, the underlying system must strictly adhere to verified institutional data. This tension becomes particularly critical in high-stakes domains such as academic advising, where even minor inaccuracies can lead to serious consequences.

### 2. Input–Output Asymmetry in Vietnamese Academic QA Systems

On the input side, students tend to express their queries in highly variable forms of natural Vietnamese, often using informal language, abbreviations, or incomplete expressions. In contrast, the output side demands rigorous standardization: course names must precisely correspond to official course codes, and information regarding learning outcomes or prerequisite requirements must be extracted verbatim from institutional regulations. This fundamental asymmetry between flexible user queries and rigid academic data structures creates significant challenges for conventional language models.

### 3. Hallucination Risks and the Need for Semantic Control Mechanisms

The gap between informal natural language inputs and strictly standardized outputs increases the risk of hallucination in language model–based systems. Without robust semantic control mechanisms, models may generate responses that sound plausible but are factually incorrect or misaligned with official academic records. Therefore, ensuring reliable semantic grounding and controlled generation is essential for building trustworthy question-answering systems in Vietnamese academic environments.

## Team Members
- Truong Binh Ba
- Le Nguyen Thanh Tan
