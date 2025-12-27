graph TD
    %% 定義樣式
    classDef largestSCC fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef smallSCC fill:#cceeff,stroke:#0066cc,stroke-width:2px;
    classDef singleSCC fill:#f9f9f9,stroke:#666666,stroke-width:1px;

    %% 最大的 SCC {A, B, C, D}
    subgraph "Largest SCC (Core)"
        A
        B
        C
        D
    end

    %% 較小的 SCC {E, F}
    subgraph "Isolated SCC"
        E
        F
    end

    %% 內部連接 (構成迴圈的部分)
    A --> C
    C --> B
    B --> A
    C --> D
    D --> C
    D --> A
    
    E --> F
    F --> E

    %% 外部連接 (跨區域的單向連接)
    A --> H
    G --> D
    G --> I
    H --> I

    %% 應用樣式
    class A,B,C,D largestSCC;
    class E,F smallSCC;
    class G,H,I singleSCC;
