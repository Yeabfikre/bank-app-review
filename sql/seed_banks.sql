INSERT INTO banks (bank_name, app_name) VALUES
('CBE', 'com.cbe.mobile'),
('BOA', 'com.bankofabyssinia.app'),
('Dashen', 'com.dashenbank.app')
ON CONFLICT (bank_name) DO NOTHING;
