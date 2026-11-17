
BEGIN TRANSACTION;

INSERT INTO diagnosis_codes (code, description) VALUES ('A00.0', 'Cholera due to Vibrio cholerae 01, biovar cholerae') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A00.1', 'Cholera due to Vibrio cholerae 01, biovar eltor') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A00.9', 'Cholera, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A01.00', 'Typhoid fever, unspecified') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.01', 'Typhoid meningitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.02', 'Typhoid fever with heart involvement') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.03', 'Typhoid pneumonia') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.04', 'Typhoid arthritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.05', 'Typhoid osteomyelitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.09', 'Typhoid fever with other complications') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.1', 'Paratyphoid fever A') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.2', 'Paratyphoid fever B') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.3', 'Paratyphoid fever C') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A01.4', 'Paratyphoid fever, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A02.0', 'Salmonella enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.1', 'Salmonella sepsis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.20', 'Localized salmonella infection, unspecified') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.21', 'Salmonella meningitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.22', 'Salmonella pneumonia') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.23', 'Salmonella arthritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.24', 'Salmonella osteomyelitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.25', 'Salmonella pyelonephritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.29', 'Salmonella with other localized infection') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.8', 'Other specified salmonella infections') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A02.9', 'Salmonella infection, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A03.0', 'Shigellosis due to Shigella dysenteriae') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A03.1', 'Shigellosis due to Shigella flexneri') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A03.2', 'Shigellosis due to Shigella boydii') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A03.3', 'Shigellosis due to Shigella sonnei') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A03.8', 'Other shigellosis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A03.9', 'Shigellosis, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A04.0', 'Enteropathogenic Escherichia coli infection') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.1', 'Enterotoxigenic Escherichia coli infection') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.2', 'Enteroinvasive Escherichia coli infection') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.3', 'Enterohemorrhagic Escherichia coli infection') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.4', 'Other intestinal Escherichia coli infections') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.5', 'Campylobacter enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.6', 'Enteritis due to Yersinia enterocolitica') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.71', 'Enterocolitis due to Clostridium difficile, recurrent') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.72', 'Enterocolitis due to Clostridium difficile, not specified as recurrent') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.8', 'Other specified bacterial intestinal infections') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A04.9', 'Bacterial intestinal infection, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A05.0', 'Foodborne staphylococcal intoxication') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.1', 'Botulism food poisoning') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.2', 'Foodborne Clostridium perfringens [Clostridium welchii] intoxication') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.3', 'Foodborne Vibrio parahaemolyticus intoxication') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.4', 'Foodborne Bacillus cereus intoxication') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.5', 'Foodborne Vibrio vulnificus intoxication') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.8', 'Other specified bacterial foodborne intoxications') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A05.9', 'Bacterial foodborne intoxication, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A06.0', 'Acute amebic dysentery') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.1', 'Chronic intestinal amebiasis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.2', 'Amebic nondysenteric colitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.3', 'Ameboma of intestine') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.4', 'Amebic liver abscess') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.5', 'Amebic lung abscess') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.6', 'Amebic brain abscess') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.7', 'Cutaneous amebiasis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.81', 'Amebic cystitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.82', 'Other amebic genitourinary infections') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.89', 'Other amebic infections') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A06.9', 'Amebiasis, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A07.0', 'Balantidiasis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.1', 'Giardiasis [lambliasis]') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.2', 'Cryptosporidiosis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.3', 'Isosporiasis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.4', 'Cyclosporiasis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.8', 'Other specified protozoal intestinal diseases') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A07.9', 'Protozoal intestinal disease, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A08.0', 'Rotaviral enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.11', 'Acute gastroenteropathy due to Norwalk agent') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.19', 'Acute gastroenteropathy due to other small round viruses') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.2', 'Adenoviral enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.31', 'Calicivirus enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.32', 'Astrovirus enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.39', 'Other viral enteritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.4', 'Viral intestinal infection, unspecified') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A08.8', 'Other specified intestinal infections') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A09', 'Infectious gastroenteritis and colitis, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A15.0', 'Tuberculosis of lung') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.4', 'Tuberculosis of intrathoracic lymph nodes') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.5', 'Tuberculosis of larynx, trachea and bronchus') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.6', 'Tuberculous pleurisy') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.7', 'Primary respiratory tuberculosis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.8', 'Other respiratory tuberculosis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A15.9', 'Respiratory tuberculosis unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A17.0', 'Tuberculous meningitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.1', 'Meningeal tuberculoma') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.81', 'Tuberculoma of brain and spinal cord') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.82', 'Tuberculous meningoencephalitis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.83', 'Tuberculous neuritis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.89', 'Other tuberculosis of nervous system') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A17.9', 'Tuberculosis of nervous system, unspecified') ON CONFLICT (code) DO NOTHING;

INSERT INTO diagnosis_codes (code, description) VALUES ('A18.01', 'Tuberculosis of spine') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.02', 'Tuberculous arthritis of other joints') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.03', 'Tuberculosis of other bones') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.09', 'Other musculoskeletal tuberculosis') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.10', 'Tuberculosis of genitourinary system, unspecified') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.11', 'Tuberculosis of kidney and ureter') ON CONFLICT (code) DO NOTHING;
INSERT INTO diagnosis_codes (code, description) VALUES ('A18.12', 'Tuberculosis of bladder') ON CONFLICT (code) DO NOTHING;

COMMIT;
