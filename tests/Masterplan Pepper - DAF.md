---
up: "[[Dev/20 - Garage/64 - Streamlit/Markdown to Word/Markdown to Word|Markdown to Word]]"  # hub
---
# Masterplan Jarvis - Dossier d'Architecture Fonctionnelle

**Date:** 2025-12-03  
**Version:** 1.0 - Draft  
**Owner:** Eric TAYLOR  
**Scope:** Système RAG intelligent pour automatisation réponses AO et valorisation expertise interne

**Nom de Projet:** PEPPER
Project Experience & Past PErformance Repository

---

## 1. Vision Stratégique et Objectifs

### 1.1 Problématique Métier

**Pain Points identifiés :**
- Temps excessif passé à rechercher les expériences pertinentes dans MyInfogene et BoondManager
- Reformulation manuelle et chronophage des références pour chaque AO
- Perte de connaissance lors des départs/mobilités
- Manque de capitalisation sur les succès passés
- Difficultés à croiser les expertises entre filiales/entités

**Impact Business :**
- Coût : ~2-3 jours par réponse AO en recherche et reformulation
- Qualité : références parfois incomplètes ou sous-optimales faute de temps
- Compétitivité : délais de réponse pénalisants sur appels d'offres rapides

### 1.2 Vision Cible

**Jarvis devient l'assistant IA qui :**
- Répond instantanément "Quelles sont nos expériences pertinentes sur [sujet X] pour [client Y] ?"
- Reformule automatiquement les expériences au bon niveau de détail selon le contexte
- Maintient à jour une base de connaissances vivante depuis nos systèmes source
- S'adapte aux permissions et aux périmètres métier de chaque utilisateur

**ROI Attendu :**
- Gain de temps : 60-80% sur la phase de recherche d'expériences (1.5-2 jours → 4-6h)
- Qualité : +30% de références exploitables par AO grâce à l'exhaustivité
- Réactivité : réponse aux demandes de pré-qualification en < 2h au lieu de 1-2 jours

---

## 2. Fonctionnalités Essentielles

### 2.1 Gestion des Collections Documentaires

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **Ingestion automatique** | Connexion API vers MyInfogene, BoondManager, SharePoint, Teams | P0 |
| **Chunking intelligent** | Découpage sémantique des documents (Docling) | P0 |
| **Mise à jour incrémentale** | Synchronisation quotidienne/hebdomadaire des modifications | P0 |
| **Gestion des versions** | Historisation des changements avec traçabilité | P1 |
| **Détection de doublons** | Identification des contenus similaires | P1 |
| **Enrichissement métadonnées** | Extraction automatique tags, dates, acteurs, clients | P1 |
| **OCR avancé** | Reconnaissance texte dans images/PDF scannés | P2 |

### 2.2 Recherche et Récupération (RAG Core)

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **Recherche sémantique** | Embedding + similarité vectorielle (Qdrant) | P0 |
| **Recherche hybride** | Combinaison sémantique + keyword + filtres métadonnées | P0 |
| **RAG Direct** | Récupération simple + LLM | P0 |
| **CQR (Contextual Query Reformulation)** | Reformulation requête selon contexte | P0 |
| **HyDE (Hypothetical Document Embeddings)** | Génération réponse hypothétique pour améliorer recherche | P1 |
| **Fusion RAG** | Combinaison multi-stratégies pour résultats optimaux | P1 |
| **Auto-sélection stratégie** | IA choisit automatiquement le meilleur pattern RAG | P1 |
| **Re-ranking** | Réordonnancement résultats par pertinence contextuelle | P1 |
| **Citation précise** | Référencement source avec numéros de page/section | P0 |

### 2.3 Génération et Reformulation

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **Synthèse multi-sources** | Agrégation intelligente de plusieurs expériences | P0 |
| **Adaptation au contexte** | Reformulation selon type AO (public/privé, taille, secteur) | P0 |
| **Ajustement niveau détail** | Version executive summary vs. détaillée technique | P0 |
| **Multi-langue** | Support FR/EN natif, autres langues en P2 | P1 |
| **Respect templates** | Adaptation format selon modèles AO standards | P1 |
| **Anonymisation** | Masquage informations sensibles si requis | P2 |

### 2.4 Gestion des Permissions et Sécurité

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **SSO Azure/Entra** | Authentification unique entreprise | P0 |
| **Collections publiques** | Visibles par tout le groupe | P0 |
| **Collections équipe** | Limitées aux membres Teams/AD groups | P0 |
| **Collections privées** | Accessibles uniquement au créateur | P0 |
| **Collections entité** | Périmètre filiale/société (Infogene, Vulcain, etc.) | P1 |
| **Héritage permissions** | Alignement sur droits sources (SharePoint, Teams) | P1 |
| **Audit trail** | Logs complets d'accès et d'utilisation | P0 |
| **Chiffrement au repos** | Données sensibles chiffrées dans Qdrant | P1 |
| **Filtrage automatique** | Utilisateur ne voit que ce qu'il a le droit de voir | P0 |

### 2.5 Expérience Utilisateur

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **Interface Chat** | Conversation naturelle type ChatGPT | P0 |
| **Interface MCP** | Intégration dans outils agentiques (Claude, etc.) | P1 |
| **Suggestions auto** | Propositions de questions/recherches fréquentes | P1 |
| **Historique conversations** | Reprise contexte sessions précédentes | P0 |
| **Export résultats** | Word/PDF/Markdown avec mise en forme | P0 |
| **Feedback utilisateur** | Notation pertinence (👍👎) pour amélioration continue | P1 |
| **Mode "Quick Search"** | Recherche rapide sans conversation complète | P2 |

### 2.6 Administration et Monitoring

| Fonction | Description | Priorité |
|----------|-------------|----------|
| **Dashboard admin** | Vue d'ensemble utilisation, performance, santé système | P0 |
| **Gestion collections** | Création, modification, suppression par admins | P0 |
| **Monitoring temps réel** | Latence, disponibilité, erreurs | P0 |
| **Analytics usage** | Qui utilise quoi, quand, comment | P1 |
| **Gestion modèles LLM** | Switch entre Llama 3.2, Llama 4, GPT-OSS-20B | P1 |
| **Backup & Recovery** | Sauvegarde Qdrant, restauration rapide | P0 |
| **Scaling manuel/auto** | Ajout ressources selon charge | P1 |
| **Cost tracking** | Suivi coûts infrastructure et tokens | P2 |

### 2.7 Intégrations et Connecteurs

| Système Source | Type d'intégration | Données récupérées | Priorité |
|----------------|-------------------|-------------------|----------|
| **MyInfogene** | API REST | Projets, missions, compétences, CV | P0 |
| **BoondManager** | API REST | Opportunités, clients, propositions commerciales | P0 |
| **SharePoint** | MS Graph API | Documents techniques, présentations, rapports | P1 |
| **Teams** | MS Graph API | Conversations, décisions, fichiers partagés | P1 |
| **Confluence** | API REST | Documentation projets, wikis internes | P2 |
| **Jira** | API REST | Tickets, problèmes résolus, solutions techniques | P2 |
| **Email (Exchange)** | MS Graph API | Emails référents clients avec attachements | P2 |
| **n8n Workflows** | Webhook/API | Orchestration mises à jour et pipelines ETL | P0 |

---

## 3. Cartographie des Systèmes et Interfaces

### 3.1 Vue d'Ensemble de l'Écosystème

```mermaid
graph TB
    subgraph "Utilisateurs"
        U1[Chef de Projet]
        U2[Commercial]
        U3[Ingénieur]
        U4[Direction]
    end
    
    subgraph "Points d'Entrée"
        UI[Interface Web Jarvis]
        MCP[MCP Server - IA Agentique]
        API[API REST Publique]
    end
    
    subgraph "Couche Application"
        AUTH[Authentification SSO]
        PERM[Gestionnaire Permissions]
        CHAT[Moteur Conversationnel]
        RAG[Moteur RAG Intelligent]
        GEN[Générateur Réponses]
    end
    
    subgraph "Couche Données"
        QDRANT[(Qdrant Vector DB)]
        CACHE[(Redis Cache)]
        LOGS[(Logs & Analytics)]
        CONV[(Historique Conversations)]
    end
    
    subgraph "Orchestration"
        N8N[n8n Workflows]
        SCHEDULER[Planificateur Tâches]
    end
    
    subgraph "Systèmes Sources"
        MYINFO[MyInfogene]
        BOOND[BoondManager]
        SP[SharePoint]
        TEAMS[Teams]
        CONF[Confluence]
    end
    
    subgraph "Infrastructure"
        LLM1[Llama 3.2]
        LLM2[Llama 4]
        LLM3[GPT-OSS-20B]
        EMBED[Embeddings Service]
    end
    
    U1 & U2 & U3 & U4 --> UI & MCP
    UI & MCP & API --> AUTH
    AUTH --> PERM
    PERM --> CHAT & RAG
    CHAT --> RAG --> GEN
    RAG <--> QDRANT
    RAG <--> CACHE
    CHAT <--> CONV
    GEN --> LLM1 & LLM2 & LLM3
    RAG --> EMBED
    
    N8N --> SCHEDULER
    SCHEDULER --> MYINFO & BOOND & SP & TEAMS & CONF
    MYINFO & BOOND & SP & TEAMS & CONF --> N8N
    N8N --> EMBED --> QDRANT
    
    CHAT & RAG & GEN --> LOGS
    
    style QDRANT fill:#ff6b6b
    style N8N fill:#ff9ff3
    style RAG fill:#95e1d3
    style AUTH fill:#feca57
```

### 3.2 Flux de Données - Ingestion

```mermaid
sequenceDiagram
    participant N8N
    participant Source as MyInfogene/Boond
    participant Processor as Document Processor
    participant Embed as Embeddings
    participant Qdrant
    participant Notif as Notifications
    
    N8N->>Source: GET /api/projects (modifiés depuis T-1)
    Source-->>N8N: JSON projets + métadonnées
    N8N->>Processor: Envoie documents bruts
    Processor->>Processor: Chunking intelligent (Docling)
    Processor->>Embed: Chunks + métadonnées
    Embed->>Embed: Génération embeddings
    Embed->>Qdrant: Upsert vectors + metadata
    Qdrant-->>Embed: Confirmation
    Embed-->>N8N: Succès ingestion
    N8N->>Notif: Notification admins (si erreurs)
```

### 3.3 Flux de Requête Utilisateur

```mermaid
sequenceDiagram
    participant User
    participant UI as Interface Jarvis
    participant Auth as SSO/Permissions
    participant Chat as Chat Engine
    participant RAG as RAG Engine
    participant LLM
    participant Qdrant
    
    User->>UI: "Nos expériences en cybersécurité pour banques"
    UI->>Auth: Vérification token + permissions
    Auth-->>UI: User context + accessible collections
    UI->>Chat: Query + context + history
    Chat->>RAG: Requête enrichie
    RAG->>RAG: Sélection stratégie (CQR/HyDE/Fusion)
    RAG->>Qdrant: Recherche vectorielle avec filtres permissions
    Qdrant-->>RAG: Top-K documents pertinents
    RAG->>RAG: Re-ranking + citation
    RAG->>LLM: Contexte + documents + instructions
    LLM-->>RAG: Réponse générée avec citations
    RAG-->>Chat: Réponse structurée
    Chat-->>UI: Réponse formatée + sources
    UI-->>User: Affichage conversationnel
```

### 3.4 Matrice des Interfaces

| Interface | Protocole | Authentification | Fréquence | Criticité |
|-----------|-----------|------------------|-----------|-----------|
| **MyInfogene → Jarvis** | REST API | OAuth 2.0 | Quotidien | Haute |
| **BoondManager → Jarvis** | REST API | API Key | Quotidien | Haute |
| **SharePoint → Jarvis** | MS Graph | Azure AD | Hebdo | Moyenne |
| **Teams → Jarvis** | MS Graph | Azure AD | Hebdo | Basse |
| **n8n → Jarvis** | Webhook | JWT | Temps réel | Haute |
| **Jarvis → Qdrant** | gRPC | Internal | Temps réel | Critique |
| **Jarvis → LLMs** | HTTP | Internal | Temps réel | Critique |
| **User → Jarvis** | HTTPS | SSO Azure | Temps réel | Critique |
| **MCP Server → Jarvis** | REST | Bearer Token | Temps réel | Haute |

---

## 4. Trois Architectures Proposées

### 4.1 Architecture A - "Monolithique Scalable"

**Principe:** Une application tout-en-un avec scaling horizontal classique.

```mermaid
graph TB
    subgraph "Load Balancing"
        LB[HAProxy / Nginx]
    end
    
    subgraph "Application Tier - Instances Multiples"
        APP1[Jarvis App Instance 1<br/>FastAPI + RAG + Chat]
        APP2[Jarvis App Instance 2<br/>FastAPI + RAG + Chat]
        APP3[Jarvis App Instance N<br/>FastAPI + RAG + Chat]
    end
    
    subgraph "Data Tier"
        QDRANT1[(Qdrant Primary)]
        QDRANT2[(Qdrant Replica 1)]
        QDRANT3[(Qdrant Replica 2)]
        REDIS[(Redis Cluster)]
        POSTGRES[(PostgreSQL<br/>Metadata + Logs)]
    end
    
    subgraph "LLM Tier"
        LLM_POOL[LLM Pool<br/>Llama 3.2, 4, GPT-OSS]
    end
    
    subgraph "ETL"
        N8N_CLUSTER[n8n Cluster]
    end
    
    LB --> APP1 & APP2 & APP3
    APP1 & APP2 & APP3 --> QDRANT1
    QDRANT1 <--> QDRANT2 & QDRANT3
    APP1 & APP2 & APP3 <--> REDIS
    APP1 & APP2 & APP3 --> POSTGRES
    APP1 & APP2 & APP3 --> LLM_POOL
    N8N_CLUSTER --> QDRANT1
```

**Avantages:**
- ✅ Simple à déployer et maintenir
- ✅ Faible latence (tout dans un process)
- ✅ Facile à déboguer
- ✅ Coût infrastructure réduit (peu de composants)

**Inconvénients:**
- ❌ Scaling limité (réplication complète à chaque instance)
- ❌ Difficulté à scale indépendamment RAG vs Chat vs API
- ❌ Risque de saturation si un composant consomme trop (ex: embeddings)
- ❌ Mise à jour = redéploiement complet

**Recommandé pour:**
- MVP et Phase 1 (< 100 utilisateurs simultanés)
- Équipe technique réduite
- Budget infrastructure contraint

**Capacité:**
- 50-150 utilisateurs simultanés
- ~1000 requêtes/jour
- SLA 99.5%

---

### 4.2 Architecture B - "Microservices Modulaires"

**Principe:** Découpage fonctionnel avec services indépendants et scaling granulaire.

```mermaid
graph TB
    subgraph "API Gateway"
        GATEWAY[API Gateway + Auth]
    end
    
    subgraph "Frontend Services"
        CHAT_SVC[Chat Service<br/>Node.js]
        API_SVC[Public API<br/>FastAPI]
        MCP_SVC[MCP Server<br/>Python]
    end
    
    subgraph "Core Services"
        RAG_SVC[RAG Service<br/>Python FastAPI]
        EMBED_SVC[Embedding Service<br/>Python]
        RERANK_SVC[Re-ranking Service<br/>Python]
        GEN_SVC[Generation Service<br/>Python]
    end
    
    subgraph "Data Services"
        QDRANT_CLUSTER[(Qdrant Cluster<br/>3 nodes)]
        REDIS_CLUSTER[(Redis Cluster<br/>Sentinel)]
        POSTGRES[(PostgreSQL HA<br/>Primary + Replica)]
    end
    
    subgraph "Background Services"
        ETL_SVC[ETL Service<br/>n8n]
        SCHEDULER[Scheduler<br/>Airflow/Temporal]
        MONITOR[Monitoring<br/>Prometheus + Grafana]
    end
    
    subgraph "LLM Infrastructure"
        LLM_GATEWAY[LLM Gateway<br/>LiteLLM]
        LLM_NODES[LLM Nodes Pool]
    end
    
    GATEWAY --> CHAT_SVC & API_SVC & MCP_SVC
    CHAT_SVC & API_SVC & MCP_SVC --> RAG_SVC
    RAG_SVC --> EMBED_SVC & RERANK_SVC
    RAG_SVC --> QDRANT_CLUSTER
    RAG_SVC --> GEN_SVC
    GEN_SVC --> LLM_GATEWAY
    LLM_GATEWAY --> LLM_NODES
    
    EMBED_SVC --> REDIS_CLUSTER
    CHAT_SVC & API_SVC --> REDIS_CLUSTER
    
    ETL_SVC --> EMBED_SVC
    ETL_SVC --> QDRANT_CLUSTER
    SCHEDULER --> ETL_SVC
    
    CHAT_SVC & RAG_SVC & GEN_SVC --> POSTGRES
    MONITOR --> CHAT_SVC & RAG_SVC & GEN_SVC & QDRANT_CLUSTER
```

**Avantages:**
- ✅ Scaling indépendant par service (ex: 5 instances RAG, 2 instances Chat)
- ✅ Haute disponibilité (panne d'un service ≠ panne totale)
- ✅ Évolutivité technologique (remplacer un service sans tout casser)
- ✅ Isolation des problèmes (bug dans Embedding ≠ bug dans Chat)
- ✅ Équipes peuvent travailler en parallèle sur services différents

**Inconvénients:**
- ❌ Complexité opérationnelle élevée
- ❌ Latence réseau entre services
- ❌ Nécessite orchestration Kubernetes
- ❌ Debugging plus complexe (traces distribuées requises)
- ❌ Coût infrastructure plus élevé

**Recommandé pour:**
- Phase 2-3 (> 200 utilisateurs)
- Équipe DevOps dédiée
- Besoin de scale à grande échelle
- Plusieurs équipes de développement

**Capacité:**
- 200-1000+ utilisateurs simultanés
- 10k-50k requêtes/jour
- SLA 99.9%

---

### 4.3 Architecture C - "Hybride Pragmatique"

**Principe:** Monolithe pour les fonctions principales + services spécialisés pour charges intensives.

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[HAProxy]
    end
    
    subgraph "Application Monolith - Multiple Instances"
        CORE1[Jarvis Core App 1<br/>FastAPI: API + Chat + RAG Logic]
        CORE2[Jarvis Core App 2<br/>FastAPI: API + Chat + RAG Logic]
    end
    
    subgraph "Specialized Heavy Services"
        EMBED_CLUSTER[Embedding Service<br/>GPU-enabled<br/>Auto-scaled 1-5 instances]
        LLM_GATEWAY[LLM Gateway<br/>Load balancer vers models]
    end
    
    subgraph "Data Layer"
        QDRANT_PRIMARY[(Qdrant Primary)]
        QDRANT_REPLICAS[(Qdrant Replicas x2)]
        REDIS[(Redis Sentinel)]
        POSTGRES[(PostgreSQL<br/>Replication)]
    end
    
    subgraph "Background Jobs"
        N8N[n8n Cluster<br/>2 instances]
        WORKER_POOL[Celery Workers<br/>Pour jobs longs]
    end
    
    subgraph "LLM Pool"
        LLM1[Llama 3.2]
        LLM2[Llama 4]
        LLM3[GPT-OSS-20B]
    end
    
    LB --> CORE1 & CORE2
    CORE1 & CORE2 --> EMBED_CLUSTER
    CORE1 & CORE2 --> LLM_GATEWAY
    CORE1 & CORE2 --> QDRANT_PRIMARY
    QDRANT_PRIMARY <--> QDRANT_REPLICAS
    CORE1 & CORE2 <--> REDIS
    CORE1 & CORE2 --> POSTGRES
    
    LLM_GATEWAY --> LLM1 & LLM2 & LLM3
    
    N8N --> EMBED_CLUSTER
    N8N --> QDRANT_PRIMARY
    CORE1 & CORE2 --> WORKER_POOL
    WORKER_POOL --> POSTGRES
```

**Avantages:**
- ✅ Équilibre complexité/performance
- ✅ Services lourds (Embeddings, LLM) isolés et scalables indépendamment
- ✅ Core app simple à maintenir
- ✅ Coûts maîtrisés (scale uniquement ce qui coûte cher)
- ✅ Migration progressive possible (monolithe → microservices)

**Inconvénients:**
- ⚠️ Nécessite quand même orchestration pour services spécialisés
- ⚠️ Complexité intermédiaire
- ⚠️ Risque de "monolithe qui grossit" si pas de discipline

**Recommandé pour:**
- Transition Phase 1 → Phase 2
- Équipe technique de taille moyenne
- Besoins de scaling progressif
- **→ Recommandation pour Infogene**

**Capacité:**
- 100-500 utilisateurs simultanés
- 5k-20k requêtes/jour
- SLA 99.7%

---

## 5. Comparaison et Recommandation

### 5.1 Matrice de Décision

| Critère | Architecture A<br/>Monolithique | Architecture B<br/>Microservices | Architecture C<br/>Hybride |
|---------|--------------------------------|----------------------------------|---------------------------|
| **Complexité déploiement** | ⭐⭐⭐⭐⭐ Très Simple | ⭐⭐ Complexe | ⭐⭐⭐⭐ Simple |
| **Scalabilité** | ⭐⭐⭐ Limitée | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐⭐ Bonne |
| **Coût infrastructure** | ⭐⭐⭐⭐⭐ Minimal | ⭐⭐ Élevé | ⭐⭐⭐⭐ Modéré |
| **Maintenabilité** | ⭐⭐⭐ Moyenne | ⭐⭐⭐⭐ Bonne | ⭐⭐⭐⭐ Bonne |
| **Performance** | ⭐⭐⭐⭐ Bonne | ⭐⭐⭐⭐ Bonne | ⭐⭐⭐⭐⭐ Excellente |
| **Temps de mise en œuvre** | ⭐⭐⭐⭐⭐ Rapide (1-2 mois) | ⭐⭐ Long (4-6 mois) | ⭐⭐⭐⭐ Raisonnable (2-3 mois) |
| **Compétences requises** | ⭐⭐⭐⭐ Basiques | ⭐⭐ Avancées (K8s) | ⭐⭐⭐ Intermédiaires |
| **Haute disponibilité** | ⭐⭐⭐ Moyenne | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐⭐ Bonne |
| **Évolutivité future** | ⭐⭐ Limitée | ⭐⭐⭐⭐⭐ Illimitée | ⭐⭐⭐⭐ Très bonne |

### 5.2 Recommandation : Architecture C - Hybride Pragmatique

**Justification:**

1. **Aligné avec la maturité actuelle**
   - Équipe AI actuelle : 1 Lead Dev + 2 apprentis (disponibilité alternée)
   - Infrastructure existante : Docker Compose → Migration progressive possible
   - Pas besoin de Kubernetes expertise immédiate

2. **Répond aux besoins business**
   - Peut gérer 100-500 utilisateurs (objectif 2025-2026)
   - SLA 99.7% suffisant pour usage interne
   - Performance excellente pour cas d'usage AO (latence critique)

3. **Optimise les coûts**
   - Services lourds (Embeddings GPU) scalent indépendamment
   - Pas de surcoût microservices complet
   - Possibilité d'optimiser selon utilisation réelle

4. **Permet l'évolution**
   - Migration vers microservices possible si besoin (Phase 3)
   - Core app reste simple pendant scale-up
   - Découplage services coûteux = flexibilité budgétaire

**Prérequis techniques:**
- Docker Swarm OU Kubernetes léger (k3s) pour orchestration
- Qdrant en cluster (minimum 3 nodes)
- Redis Sentinel pour cache HA
- PostgreSQL avec replication (Primary + 1 Replica)
- Monitoring Prometheus + Grafana

---

## 6. Roadmap d'Implémentation

### Phase 1 - MVP Fonctionnel (Q1 2025 - 3 mois)

**Objectifs:**
- Système RAG opérationnel sur MyInfogene et BoondManager
- Interface Chat basique
- Collections publiques et privées
- Authentification SSO

**Deliverables:**
- ✅ Architecture C déployée en mode simplifié (sans scaling automatique)
- ✅ Connecteurs MyInfogene + BoondManager opérationnels
- ✅ RAG Direct + CQR fonctionnels
- ✅ Interface Web Streamlit/Gradio
- ✅ Qdrant 3-nodes cluster
- ✅ Authentification Azure AD
- ✅ 10-20 utilisateurs pilotes (équipe pré-vente)

**Ressources:**
- Lead Dev : architecture + RAG core
- Dev 1 : n8n pipelines + connecteurs API
- Dev 2 : Frontend + Auth SSO
- Eric : Product Owner + tests utilisateurs

### Phase 2 - Enrichissement et Scale (Q2-Q3 2025 - 4 mois)

**Objectifs:**
- Stratégies RAG avancées (HyDE, Fusion)
- Collections par équipes Teams
- MCP Server pour IA agentique
- Intégrations SharePoint/Teams
- Scaling automatique composants critiques

**Deliverables:**
- ✅ Auto-sélection stratégie RAG par IA
- ✅ Permissions granulaires via Azure/Entra
- ✅ Collections équipes synchronisées avec Teams
- ✅ Interface MCP opérationnelle
- ✅ Connecteurs SharePoint + Teams
- ✅ Auto-scaling Embedding Service (1-5 instances)
- ✅ 50-100 utilisateurs actifs

**Ressources:**
- Lead Dev : RAG avancé + MCP
- Dev 1 : Permissions + connecteurs MS Graph
- Dev 2 : Scaling + monitoring
- + 1 DevOps externe (3 mois) pour infra scaling

### Phase 3 - Production et Groupe (Q4 2025 - 3 mois)

**Objectifs:**
- Rollout toutes filiales Vulcain
- Collections par entité juridique
- Interface production Vue.js
- Intégrations Confluence/Jira
- SLA 99.9%

**Deliverables:**
- ✅ Multi-tenancy par filiale
- ✅ Interface Vue.js production
- ✅ Connecteurs Confluence + Jira
- ✅ Dashboard analytics avancés
- ✅ Documentation complète
- ✅ Formation utilisateurs (10 sessions)
- ✅ 200-300 utilisateurs groupe

**Ressources:**
- Équipe AI complète
- + 1 DevOps permanent
- + Support formation/change management

### Jalons Critiques

| Jalon | Date Cible | Critère de Succès |
|-------|-----------|-------------------|
| **POC validé** | Fin Janvier 2025 | 5 réponses AO réussies avec Jarvis |
| **MVP Production** | Fin Mars 2025 | 20 utilisateurs quotidiens, SLA > 99% |
| **Scale Infogene** | Fin Juin 2025 | 100 utilisateurs, 500 requêtes/jour |
| **Rollout Groupe** | Fin Décembre 2025 | 300 utilisateurs, 2000 requêtes/jour |

---

## 7. Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Disponibilité équipe** (apprentis alternance) | Haute | Moyen | Planning ajusté sur semaines présence, documentation exhaustive |
| **Performance Qdrant** (volumétrie MyInfogene) | Moyenne | Haute | Benchmark dès POC, plan B vers Weaviate/Milvus |
| **Qualité connecteurs API** (changements MyInfogene) | Moyenne | Haute | Versioning API, tests automatisés, fallback manuel |
| **Latence LLM** (charge simultanée) | Moyenne | Moyenne | Queue system (Celery), cache Redis agressif |
| **Complexité permissions** (matrice entités/équipes) | Haute | Haute | Phase par phase (Publique → Privée → Équipe → Entité) |
| **Adoption utilisateurs** | Moyenne | Haute | Change management, formation, quick wins visibles |

---

## 8. Budget Prévisionnel (Architecture C)

### Infrastructure Année 1

| Poste | Coût Mensuel | Coût Annuel | Note |
|-------|--------------|-------------|------|
| **Serveurs Application** (2x 16 vCPU, 64GB RAM) | 800€ | 9,600€ | On-prem ou VM dédiées |
| **Serveur Embeddings** (1x GPU T4, 32GB RAM) | 600€ | 7,200€ | Scaling 1-5 selon charge |
| **Cluster Qdrant** (3x 8 vCPU, 32GB RAM, SSD 500GB) | 900€ | 10,800€ | |
| **Redis + PostgreSQL** (HA) | 300€ | 3,600€ | |
| **Monitoring** (Prometheus, Grafana, logs) | 200€ | 2,400€ | |
| **Backup & Storage** (2TB) | 150€ | 1,800€ | |
| **Total Infrastructure** | **2,950€/mois** | **35,400€/an** | |

### Licences et Services

| Poste | Coût Annuel |
|-------|-------------|
| **n8n Self-Hosted** | 0€ (OSS) |
| **Qdrant** | 0€ (OSS) |
| **Azure AD/Entra** (SSO) | Inclus licences M365 |
| **API MyInfogene** | 0€ (interne) |
| **API BoondManager** | 0€ (existant) |

### Ressources Humaines Année 1

| Poste | Coût |
|-------|------|
| **Lead Dev** (fulltime) | Budget RH existant |
| **Dev 1 + Dev 2** (apprentis alternance) | Budget RH existant |
| **DevOps externe** (3 mois, Phase 2) | 25,000€ |
| **Formation & Change Mgmt** | 10,000€ |
| **Total RH additionnel** | **35,000€** |

**Budget Total Année 1: ~70,000€**

---

## 9. Indicateurs de Performance (KPIs)

### KPIs Techniques

| Métrique | Cible MVP | Cible Production |
|----------|-----------|------------------|
| **Latence moyenne requête simple** | < 1s | < 500ms |
| **Latence requête complexe** (multi-docs) | < 3s | < 2s |
| **Disponibilité système** | 99.5% | 99.7% |
| **Temps indexation 1000 documents** | < 15 min | < 10 min |
| **Précision RAG** (pertinence top-3) | > 70% | > 85% |
| **Taux d'erreur** | < 1% | < 0.5% |

### KPIs Business

| Métrique | Cible Année 1 |
|----------|---------------|
| **Utilisateurs actifs mensuels** | 150 |
| **Requêtes par utilisateur/semaine** | 10 |
| **Gain temps recherche AO** | 60% (2j → 0.8j) |
| **Taux satisfaction utilisateurs** | > 4/5 |
| **Nombre AO soutenus** | 50 |
| **ROI perçu** | Positif sur 80% utilisateurs |

---

## 10. Prochaines Étapes

### Semaine 1-2 (Décembre 2025)
- [ ] Validation DAF par Direction
- [ ] Commande matériel (GPU, serveurs si nécessaire)
- [ ] Kick-off projet avec équipe élargie
- [ ] Setup environnement développement

### Semaine 3-4 (Décembre-Janvier)
- [ ] Architecture détaillée technique
- [ ] POC connecteur MyInfogene
- [ ] Setup Qdrant cluster
- [ ] Premiers tests RAG sur données réelles

### Janvier 2025
- [ ] Sprint 1 : Connecteurs MyInfogene + BoondManager
- [ ] Sprint 2 : RAG Direct + CQR
- [ ] Sprint 3 : Interface Chat basique
- [ ] Sprint 4 : SSO + Collections publiques/privées

### Février 2025
- [ ] Tests internes équipe AI
- [ ] Pilote 10 utilisateurs pré-vente
- [ ] Ajustements feedback
- [ ] Préparation communication interne

### Mars 2025
- [ ] Lancement MVP production
- [ ] Formation 20 premiers utilisateurs
- [ ] Monitoring intensif
- [ ] Planification Phase 2

---

**Document préparé par:** Eric TAYLOR, CAIO Infogene  
**Dernière mise à jour:** 2025-12-03  
**Statut:** Draft v1.0 - En attente validation

**Contacts:**
- Architecture : Eric TAYLOR
- Développement : [Lead Dev Name]
- Infrastructure : [DevOps Contact]

---

## Annexes

### A. Glossaire

- **RAG (Retrieval-Augmented Generation)** : Technique combinant recherche documentaire et génération par LLM
- **CQR (Contextual Query Reformulation)** : Reformulation automatique requête selon contexte
- **HyDE (Hypothetical Document Embeddings)** : Génération réponse hypothétique pour améliorer recherche
- **Fusion RAG** : Combinaison de plusieurs stratégies RAG
- **Embedding** : Représentation vectorielle d'un texte
- **Qdrant** : Base de données vectorielle open-source
- **MCP (Model Context Protocol)** : Protocole pour connexion IA agentique

### B. Références Techniques

- Docling: https://github.com/DS4SD/docling
- Qdrant: https://qdrant.tech/
- n8n: https://n8n.io/
- FastAPI: https://fastapi.tiangolo.com/
- LiteLLM: https://github.com/BerriAI/litellm

### C. Standards et Normes

- RGPD : Compliance totale via on-premise et SSO
- ISO 27001 : Audit trail, chiffrement, gestion permissions
- Accessibilité WCAG 2.1 : Interface web conforme niveau AA

<!-- hub-related:start -->
⬆ [Markdown to Word](../Markdown%20to%20Word.md)

## Voir aussi

_Liens générés par `hub-related` (GLaDOS), entre ces balises._

- [Masterplan Pepper - DAF](../../../../01%20-%20AI%20Route%202026/00%20Projects/10%20-%20PEPPER/Documentation/Basics/Masterplan%20Pepper%20-%20DAF.md) — Version parallèle du même DAF PEPPER, utile pour comparer architecture et périmètre.
- [Masterplan Pepper - Outline](Documentation/AI%20Projects/Projets/PEPPER/Masterplan%20Pepper%20-%20Outline.md) — Plan d’ensemble du projet PEPPER, complète le dossier d’architecture fonctionnelle.
- [00 - Contexte et Référentiel PEPPER](../../../../01%20-%20AI%20Route%202026/00%20Projects/10%20-%20PEPPER/Documentation/User%20Stories/00%20-%20Contexte%20et%20R%C3%A9f%C3%A9rentiel%20PEPPER.md) — Contexte et référentiel des données PEPPER, indispensables pour l’ingestion documentaire.
- [US-COM-001 - Recherche Expériences pour AO](../../../../01%20-%20AI%20Route%202026/00%20Projects/10%20-%20PEPPER/Gestion%20de%20Projet/Dossiers%20Entretiens%20Personas/08%20-%20Manager%20BU/02%20-%20User%20Stories/US-COM-001%20-%20Recherche%20Exp%C3%A9riences%20pour%20AO.md) — User story clé sur la recherche d’expériences pour les AO, fonction centrale du système.
- [User Stories PEPPER](../../../../01%20-%20AI%20Route%202026/00%20Projects/10%20-%20PEPPER/Documentation/Basics/User%20Stories%20PEPPER.md) — Spécifications des user stories PEPPER, suite logique détaillée du DAF.
<!-- hub-related:end -->
