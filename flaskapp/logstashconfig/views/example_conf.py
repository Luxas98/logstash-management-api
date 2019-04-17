patient_conf = {
                "host": "mssql",
                "port": 1433,
                "password": "Password123",
                "username": "sa",
                "table_name": "PATIENT_PATIENT",
                "primary_key": "PATIENTNR",
                "sanitize_columns": [
                    "BSN",
                    "PATIENTNR",
                    "KOPPELSTAT",
                    "NAAMGEBR",
                    "VOORVOEGA",
                    "MEISJESNAA",
                    "VOORVOEGM",
                    "ACHTERNAAM",
                    "ROEPNAAM",
                    "TITELS",
                    "VOORNAAM",
                    "VOORLETTER",
                    "TELEFOON1",
                    "TELEFOON2",
                    "GESLACHT",
                    "GEBDAT",
                    "OVERLEDEN",
                    "OVERLDAT",
                    "BURGSTAAT",
                    "MEERLING",
                    "TAAL",
                    "HUISARTS",
                    "APOTHEEK",
                    "PATCODES",
                    "MEMO",
                    "PATIENTNR_OBJECTID"
                ],
                "joins": [
                    {
                        "table_name": "CSZISLIB_AFWADRES",
                        "key": "PATIENTNR_OBJECTID"
                    }
                ],
                "fields_mappings": [
                    {
                        "field_name": "active",
                        "db_column": "koppelstat",
                        "logstash_field": "[active]",
                        "column_type": "boolean"
                    },
                    {
                        "field_name": "bsn",
                        "db_column": "bsn",
                        "logstash_field": "[identifier][value]"
                    },
                    {
                        "field_name": "patientnr",
                        "db_column": "patientnr",
                        "logstash_field": "[identifier][value]"
                    },
                    {
                        "db_column": "naamgebr",
                        "logstash_field": "[name][text]"
                    },
                    {
                        "db_column": "MEISJESNAA",
                        "logstash_field": "[name][text]",
                        "use": "maiden"
                    },
                    {
                        "db_column": "ACHTERNAAM",
                        "logstash_field": "[name][family]"
                    },
                    {
                        "db_column": "ROEPNAAM",
                        "logstash_field": "[name][text]",
                        "use": "nickname"
                    },
                    {
                        "db_column": "TITELS",
                        "logstash_field": "[name][prefix]"
                    },
                    {
                        "db_column": "VOORNAAM",
                        "logstash_field": "[name][given]"
                    },
                    {
                        "db_column": "TELEFOON1",
                        "logstash_field": "[telecom][value]",
                        "use": "mobile"
                    },
                    {
                        "db_column": "GESLACHT",
                        "logstash_field": "[gender]",
                    },
                    {
                        "db_column": "GEBDAT",
                        "logstash_field": "[birthDate]"
                    },
                    {
                        "db_column": "OVERLEDEN",
                        "logstash_field": "[deceasedBoolean]",
                        "column_type": "boolean"
                    },
                    {
                        "db_column": "BURGSTAAT",
                        "logstash_field": "[maritalStatus][value]"
                    },
                    {
                        "db_column": "MEERLING",
                        "logstash_field": "[multipleBirthBoolean]",
                        "column_type": "boolean"
                    },
                    {
                        "db_column": "TAAL",
                        "logstash_field": "[communication][language][coding][code]"
                    },
                    {
                        "db_column": "HUISARTS",
                        "logstash_field": "[generalPractitioner][reference]"
                    },
                    {
                        "db_column": "APOTHEEK",
                        "logstash_field": "[managingOrganization][reference]"
                    },
                    {
                        "db_column": "PATIENTNR_OBJECTID",
                        "logstash_field": "[identifier][value]"
                    }
                ]
            }