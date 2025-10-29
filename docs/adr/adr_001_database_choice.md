# ADR-001: Database Choice for Semantic Search

## Status

**Status**: Accepted

## Date

**Date**: 2025-10-28

## Context

### Problem Statement
The Momentum Onboarding Platform requires a semantic search capability to allow users to find relevant information within our knowledge base (e.g., HR policies, technical documentation, setup guides) using natural language queries. A simple keyword search is insufficient as it fails to capture the user's intent. For example, a query for "how do I get paid?" should match documents titled "Understanding Your Paystub" or "Setting Up Direct Deposit." This requires storing and querying high-dimensional vector embeddings generated from our documents.

### Drivers & Constraints
*   **Driver:** Implement a powerful semantic search feature to improve user experience and information discovery.
*   **Driver:** Enable hybrid search, allowing users to filter search results by metadata (e.g., department, author, date) in addition to semantic relevance.
*   **Constraint:** The solution must be reliable and maintain high data integrity, as it is a core feature of our B2B platform.
*   **Constraint:** As a small engineering team, we must minimize operational complexity and avoid introducing new systems that require specialized maintenance skills.
*   **Constraint:** The chosen solution must be cost-effective and leverage our existing infrastructure and expertise where possible.

### Considered Options
1.  **PostgreSQL with the `pgvector` extension:** Integrate vector search capabilities directly into our primary relational database.
2.  **Specialized Vector Database (e.g., ChromaDB, FAISS):** Introduce a separate, purpose-built database dedicated to storing and querying vectors, running alongside our primary PostgreSQL database.

## Decision

We have decided to **use PostgreSQL with the `pgvector` extension** to implement semantic search capabilities.

This means we will install the `pgvector` extension into our existing PostgreSQL database. Document embeddings will be stored in a `vector` column within the same table as the source text and associated metadata. Application queries will leverage standard SQL combined with `pgvector`'s distance functions to perform efficient similarity searches.

This choice was made for the following key reasons:
1.  **Architectural Simplicity:** It allows us to maintain a single, unified data store for both relational data and vector embeddings, drastically reducing system complexity.
2.  **Operational Efficiency:** We avoid the significant overhead of deploying, monitoring, backing up, and securing a second database system, which is a critical advantage for our small team.
3.  **Data Integrity and Hybrid Search:** Storing vectors with their source data in the same transaction-safe environment eliminates data synchronization issues and enables powerful, atomic hybrid queries that combine vector search with traditional SQL `WHERE` clauses.

## Consequences

### Positive
*   **Reduced Operational Burden:** The team can leverage its existing PostgreSQL expertise and infrastructure for deployment, monitoring, and maintenance, avoiding the learning curve and operational cost of a new database technology.
*   **Guaranteed Data Consistency:** By co-locating vectors and metadata, we eliminate the entire class of problems related to keeping two separate databases in sync. Updates are atomic and ACID-compliant.
*   **Powerful, Flexible Querying:** We can immediately perform complex hybrid searches (e.g., find documents semantically similar to "time off policy" but only for the "Engineering" department and created in the last year) in a single, efficient SQL query.
*   **Mature Ecosystem:** We benefit from PostgreSQL's battle-tested reliability, security, and extensive ecosystem of tools for backups, high availability, and performance tuning.

### Negative
*   **Potential Performance Ceiling:** At an extremely large scale (hundreds of millions of vectors), a specialized vector database might offer lower latency. We accept this trade-off, as our projected scale is well within `pgvector`'s performant range.
*   **Not a Specialized Tool:** We will not have access to some of the cutting-edge indexing algorithms or the AI-native developer experience (e.g., Python-centric APIs) offered by purpose-built vector databases.
*   **Extension Management:** We are responsible for managing the `pgvector` extension's update cycle, which is separate from the core PostgreSQL release schedule. This adds a minor maintenance task.

### Neutral
*   **Schema Design Implications:** Our database schema design will now incorporate the `vector` data type and indexing strategies (e.g., HNSW, IVFFlat), which will influence the design of future data models.
*   **Monitoring Adjustments:** Existing PostgreSQL monitoring dashboards will need to be updated to track the performance of vector indexes and the resource consumption of search queries.