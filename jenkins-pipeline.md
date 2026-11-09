
flowchart TD
    A([Start: Trigger Pipeline]) --> B[Checkout kodu z Git]
    B --> C[Budowanie aplikacji]
    C --> D[Testy jednostkowe]
    D --> E[Analiza statyczna kodu]
    E --> F[Analiza bezpieczeństwa]
    
    F --> G{Czy wszystkie kontrole zakończone sukcesem?}
    G -->|Nie| H[Build Failed]
    G -->|Tak| I[Budowanie obrazu Docker]
    
    I --> J[Publikacja obrazu w Registry]
    J --> K[Testy integracyjne]
    
    K --> L{Testy zakończone sukcesem?}
    L -->|Nie| H
    L -->|Tak| M[Wdrożenie na Staging]
    
    M --> N[Testy akceptacyjne / Smoke Tests]
    N --> O{Akceptacja wdrożenia?}
    
    O -->|Nie| P[Rollback / Build Failed]
    O -->|Tak| Q[Zatwierdzenie wdrożenia]
    
    Q --> R[Wdrożenie na Production]
    R --> S[Weryfikacja wdrożenia]
    S --> T([Pipeline zakończony sukcesem])
    
    H --> U([Powiadomienie o błędzie])
    P --> U

    style A fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    style T fill:#dcfce7,stroke:#16a34a,color:#14532d
    style H fill:#fee2e2,stroke:#dc2626,color:#991b1b
    style P fill:#fee2e2,stroke:#dc2626,color:#991b1b
    style U fill:#fef3c7,stroke:#d97706,color:#92400e
