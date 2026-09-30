# Data Model

## Entity relationship
```mermaid
erDiagram
    USER ||--o{ TICKET : submits
    USER ||--o{ TICKET_REVIEW : reviews
    USER o|--o{ DOCUMENT : uploads
    USER {
        int id PK
        string email UK
        string role
    }

    TICKET ||--o{ TICKET_REVIEW : has
    TICKET {
        int id PK
        int user_id FK
        string title
    }

    VISITOR_SPACE o|--o{ DOCUMENT : contains
    VISITOR_SPACE {
        int id PK
        datetime expired_at
    }

    DOCUMENT {
        int id PK
        int user_id FK
        int visitor_space_id FK
        datetime created_at
        datetime updated_at
        datetime expired_at
    }

    TICKET_REVIEW {
        int id PK
        int reviewer_id FK
        int ticket_id FK
        datetime created_at
        datetime updated_at
    }
```

user_id and visitor_space_id on each Document must be exactly one non-null item.
expired_at of intern document are empty, only guest document will be set a expired_at.
