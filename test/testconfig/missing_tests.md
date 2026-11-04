# Fehlende Testfälle in `test/jpp_test` (Stand: 30.10.2026)

> **Update 30.10.2026:** Abschnitt 1 (API-Lücken) und Abschnitt 2
> (Fehlerfall-Lücken) wurden vollständig geschlossen. Siehe die
> `[ERLEDIGT]`-Markierungen in den jeweiligen Tabellen für die konkreten
> neuen Testfälle. Abschnitt 3 (Grenzfälle) ist weiterhin offen.

Analyse basiert auf einem Abgleich der aktuellen Implementierung
(`JsonPreprocessor/CJsonPreprocessor.py`, `common.py`, `imports.py`,
`dollar_syntax.py`, `interpreter.py`, `inline_code.py`, `jsonp_parser.py`)
gegen die 255 Use Cases in `test/testconfig/TestConfig.py`
(ausgeführt über `test/jpp_test/test_usecases.py`).

Seit dieser Analyse wurden 9 neue Use Cases in `TestConfig.py` ergänzt
(Abschnitt 2) sowie das neue Modul `test/jpp_test/test_api.py` mit 14
Tests (Abschnitt 1) hinzugefügt; die Suite umfasst jetzt 278 Tests.

Methode: alle Fehlermeldungen (`JsonpError(...)`/`raise Exception(...)`) und
alle öffentlichen API-Pfade wurden extrahiert und per Volltextsuche gegen
`TestConfig.py` auf mindestens einen Treffer geprüft.

---

## 1. Komplett ungetestete öffentliche API-Methoden `[ERLEDIGT]`

Alle Punkte durch neues Modul `test/jpp_test/test_api.py` (14 Tests) abgedeckt.

| # | Feature | Fundstelle | Befund | Test |
|---|---|---|---|---|
| 1.1 | `json_loads()` / `jsonLoads()` - Laden von JSONP-Inhalt **aus einem String** (kein Datei-Pfad), inkl. Parameter `reference_dir` | `CJsonPreprocessor.py` | Kein einziger Testfall. Wird aber produktiv von `robotframework-testsuitesmanagement` und `test/testtools/GenSnippetsJPP.py` verwendet - Regressionsrisiko bleibt unentdeckt. | `test_json_loads_and_jsonLoads_are_equivalent`, `test_json_loads_requires_string_content`, `test_json_loads_rejects_missing_reference_dir` |
| 1.2 | `json_dump()` / `jsonDump()` - Schreiben eines dict zurück in eine JSON-Datei, Rückgabe des normalisierten Pfades | `CJsonPreprocessor.py` | Kein Test. | `test_json_dump_writes_normalized_file` |
| 1.3 | Konstruktor-Parameter `current_cfg` (Vorbelegung des Parameter-Stores mit bereits vorhandenen Werten) | `CJsonPreprocessor.__init__` | Immer Default `{}`; nie mit echtem Inhalt getestet. | `test_current_cfg_preseeds_parameter_store` |
| 1.4 | Konstruktor-Parameter `key_pattern` (benutzerdefinierte Regex für gültige Key-Namen) | `CJsonPreprocessor.__init__`, `CKeyChecker` | Immer Default `.+`; eigenes Pattern (z. B. nur Kleinbuchstaben) und der daraus resultierende Validierungsfehler (`CKeyChecker.key_name_checker`) nie getestet. | `test_key_pattern_accepts_matching_key`, `test_key_pattern_rejects_non_matching_key` |
| 1.5 | `syntax=CSyntaxType.json` (reines JSON, **ohne** Python-Keywords `True`/`False`/`None`) | `CSyntaxType` | Die `jpp`-Fixture (`conftest.py`) instanziiert ausschließlich `CJsonPreprocessor()` mit Default `syntax=python`. Verhalten bei strikt JSON-konformer Syntax (z. B. Ablehnung von `True`/`None` als Literal) ist ungetestet. | `test_syntax_json_parses_json_literals`, `test_syntax_json_rejects_python_keywords` |
| 1.6 | `getVersion()` / `getVersionDate()` | `CJsonPreprocessor.py` | Trivial, aber 0 Abdeckung. | `test_get_version_and_version_date` |
| 1.7 | Konstruktor-Validierung von `key_pattern` selbst: `TypeError`/`Exception` bei Nicht-String, bei `''`, bei `'.*'` und bei reinem Whitespace-Pattern | `CJsonPreprocessor.__init__` | Kein Test. | `test_constructor_rejects_invalid_key_patterns` (parametrisiert) |

---

## 2. Fehlende Fehlerfall-Testfälle (vorhandene Exception-Pfade ohne Testfall) `[ERLEDIGT]`

Alle Punkte durch neue Use Cases in `test/testconfig/TestConfig.py` abgedeckt.

| # | Fehlermeldung / Feature | Fundstelle | Auslöser (Beispiel) | TESTID |
|---|---|---|---|---|
| 2.1 | `"The imported file '...' must contain a JSON object."` | `imports.py` (`ImportResolver.import_file`) | `[import]`-Zieldatei, deren Root-Element ein Array ist (`[...]` statt `{...}`). | `JPP_1167` |
| 2.2 | `"Invalid syntax! Sub-element '...' need to be referenced using ${...} or enclosed in quotes ['...']"` | `dollar_syntax.py` (`_parse_index`) | z. B. `${list[sub-element]}` - ein Bezeichner als Index, weder gequotet noch als `${}`-Referenz. | `JPP_0275` |
| 2.3 | `"Expression '...' cannot be evaluated. ... A pair of square brackets is empty or contains not allowed characters."` | `dollar_syntax.py` (`_parse_index`, `strict`-Modus) | `${x[]}` oder `${x[ @#$ ]}` als Value/Key (unquotiert, strict-Kontext). | `JPP_0276` |
| 2.4 | `"The Python builtIn '...' return the value with the datatype ... is not suitable for JSON."` | `inline_code.py` (`InlineCodeEvaluator.evaluate`) | Inline-Code `<<...>>`, der z. B. ein `set`, eine Funktion oder ein Tuple zurückgibt (nicht JSON-kompatibler Typ). | `JPP_2196` |
| 2.5 | `"The Python builtIn must not be empty."` | `jsonp_parser.py` (`_scan_inline`) | Leerer Inline-Code-Block: `<<>>`. | `JPP_2197` |
| 2.6 | `"Type error in key b'...'. Key names must be strings; byte values are not supported."` | `jsonp_parser.py` (`_scan_key`) | Byte-Literal als Key: `b'xyz': "value"`. | `JPP_2651` |
| 2.7 | `"Python inline code must not be embedded part of a string!"` | `jsonp_parser.py` (`_make_string`) | Inline-Code **innerhalb** eines gequoteten Strings, z. B. `"text <<1+1>> text"`. | `JPP_2198` |
| 2.8 | `"Invalid expression found: '...' - The double quotes are missing!!!"` | `jsonp_parser.py` (`_raise_invalid_bare`) | Unquotiertes `$`-Fragment ohne gültige `${...}`-Struktur, z. B. `key: $notaref`. | `JPP_0277` |
| 2.9 | `"A substitution in key names is not allowed! Please update the key name ..."` (gequoteter Key mit `${...}` darin) | `jsonp_parser.py` (`_literal_key`) | `"my_${param}_key": "value"` als **gequoteter** String-Key (zu unterscheiden von der regulären Dollar-Key-Syntax ohne Anführungszeichen, die bereits getestet ist). | `JPP_0467` |
| 2.10 | Zwei-Datei-Variante der Cyclic-Import-Meldung: `"...is imported by '{A}' and by file '{B}'"` | `imports.py` (`ImportResolver.import_file`) | Bestehende Cyclic-Import-Testfälle (`JPP_1150`-`1166`) prüfen nur generisch auf den Teilstring `"Cyclic import detection"`. Der spezifische Zweig für "Datei X wird von zwei unterschiedlichen Elternknoten importiert" (statt Selbst-Import) ist nicht gezielt mit seinem vollen Meldungstext verifiziert. | `JPP_1165` (Assertion verschärft auf `"Cyclic import detection: The file"`) |

---

## 3. Grenzfälle mit unklarer/geringerer Priorität

| # | Feature | Fundstelle | Hinweis |
|---|---|---|---|
| 3.1 | `CTextProcessor.normalize_digits()` - Umwandlung von **Unicode-Ziffern** innerhalb eckiger Klammern (z. B. arabisch-indische Ziffern `[١٢]`) zu ASCII-Ziffern bei Index-Zugriffen | `common.py` | Kein Testfall mit nicht-ASCII-Ziffern als Index gefunden. |
| 3.2 | `Interpreter._name_of()` - verschachtelte Referenz als Teil eines Parameternamens, bei der der aufgelöste Wert selbst ein `dict`/`list` ist (löst `_raise_invalid_index` über den "Name"-Pfad statt über den "Index"-Pfad aus) | `interpreter.py` | Pfad vorhanden, aber ohne gezielten Testfall; Abdeckung über bestehende Tests nicht sicher nachweisbar. |
| 3.3 | `CTextProcessor.multiple_replace()` | `common.py` | Generische Utility-Methode ohne erkennbare aktive Verwendung im aktuellen Code - vermutlich Legacy; kein Test vorhanden. |

---

## Priorisierung

1. **Abschnitt 1** (API-Lücken) - höchste Priorität, insbesondere 1.1 (`json_loads`/`jsonLoads`),
   da diese Methode nachweislich von `robotframework-testsuitesmanagement` produktiv genutzt wird,
   aber im eigenen Testsuite des `python-jsonpreprocessor` nicht ein einziges Mal aufgerufen wird.
2. **Abschnitt 2** (Fehlerfälle) - reale, im Code vorhandene Exception-Pfade ohne jegliche Verifikation.
3. **Abschnitt 3** (Grenzfälle) - geringere Priorität, ggf. Legacy-Code ohne aktive Nutzung.
