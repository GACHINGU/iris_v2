CREATE TABLE fx_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency_pair VARCHAR(10),
    rate_date DATE,
    time_recorded TIME,
    source VARCHAR(20),
    rate DECIMAL(8,4),
    UNIQUE KEY (currency_pair, rate_date, time_recorded, source)
)

DESCRIBE fx_rates;

ALTER TABLE fx_rates
MODIFY currency_pair VARCHAR(10) NOT NULL;

ALTER TABLE fx_rates
MODIFY rate_date DATE NOT NULL;

ALTER TABLE fx_rates
MODIFY time_recorded TIME NOT NULL;

ALTER TABLE fx_rates
MODIFY source VARCHAR(20) NOT NULL;

ALTER TABLE fx_rates
MODIFY rate DECIMAL(8,4) NOT NULL;