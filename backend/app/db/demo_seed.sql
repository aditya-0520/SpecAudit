-- Synthetic workflow data. DEMO identifiers below are NOT BIS catalogue entries.
WITH snap AS (
  INSERT INTO registry_snapshot(snapshot_date, source_uri, state)
  VALUES ('2026-09-30', NULL, 'DEMO') RETURNING id
), officer AS (
  INSERT INTO app_user(display_name, email, role)
  VALUES ('Ananya Rao', 'ananya.rao@example.invalid', 'Procurement Review Officer') RETURNING id
), a AS (
  INSERT INTO audit(title, tender_id, organization, category, tender_date, language, state, data_state, owner_id, registry_snapshot_id)
  SELECT 'LED Lighting Procurement', 'GEM/2026/B/7142081', 'Public Works Department', 'Lighting', '2026-03-15', 'English', 'Needs review', 'DEMO', officer.id, snap.id
  FROM officer, snap RETURNING id
), sample_standard AS (
  INSERT INTO standard(standard_number, title, registry_state, official_source, snapshot_id)
  SELECT values.standard_number, values.title, 'DEMO', NULL, snap.id
  FROM snap CROSS JOIN (VALUES
    ('DEMO-IS-LGT-2023', 'LED luminaire performance (synthetic sample record)'),
    ('DEMO-IS-SAFE-2022', 'Electrical safety checklist (synthetic sample record)'),
    ('DEMO-IS-TEST-2021', 'Photometric test methods (synthetic sample record)')
  ) AS sample(standard_number, title) RETURNING id, standard_number
), req AS (
  INSERT INTO requirement(audit_id, external_id, text, normalized_text, category, parameter, value, unit, operator, source_page, source_section, source_text, confidence, state)
  SELECT a.id, x.external_id, x.text, x.normalized_text, x.category, x.parameter, x.value, x.unit, x.operator, x.page, x.section, x.text, x.confidence, x.state
  FROM a CROSS JOIN (VALUES
    ('R-01','Nominal input power shall be 36 W ± 5%.','Rated input power equals 36 W ± 5%','Technical','input power','36','W','±',4,'4.1',0.960,'DEMO'),
    ('R-02','Minimum system efficacy of 120 lm/W.','Minimum luminous efficacy 120 lm/W','Performance','luminous efficacy','120','lm/W','>=',4,'4.2',0.940,'DEMO'),
    ('R-03','Select 3000 K, 4000 K or 5700 K by site zone.','Buyer must select correlated colour temperature per site zone','Technical','CCT','3000 / 4000 / 5700','K','choice',5,'4.3',0.780,'REQUIRES_REVIEW'),
    ('R-04','Minimum IP65 for outdoor fixtures.','Outdoor fixture ingress protection at least IP65','Safety','IP rating','65','IP','>=',5,'4.4',0.910,'DEMO'),
    ('R-05','CRI shall be at least 70.','Colour rendering index at least 70','Performance','CRI','70','Ra','>=',5,'4.5',0.830,'DEMO'),
    ('R-06','Operating temperature range is not specified.','Operating temperature range missing','Environmental','operating temperature',NULL,'°C',NULL,6,'4.6',0.890,'REQUIRES_REVIEW'),
    ('R-07','The product should be of good quality and latest technology.','Vague, non-measurable quality wording','Other','quality',NULL,NULL,NULL,6,'4.7',0.980,'REQUIRES_REVIEW'),
    ('R-08','L70 lifetime of 50,000 hours at specified ambient conditions.','L70 lifetime 50,000 hours','Performance','service life','50000','h','>=',6,'4.8',0.870,'REQUIRES_REVIEW'),
    ('R-09','Power factor shall be at least 0.90 at full load.','Power factor at least 0.90 full load','Technical','power factor','0.90',NULL,'>=',7,'4.9',0.900,'DEMO'),
    ('R-10','Total harmonic distortion at most 10%.','Total harmonic distortion maximum ten percent','Technical','THD','10','%','<=',7,'4.10',0.860,'DEMO'),
    ('R-11','Provide surge protection suited to the installation.','Surge protection threshold not stated','Safety','surge protection',NULL,'kV',NULL,7,'4.11',0.810,'REQUIRES_REVIEW'),
    ('R-12','Type test documentation shall be submitted.','Type testing required, method not stated','Testing','type test',NULL,NULL,NULL,8,'4.12',0.760,'REQUIRES_REVIEW'),
    ('R-13','Certification evidence to be supplied where applicable.','Certification applicability unknown','Certification','BIS certification',NULL,NULL,NULL,8,'4.13',0.700,'REQUIRES_REVIEW'),
    ('R-14','Marking content and permanence requirements not stated.','Marking fields and durability incomplete','Marking','marking',NULL,NULL,NULL,9,'4.14',0.880,'REQUIRES_REVIEW'),
    ('R-15','Minimum warranty period of five years.','Warranty at least five years','Warranty','warranty','5','years','>=',9,'4.15',0.950,'DEMO'),
    ('R-16','Fixtures must be protected during transport and storage.','Protect fixtures during transport and storage','Packaging','packaging',NULL,NULL,NULL,10,'4.16',0.830,'DEMO'),
    ('R-17','Inspection and acceptance criteria are not defined.','Inspection and acceptance criteria missing','Inspection','acceptance criteria',NULL,NULL,NULL,10,'4.17',0.930,'REQUIRES_REVIEW')
  ) AS x(external_id,text,normalized_text,category,parameter,value,unit,operator,page,section,confidence,state)
  RETURNING id, external_id
), demo_recommendation AS (
  INSERT INTO standard_recommendation(requirement_id, standard_id, confidence, explanation, evidence_state, review_state)
  SELECT req.id, sample_standard.id, 0.700, '{"note":"Synthetic demo association; not a real standard match."}'::jsonb, 'DEMO', 'REQUIRES_REVIEW'
  FROM req
  JOIN sample_standard ON sample_standard.standard_number = CASE
    WHEN req.external_id IN ('R-01','R-02','R-03','R-04','R-05','R-08','R-09','R-10','R-14') THEN 'DEMO-IS-LGT-2023'
    WHEN req.external_id = 'R-11' THEN 'DEMO-IS-SAFE-2022'
    WHEN req.external_id = 'R-12' THEN 'DEMO-IS-TEST-2021'
    ELSE NULL END
  RETURNING id, requirement_id
)
SELECT count(*) AS demo_requirements_seeded FROM req;

-- The additional sample audit records carry metadata only; no synthetic extraction is
-- represented as expert-validated or as live registry information.
INSERT INTO audit(title, tender_id, organization, category, tender_date, language, state, data_state, registry_snapshot_id)
SELECT v.title, v.tender_id, v.organization, v.category, v.tender_date, 'English', v.state, 'DEMO', s.id
FROM registry_snapshot s
CROSS JOIN (VALUES
  ('Industrial Control Panels','EPC/2026/IND/0842','Industrial Engineering Corporation','Electrical · Industrial','2026-02-10'::date,'In progress'),
  ('Campus Water Pumps','UNI/PROC/2026/119','National Campus Procurement Unit','Pumps · Water systems','2026-01-18'::date,'Approved')
) AS v(title,tender_id,organization,category,tender_date,state)
WHERE s.snapshot_date = '2026-09-30' AND s.state = 'DEMO';
