CREATE TABLE IF NOT EXISTS Roster (
    bandit_id BIGSERIAL PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL,
    bandit_status BOOLEAN NOT NULL,
    specialization TEXT,
    bandit_level INT,
    contacts TEXT,
    appearance_date DATE
);

CREATE TABLE IF NOT EXISTS Bank (
    bank_id BIGSERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    secure_level INT NOT NULL,
    bank_address VARCHAR(255) NOT NULL,
    attractiveness INT,
    daily_revenue BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Robbery (
    robbery_id BIGSERIAL PRIMARY KEY,
    bandit_id BIGINT NOT NULL,          
    bank_id BIGINT NOT NULL,             
    result TEXT NOT NULL,
    robbery_date DATE,
    share FLOAT,
    assessment_of_actions TEXT,
    CONSTRAINT fk_bandit_id FOREIGN KEY(bandit_id)
        REFERENCES Roster(bandit_id) ON DELETE CASCADE,
    CONSTRAINT fk_bank_id FOREIGN KEY(bank_id)
        REFERENCES Bank(bank_id) ON DELETE CASCADE
);